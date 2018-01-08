from ... import operator as rop
from ...engine import Engine
import operator as op

METHOD = 'native'


@Engine.operator_compiler(method=METHOD, operator=rop.And)
def and_(engine, method, operator):
    def func(data):
        a = engine.compile_operator(method, operator.value[0])(data)
        for b in operator.value[1:]:
            a = op.__and__(a, engine.compile_operator(method, b)(data))
        return a
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.Or)
def or_(engine, method, operator):
    def func(data):
        a = engine.compile_operator(method, operator.value[0])(data)
        for b in operator.value[1:]:
            a = op.__or__(a, engine.compile_operator(method, b)(data))
        return a
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.Equal)
def eq(engine, method, operator):
    def func(data):
        value = operator.value
        if isinstance(operator.value, rop.Operator):
            value = engine.compile_operator(method, operator.value)(data)
        return op.eq(data[operator.field], value)
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.NotEqual)
def ne(engine, method, operator):
    def func(data):
        value = operator.value
        if isinstance(operator.value, rop.Operator):
            value = engine.compile_operator(method, operator.value)(data)
        return op.ne(data[operator.field], value)
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.LessEqualThan)
def le(engine, method, operator):
    def func(data):
        value = operator.value
        if isinstance(operator.value, rop.Operator):
            value = engine.compile_operator(method, operator.value)(data)
        return op.le(data[operator.field], value)
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.GreaterEqualThan)
def ge(engine, method, operator):
    def func(data):
        value = operator.value
        if isinstance(operator.value, rop.Operator):
            value = engine.compile_operator(method, operator.value)(data)
        return op.ge(data[operator.field], value)
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.LessThan)
def lt(engine, method, operator):
    def func(data):
        value = operator.value
        if isinstance(operator.value, rop.Operator):
            value = engine.compile_operator(method, operator.value)(data)
        return op.lt(data[operator.field], value)
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.GreaterThan)
def gt(engine, method, operator):
    def func(data):
        value = operator.value
        if isinstance(operator.value, rop.Operator):
            value = engine.compile_operator(method, operator.value)(data)
        return op.gt(data[operator.field], value)
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.In)
def in_(engine, method, operator):
    return lambda data: data[operator.field] in operator.value


@Engine.operator_compiler(method=METHOD, operator=rop.Get)
def get(engine, method, operator):
    return lambda data: data[operator.value]


@Engine.operator_compiler(method=METHOD, operator=rop.Like)
def like(engine, method, operator):
    return lambda data: operator.value in data[operator.field]
