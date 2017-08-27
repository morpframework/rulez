
from ... import action as ra
from ... import operator as op
from ...engine import Engine

METHOD = 'native'


@Engine.rulechain_compiler(method=METHOD)
def _compile_rulechain(engine, method, rulechain):
    def apply(obj):
        for rule in rulechain:
            def condition(obj): return obj
            if rule.get('condition', None):
                condition = engine.compile_condition(
                    method, rule.get('condition', None))
            if condition(obj):
                actions = [engine.get_action(**act) for act in rule['actions']]
                for a in actions:
                    engine.compile_action(method, a)(obj)
                return obj
        return obj
    return apply


@Engine.action_compiler(method=METHOD, action=ra.Set)
def set(engine, method, action):
    def func(data):
        value = action.value
        if isinstance(value, op.Operator):
            value = engine.compile_operator(method, value)(data)
        data[action.field] = value
        return data
    return func
