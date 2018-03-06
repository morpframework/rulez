import reg
import operator as op
from .engine import Engine


class Operator(object):

    def __init__(self, operator, engine, value):
        self.operator = operator
        vals = []
        for v in (value or []):
            op = v['operator']
            value = v['value']
            field = v.get('field', None)
            o = engine.get_operator(op, value, field)
            vals.append(o)
        self.value = vals


@Engine.operator(operator='and', types=[list, tuple])
class And(Operator):
    pass


@Engine.operator(operator='or', types=[list, tuple])
class Or(Operator):
    pass


class FieldOperator(Operator):

    def __init__(self, operator, engine, field, value):
        self.operator = operator
        self.field = field
        if isinstance(value, dict) and value.get('operator', None):
            value = engine.get_operator(**value)
        self.value = value


@Engine.operator(operator='==', types=[dict, str, float, int])
class Equal(FieldOperator):
    pass


@Engine.operator(operator='!=', types=[dict, str, float, int])
class NotEqual(FieldOperator):
    pass


@Engine.operator(operator='<=', types=[dict, str, float, int])
class LessEqualThan(FieldOperator):
    pass


@Engine.operator(operator='>=', types=[dict, str, float, int])
class GreaterEqualThan(FieldOperator):
    pass


@Engine.operator(operator='<', types=[dict, str, float, int])
class LessThan(FieldOperator):
    pass


@Engine.operator(operator='>', types=[dict, str, float, int])
class GreaterThan(FieldOperator):
    pass


@Engine.operator(operator='in', types=[list, tuple])
class In(FieldOperator):
    pass


class FieldGetter(Operator):

    def __init__(self, operator, engine, value):
        self.operator = operator
        self.value = value


@Engine.operator(operator='get', types=[str])
class Get(FieldGetter):
    pass


@Engine.operator(operator='~', types=[str])
class Like(FieldOperator):
    pass
