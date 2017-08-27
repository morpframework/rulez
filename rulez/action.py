import reg
from .engine import Engine
from . import operator as op


class Action(object):
    pass


@Engine.action(action='set')
class Set(Action):

    @property
    def identifier(self):
        return ':'.join([self.action, self.field])

    def __init__(self, action, engine, field, value):
        self.action = action
        self.field = field
        if isinstance(value, dict):
            value = engine.get_operator(**value)
        self.value = value
