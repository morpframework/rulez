import shlex
import re
import boolean
import json


class AND(boolean.AND):

    def json(self):
        return {
            'operator': 'and',
            'value': [a.json() for a in self.args]
        }


class OR(boolean.OR):
    def json(self):
        return {
            'operator': 'or',
            'value': [a.json() for a in self.args]
        }


class FIELD(boolean.Symbol):

    def decode_symbol(self):
        for op in ['==', '<=', '>=', '!=', '<', '>', '=', ' in ']:
            if op in self.obj:
                k, v = self.obj.split(op)
                if op.strip() in ['in']:
                    v = json.loads(v)
                else:
                    v = v.strip()
                return k.strip(), op.strip(), v
        raise ValueError("Unable to decode symbol '%s'" % self.obj)

    def json(self):
        s = self.decode_symbol()
        k, o, v = s
        value = v
        if isinstance(value, str):
            if re.match(r'^[\d\.]+$', value):
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
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


def parse_dsl(s):
    algebra = BooleanAlgebra()
    parsed = algebra.parse(s)
    return parsed.json()


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
