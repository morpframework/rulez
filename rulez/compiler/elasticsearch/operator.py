from ... import operator as rop
from ...engine import Engine
import operator as op
from elasticsearch_dsl import Q

METHOD = 'elasticsearch'


@Engine.operator_compiler(method=METHOD, operator=rop.And)
def and_(engine, method, operator):
    def func():
        values = []
        for value in operator.value:
            vv = engine.compile_operator(method, value)()
            values += vv['bool']['must']
        return {
            'bool': {
                'must': values
            }
        }
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.Or)
def or_(engine, method, operator):
    def func():
        values = []
        for value in operator.value:
            vv = engine.compile_operator(method, value)()
            values += vv['bool']['must']
        return {
            'bool': {
                'should': values
            }
        }
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.Equal)
def eq(engine, method, operator):
    def func():
        return {'bool': {'must': [{'term': {operator.field: operator.value}}]}}
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.GreaterEqualThan)
def ge(engine, method, operator):
    def func():
        return {'bool': {'must': [
            {'range': {operator.field: {'gte': operator.value}}}]}}
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.LessEqualThan)
def le(engine, method, operator):
    def func():
        return {'bool': {'must': [
            {'range': {operator.field: {'lte': operator.value}}}]}}
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.GreaterThan)
def gt(engine, method, operator):
    def func():
        return {'bool': {'must': [
            {'range': {operator.field: {'gt': operator.value}}}]}}
    return func


@Engine.operator_compiler(method=METHOD, operator=rop.LessThan)
def lt(engine, method, operator):
    def func():
        return {'bool': {'must': [
            {'range': {operator.field: {'lt': operator.value}}}]}}
    return func
