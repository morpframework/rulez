import shlex
import re
import boolean
import json
from .engine import OperatorNotAllowedError
import warnings
import typing


class AND(boolean.AND):
    def json(self, allowed_operators=None):
        allowed_operators = allowed_operators or []
        values = []
        for a in self.args:
            j = a.json(allowed_operators)
            if allowed_operators and j["operator"].lower() not in allowed_operators:
                raise OperatorNotAllowedError(j["operator"])
            values.append(j)
        return Operation({"operator": "and", "value": values})


class OR(boolean.OR):
    def json(self, allowed_operators=None):
        allowed_operators = allowed_operators or []
        values = []
        for a in self.args:
            j = a.json(allowed_operators)
            if allowed_operators and j["operator"].lower() not in allowed_operators:
                raise OperatorNotAllowedError(j["operator"])
            values.append(j)
        return Operation({"operator": "or", "value": values})


float_pattern = re.compile(r"^\d+\.\d+$")
int_pattern = re.compile(r"^\d+$")
str1_pattern = re.compile(r'^"[\w+ ]*"$')
str2_pattern = re.compile(r"^'[\w+ ]*'$")
field_pattern = re.compile(r"^\w+$")


class FIELD(boolean.Symbol):
    def decode_symbol(self):
        for op in ["==", "<=", ">=", "!=", "<", ">", "=", " in "]:
            if op in self.obj:
                ss = self.obj.split(op)
                if len(ss) != 2:
                    raise ValueError('Unable to decode "%s"' % self.obj)
                k, v = ss
                if op.strip() in ["in"]:
                    ov = v.strip()
                    if ov.startswith("(") or ov.startswith("["):
                        ov = ov[1:]
                    if ov.endswith(")") or ov.endswith("]"):
                        ov = ov[:-1]
                    ov = ov.strip().split(",")
                    v = []
                    for vv in ov:
                        vv = vv.strip()
                        if float_pattern.match(vv):
                            vv = float(vv)
                        elif int_pattern.match(vv):
                            vv = int(vv)
                        elif str1_pattern.match(vv) or str2_pattern.match(vv):
                            vv = vv[1:-1]
                        v.append(vv)
                else:
                    v = v.strip()
                return k.strip(), op.strip(), v
        if field_pattern.match(self.obj):
            return None, None, Field(self.obj)
        raise ValueError("Unable to decode symbol '%s'" % self.obj)

    def json(self, allowed_operators=None):
        allowed_operators = allowed_operators or []
        s = self.decode_symbol()
        k, o, v = s
        if k is None and o is None and isinstance(v, Field):
            return v
        value = v
        if isinstance(value, str):
            if float_pattern.match(value):
                value = float(value)
            elif int_pattern.match(value):
                value = int(value)
            elif str1_pattern.match(value) or str2_pattern.match(value):
                value = value[1:-1]
            elif field_pattern.match(value):
                value = Field(value)
            else:
                raise ValueError("Unable to decode value '%s'" % value)
        if allowed_operators and o.lower() not in allowed_operators:
            raise OperatorNotAllowedError(o)
        return Operation({"field": k, "operator": o, "value": value})


class BooleanAlgebra(boolean.BooleanAlgebra):
    def __init__(self):
        super(BooleanAlgebra, self).__init__(
            Symbol_class=FIELD, AND_class=AND, OR_class=OR
        )

    def tokenize(self, s):
        ops = {
            "or": boolean.TOKEN_OR,
            "and": boolean.TOKEN_AND,
            "(": boolean.TOKEN_LPAR,
            ")": boolean.TOKEN_RPAR,
        }

        tokens = []
        s = s.replace("(", " ( ")
        s = s.replace(")", " ) ")
        s = s.replace("]", " ] ")
        s = s.replace("[", " [ ")
        splitted = shlex.split(s, posix=False)
        for t in splitted:
            if t.lower() in ops.keys():
                tokens.append(t)
            else:
                if not tokens:
                    tokens.append(t)
                elif tokens[-1].lower() in ops.keys():
                    tokens.append(t)
                else:
                    tokens[-1] += " %s" % t

        for col, tok in enumerate(tokens):
            if tok.lower() in ops:
                yield ops[tok.lower()], tok, col
            else:
                yield boolean.TOKEN_SYMBOL, tok, col


def or_(*args):
    return {"operator": "or", "value": list(args)}


def and_(*args):
    return {"operator": "and", "value": list(args)}


class Operation(dict):
    def __and__(self, value):
        return Operation(and_(self, value))

    def __or__(self, value):
        return Operation(or_(self, value))


class Field(dict):
    def __init__(self, key):
        self.key = key
        super().__init__({"operator": "get", "value": key})

    def __eq__(self, value):
        return Operation({"field": self.key, "operator": "==", "value": value})

    def __gt__(self, value):
        return Operation({"field": self.key, "operator": ">", "value": value})

    def __lt__(self, value):
        return Operation({"field": self.key, "operator": "<", "value": value})

    def __ge__(self, value):
        return Operation({"field": self.key, "operator": ">=", "value": value})

    def __le__(self, value):
        return Operation({"field": self.key, "operator": "<=", "value": value})

    def __ne__(self, value):
        return Operation({"field": self.key, "operator": "!=", "value": value})

    def in_(self, values):
        if not isinstance(values, list):
            raise TypeError("Expected a list")
        return Operation({"field": self.key, "operator": "in", "value": values})

    def __and__(self, value):
        return Operation(and_(self, value))

    def __or__(self, value):
        return Operation(or_(self, value))


class FieldGetter(object):
    def __getitem__(self, key):
        """

        .. code-block:: pycon

           >>> import rulez

           >>> rulez.field['field1']
           { 'operator': 'get', 'value': 'field1' }

           >>> rulez.field['field1'] == 'myvalue'
           { 'field': 'field1', 'operator': '==', 'value': 'myvalue' }

           >>> rulez.field['field1'] == rulez.field['field2']
           { 'field': 'field1', 'operator': '==',
             'value': {
                   'operator': 'get',
                   'value': 'field2' }}

           >>> rulez.field['field1'] & rulez.field['field2']
           {'operator': 'and',
            'value': [
                {'operator': 'get', 'value': 'field1'},
                {'operator': 'get', 'value': 'field2'}]}

           >>> rulez.field['field1'] | rulez.field['field2']
           {'operator': 'or',
            'value': [
                {'operator': 'get', 'value': 'field1'},
                {'operator': 'get', 'value': 'field2'}]}

        .. note::

           ``rulez.field[key]`` is deprecated at version 0.1.4 in favor of
           ``rulez.field(key)``.

        """

        warnings.warn("Getitem accessor is deprecated", DeprecationWarning)
        return Field(key)

    def __call__(self, key):

        """

        .. code-block:: pycon

           >>> import rulez

           >>> rulez.field('field1')
           { 'operator': 'get', 'value': 'field1' }

           >>> rulez.field('field1') == 'myvalue'
           { 'field': 'field1', 'operator': '==', 'value': 'myvalue' }

           >>> rulez.field('field1') == rulez.field('field2')
           { 'field': 'field1', 'operator': '==',
             'value': {
                   'operator': 'get',
                   'value': 'field2' }}

           >>> rulez.field('field1') & rulez.field('field2')
           {'operator': 'and',
            'value': [
                {'operator': 'get', 'value': 'field1'},
                {'operator': 'get', 'value': 'field2'}]}

           >>> rulez.field('field1') | rulez.field('field2')
           {'operator': 'or',
            'value': [
                {'operator': 'get', 'value': 'field1'},
                {'operator': 'get', 'value': 'field2'}]}

        """

        return Field(key)


field = FieldGetter()


def parse_dsl(
    s, allowed_operators: typing.Optional[typing.List[str]] = None
) -> Operation:
    """
    Parse string and output comparison operation.

    :param s: query string
    :param allowed_operators: List of allowed operators
    :type allowed_operators: typing.Optional[typing.List[str]]

    .. code-block:: pycon

       >>> import rulez
       >>> rulez.parse_dsl("field1 == field2")
       {'field': 'field1', 'operator': '==',
        'value': {'operator': 'get',
                  'value': 'field2'}}

       >>> rulez.parse_dsl("field1 == 'hello world'")
       {'field': 'field1', 'operator': '==',
        'value': 'hello world'}

       >>> rulez.parse_dsl("(field1 == field2) or (field3 == 'value1')")
       {'operator': 'or',
        'value': [{'field': 'field1', 'operator': '==',
                   'value': {'operator': 'get', 'value': 'field2'}},
                  {'field': 'field3', 'operator': '==',
                    'value': 'value1'}]}

       >>> rulez.parse_dsl('field1 in ["a","b","c"]')
       {'field': 'field1', 'operator': 'in', 'value': ['a', 'b', 'c']}

       >>> rulez.parse_dsl('field1 in in [1.0,2.0,3.0]')
       {'field': 'field1', 'operator': 'in', 'value': [1.0, 2.0, 3.0]}


    """
    allowed_operators = allowed_operators or []
    algebra = BooleanAlgebra()
    parsed = algebra.parse(s)
    res = parsed.json(allowed_operators)
    for i in res:
        if allowed_operators and (res["operator"].lower() not in allowed_operators):
            raise OperatorNotAllowedError(res["operator"])
    return res
