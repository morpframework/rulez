#
from .engine import OperatorNotAllowedError
from .compiler import native, sqlalchemy
from . import operator
from .engine import Engine
from .compiler.native import operator as operator_compiler
from .dsl import field, or_, and_, parse_dsl
import dectate

dectate.commit(Engine)


def validate_condition(query, allowed_operators=None):
    engine = Engine()
    engine.validate_condition(query, allowed_operators)


def compile_condition(method, query, allowed_operators=None):
    engine = Engine()
    return engine.compile_condition(method, query, allowed_operators)
