from ... import operator as rop
from ...engine import Engine
import sqlalchemy as sa

METHOD = 'sqlalchemy'


@Engine.operator_compiler(method=METHOD, operator=rop.And)
def and_(engine, method, operator):
    def func(model):
        c = []
        for v in operator.value:
            c.append(engine.compile_operator(method, v)(model))
        return sa.and_(*c)
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.Or)
def or_(engine, method, operator):
    def func(model):
        c = []
        for v in operator.value:
            c.append(engine.compile_operator(method, v)(model))
        return sa.or_(*c)
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.Equal)
def eq(engine, method, operator):
    def func(model):
        attr = getattr(model, operator.field)
        return attr == operator.value
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.NotEqual)
def ne(engine, method, operator):
    def func(model):
        attr = getattr(model, operator.field)
        return attr != operator.value
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.LessEqualThan)
def le(engine, method, operator):
    def func(model):
        value = operator.value
        if isinstance(operator.value, rop.Operator):
            value = engine.compile_operator(method, operator.value)(model)
        attr = getattr(model, operator.field)
        return attr <= value
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.GreaterEqualThan)
def ge(engine, method, operator):
    def func(model):
        value = operator.value
        if isinstance(operator.value, rop.Operator):
            value = engine.compile_operator(method, operator.value)(model)
        attr = getattr(model, operator.field)
        return attr >= value
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.LessThan)
def lt(engine, method, operator):
    def func(model):
        value = operator.value
        if isinstance(operator.value, rop.Operator):
            value = engine.compile_operator(method, operator.value)(model)
        attr = getattr(model, operator.field)
        return attr < value
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.GreaterThan)
def gt(engine, method, operator):
    def func(model):
        value = operator.value
        if isinstance(operator.value, rop.Operator):
            value = engine.compile_operator(method, operator.value)(model)
        attr = getattr(model, operator.field)
        return attr > value
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.In)
def in_(engine, method, operator):
    def func(model):
        attr = getattr(model, operator.field)
        return attr.in_(operator.value)
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.Like)
def like(engine, method, operator):
    def func(model):
        attr = getattr(model, operator.field)
        return attr.ilike('%%%s%%' % operator.value)
    return func
