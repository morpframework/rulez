from ... import operator as rop
from ...engine import Engine
import operator as op
from jsonpath_ng import parse as jsonpath_parse

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
        if operator.field.startswith('$'):
            match = jsonpath_parse(operator.field).find(data)
            if match:
                sourceval = match[0].value
        else:
            sourceval = data[operator.field]
        return op.eq(sourceval, value)
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.NotEqual)
def ne(engine, method, operator):
    def func(data):
        value = operator.value
        if isinstance(operator.value, rop.Operator):
            value = engine.compile_operator(method, operator.value)(data)
        if operator.field.startswith('$'):
            match = jsonpath_parse(operator.field).find(data)
            if match:
                sourceval = match[0].value
        else:
            sourceval = data[operator.field]
        return op.ne(sourceval, value)
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
        if operator.field.startswith('$'):
            match = jsonpath_parse(operator.field).find(data)
            if match:
                sourceval = match[0].value
        else:
            sourceval = data[operator.field]
        return op.ge(sourceval, value)
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.LessThan)
def lt(engine, method, operator):
    def func(data):
        value = operator.value
        if isinstance(operator.value, rop.Operator):
            value = engine.compile_operator(method, operator.value)(data)
        if operator.field.startswith('$'):
            match = jsonpath_parse(operator.field).find(data)
            if match:
                sourceval = match[0].value
        else:
            sourceval = data[operator.field]
        return op.lt(sourceval, value)
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.GreaterThan)
def gt(engine, method, operator):
    def func(data):
        value = operator.value
        if isinstance(operator.value, rop.Operator):
            value = engine.compile_operator(method, operator.value)(data)
        if operator.field.startswith('$'):
            match = jsonpath_parse(operator.field).find(data)
            if match:
                sourceval = match[0].value
        else:
            sourceval = data[operator.field]
        return op.gt(sourceval, value)
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.In)
def in_(engine, method, operator):
    def func(data):
        value = operator.value
        if operator.field.startswith('$'):
            match = jsonpath_parse(operator.field).find(data)
            if match:
                sourceval = match[0].value
        else:
            sourceval = data[operator.field]
        return sourceval in value
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.Get)
def get(engine, method, operator):
    return lambda data: data[operator.value]


@Engine.operator_compiler(method=METHOD, operator=rop.Like)
def like(engine, method, operator):
    def func(data):
        value = operator.value
        if operator.field.startswith('$'):
            match = jsonpath_parse(operator.field).find(data)
            if match:
                sourceval = match[0].value
        else:
            sourceval = data[operator.field]
        return value in sourceval
    return func
