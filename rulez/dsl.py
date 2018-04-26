import shlex
import re
import boolean
import json
from .engine import OperatorNotAllowedError


class AND(boolean.AND):

    def json(self, allowed_operators=None):
        allowed_operators = allowed_operators or []
        values = []
        for a in self.args:
            j = a.json(allowed_operators)
            if allowed_operators and j['operator'].lower() not in allowed_operators:
                raise OperatorNotAllowedError(j['operator'])
            values.append(j)
        return {
            'operator': 'and',
            'value': values
        }


class OR(boolean.OR):

    def json(self, allowed_operators=None):
        allowed_operators = allowed_operators or []
        values = []
        for a in self.args:
            j = a.json(allowed_operators)
            if allowed_operators and j['operator'].lower() not in allowed_operators:
                raise OperatorNotAllowedError(j['operator'])
            values.append(j)
        return {
            'operator': 'or',
            'value': values
        }


class FIELD(boolean.Symbol):

    def decode_symbol(self):
        for op in ['==', '<=', '>=', '!=', '<', '>', '=', ' in ']:
            if op in self.obj:
                ss = self.obj.split(op)
                if len(ss) != 2:
                    raise ValueError('Unable to decode "%s"' % self.obj)
                k, v = ss
                if op.strip() in ['in']:
                    v = json.loads(v)
                else:
                    v = v.strip()
                return k.strip(), op.strip(), v
        raise ValueError("Unable to decode symbol '%s'" % self.obj)

    def json(self, allowed_operators=None):
        allowed_operators = allowed_operators or []
        s = self.decode_symbol()
        k, o, v = s
        value = v
        if isinstance(value, str):
            if re.match(r'^[\d\.]+$', value):
                if value.find('.') == 1:
                    value = float(value)
                elif value.find('.') < 1:
                    value = int(value)
        if allowed_operators and o.lower() not in allowed_operators:
            raise OperatorNotAllowedError(o)
        return {
            'field': k,
            'operator': o,
            'value': value
        }


class BooleanAlgebra(boolean.BooleanAlgebra):

    def __init__(self):
        super(BooleanAlgebra, self).__init__(
            Symbol_class=FIELD, AND_class=AND, OR_class=OR)

    def tokenize(self, s):
        ops = {
            'or': boolean.TOKEN_OR,
            'and': boolean.TOKEN_AND,
            '(': boolean.TOKEN_LPAR,
            ')': boolean.TOKEN_RPAR
        }

        tokens = []
        splitted = shlex.split(s)

        for t in splitted:
            if t.lower() in ops.keys():
                tokens.append(t)
            else:
                if not tokens:
                    tokens.append(t)
                elif tokens[-1].lower() in ops.keys():
                    tokens.append(t)
                else:
                    tokens[-1] += ' %s' % t

        for col, tok in enumerate(tokens):
            if tok.lower() in ops:
                yield ops[tok.lower()], tok, col
            else:
                yield boolean.TOKEN_SYMBOL, tok, col


def parse_dsl(s, allowed_operators=None):
    allowed_operators = allowed_operators or []
    algebra = BooleanAlgebra()
    parsed = algebra.parse(s)
    res = parsed.json(allowed_operators)
    for i in res:
        if allowed_operators and (
                res['operator'].lower() not in allowed_operators):
            raise OperatorNotAllowedError(res['operator'])
    return res


class Field(object):

    def __init__(self, key):
        self.key = key

    def __eq__(self, value):
        return {
            'field': self.key,
            'operator': '==',
            'value': value
        }

    def __gt__(self, value):
        return {
            'field': self.key,
            'operator': '>',
            'value': value
        }

    def __lt__(self, value):
        return {
            'field': self.key,
            'operator': '<',
            'value': value
        }

    def __ge__(self, value):
        return {
            'field': self.key,
            'operator': '>=',
            'value': value
        }

    def __le__(self, value):
        return {
            'field': self.key,
            'operator': '<=',
            'value': value
        }

    def __ne__(self, value):
        return {
            'field': self.key,
            'operator': '!=',
            'value': value
        }

    def in_(self, values):
        return {
            'field': self.key,
            'operator': 'in',
            'value': values
        }


def or_(*args):
    return {
        'operator': 'or',
        'value': list(args)
    }


def and_(*args):
    return {
        'operator': 'and',
        'value': list(args)
    }


class FieldGetter(object):

    def __getitem__(self, key):
        return Field(key)


field = FieldGetter()
