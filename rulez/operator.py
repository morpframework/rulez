import reg
import operator as op
from .engine import Engine


class Operator(object):
    def __init__(self, operator, engine, value):
        self.operator = operator
        vals = []
        for v in value or []:
            op = v["operator"]
            value = v["value"]
            field = v.get("field", None)
            o = engine.get_operator(op, value, field)
            vals.append(o)
        self.value = vals


@Engine.operator(operator="and", types=[list, tuple])
class And(Operator):
    """Apply boolean ``AND`` condition to list of values

    :operator: ``and``
    :value_types: ``list``, ``tuple``

    Items in values have to be a compilable ``rulez`` operator
    JSON
    """

    pass


@Engine.operator(operator="or", types=[list, tuple])
class Or(Operator):
    """Apply boolean ``OR`` condition to list of values

    :operator: ``or``
    :value_types: ``list[rulez_operation]``, ``tuple[rulez_operation]``

    Items in values have to be a compilable ``rulez`` operation
    JSON
    """

    pass


class FieldOperator(Operator):
    def __init__(self, operator, engine, field, value):
        self.operator = operator
        self.field = field
        if isinstance(value, dict) and value.get("operator", None):
            value = engine.get_operator(**value)
        self.value = value


@Engine.operator(operator="==", types=[dict, str, float, int])
class Equal(FieldOperator):
    """
    Compare whether contents of field is same as value

    :operator: ``==``
    :value_types: ``rulez_operation``, ``str``, ``float``, ``int``

    """

    pass


@Engine.operator(operator="!=", types=[dict, str, float, int])
class NotEqual(FieldOperator):
    """
    Compare whether contents of field is not equal to value

    :operator: ``!=``
    :value_types: ``rulez_operation``, ``str``, ``float``, ``int``

    """

    pass


@Engine.operator(operator="<=", types=[dict, str, float, int])
class LessEqualThan(FieldOperator):
    """
    Compare whether contents of field is less equal than value

    :operator: ``<=``
    :value_types: ``rulez_operation``, ``str``, ``float``, ``int``

    """

    pass


@Engine.operator(operator=">=", types=[dict, str, float, int])
class GreaterEqualThan(FieldOperator):
    """
    Compare whether contents of field is greater equal than value

    :operator: ``>=``
    :value_types: ``rulez_operation``, ``str``, ``float``, ``int``

    """

    pass


@Engine.operator(operator="<", types=[dict, str, float, int])
class LessThan(FieldOperator):
    """
    Compare whether contents of field is less than value

    :operator: ``<``
    :value_types: ``rulez_operation``, ``str``, ``float``, ``int``

    """

    pass


@Engine.operator(operator=">", types=[dict, str, float, int])
class GreaterThan(FieldOperator):
    """
    Compare whether contents of field is greater than value

    :operator: ``>``
    :value_types: ``rulez_operation``, ``str``, ``float``, ``int``

    """

    pass


@Engine.operator(operator="in", types=[list, tuple])
class In(FieldOperator):

    """Apply boolean ``OR`` condition to list of values

    :operator: ``or``
    :value_types: ``list[rulez_operation]``, ``tuple[rulez_operation]``,
                  ``list[str]``, ``list[float]``, ``list[int]``

    """

    pass


class FieldGetter(Operator):
    def __init__(self, operator, engine, value):
        self.operator = operator
        self.value = value


@Engine.operator(operator="get", types=[str])
class Get(FieldGetter):
    """Get value from a field

    :operator: ``get``
    :value_types: ``field_name``

    """

    pass


@Engine.operator(operator="~", types=[str])
class Like(FieldOperator):
    """
    Compare whether contents of field is like value

    :operator: ``~``
    :value_types: ``str``

    """

    pass


@Engine.operator(operator="match", types=[str])
class Match(FieldOperator):
    """
    Compare whether contents of field matches value

    :operator: ``match``
    :value_types: ``str``

    .. warning:: This operator only supported in ``sqlalchemy`` compiler.
    """

    pass
