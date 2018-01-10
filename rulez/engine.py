import dectate
import reg


class OperatorNotAllowedError(Exception):

    def __init__(self, message, *args, **kwargs):
        message = "Operator '%s' is not allowed" % message
        super(OperatorNotAllowedError, self).__init__(message, *args, **kwargs)


class NestedOperationNotAllowedError(Exception):

    def __init__(self, message, *args, **kwargs):
        message = "NestedOperation '%s' is not allowed" % message
        super(NestedOperationNotAllowedError, self).__init__(
            message, *args, **kwargs)


class OperatorAction(dectate.Action):

    app_class_arg = True

    def __init__(self, operator, type_):
        self.operator = operator
        self.type = type_

    def identifier(self, app_class):
        return str((app_class, self.operator, self.type))

    def perform(self, op, app_class):

        def operator(engine, operator, value, field=None):
            if field is not None:
                return op(operator, engine, field, value)
            return op(operator, engine, value)

        app_class.get_operator.register(operator,
                                        operator=self.operator,
                                        value=self.type)


class OperatorCompilerAction(dectate.Action):

    app_class_arg = True

    def __init__(self, method, operator):
        self.method = method
        self.operator = operator

    def identifier(self, app_class):
        return str((app_class, self.method, self.operator))

    def perform(self, obj, app_class):

        app_class.compile_operator.register(
            method=self.method,
            operator=self.operator)(obj)


class ActionAction(dectate.Action):

    app_class_arg = True

    def __init__(self, action):
        self.action = action

    def identifier(self, app_class):
        return str((app_class, self.action))

    def perform(self, obj, app_class):

        @app_class.get_action.register(action=self.action)
        def action(engine, action, parameter):
            return obj(self.action, engine, **parameter)


class ActionCompilerAction(dectate.Action):

    app_class_arg = True

    def __init__(self, method, action):
        self.method = method
        self.action = action

    def identifier(self, app_class):
        return str((app_class, self.method, self.action))

    def perform(self, obj, app_class):
        app_class.compile_action.register(
            method=self.method, action=self.action)(obj)


class RuleChainCompilerAction(dectate.Action):

    app_class_arg = True

    def __init__(self, method):
        self.method = method

    def identifier(self, app_class):
        return str((app_class, self.method))

    def perform(self, obj, app_class):

        app_class.compile_rulechain.register(
            method=self.method)(obj)


class Engine(dectate.App):

    _operator = dectate.directive(OperatorAction)

    rulechain_compiler = dectate.directive(RuleChainCompilerAction)
    action = dectate.directive(ActionAction)

    @classmethod
    def operator(klass, operator, types):
        def func(op):
            for t in types + [type(None)]:
                klass._operator(operator, t)(op)
            return op
        return func

    operator_compiler = dectate.directive(OperatorCompilerAction)

    action_compiler = dectate.directive(ActionCompilerAction)

    @reg.dispatch_method(
        reg.match_key('operator',
                      lambda self, operator, value, field: operator),
        reg.match_instance('value'))
    def get_operator(self, operator, value, field=None):
        raise NotImplementedError

    @reg.dispatch_method(
        reg.match_key('method',
                      lambda self, method, operator: method),
        reg.match_instance('operator'))
    def compile_operator(self, method, operator):
        raise NotImplementedError((method, operator))

    @reg.dispatch_method(
        reg.match_key('action', lambda self, action, parameter: action))
    def get_action(self, action, parameter):
        raise NotImplementedError((action, parameter))

    @reg.dispatch_method(
        reg.match_key('method', lambda self, method, action: method),
        reg.match_instance('action'))
    def compile_action(self, method, action):
        raise NotImplementedError((method, action))

    def parse_condition(self, config):
        param = {
            'operator': config['operator'],
            'value': config['value']
        }
        if config.get('field', None):
            param['field'] = config['field']

        parsed = self.get_operator(**param)
        return parsed

    def parse_action(self, config):
        return self.get_action(**config)

    def compile_condition(self, method, query, allowed_operators=None,
                          nestable_operators=None):
        self.validate_condition(query, allowed_operators, nestable_operators)
        q = self.parse_condition(query)
        return self.compile_operator(method, q)

    @reg.dispatch_method(
        reg.match_key('method', lambda self, method, rulechain: method))
    def compile_rulechain(self, method, rulechain):
        raise NotImplementedError

    def validate_condition(self, query, allowed_operators=None,
                           nestable_operators=None):
        parsed = self.parse_condition(query)
        self._validate_condition(parsed, allowed_operators, nestable_operators)

    def _validate_condition(self, query, allowed_operators=None,
                            nestable_operators=None):
        from .operator import Operator

        if (allowed_operators is not None and
                query.operator not in allowed_operators):
            raise OperatorNotAllowedError(query.operator)

        if isinstance(query.value, list) or isinstance(query.value, tuple):
            for v in query.value:
                if isinstance(v, Operator):
                    if (nestable_operators is not None and
                            query.operator in nestable_operators and
                            v.operator in nestable_operators):
                        raise NestedOperationNotAllowedError(query)
                    self._validate_condition(v, allowed_operators)
