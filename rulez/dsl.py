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
