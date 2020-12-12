import pytest


def test_native_condition():
    from rulez import Engine
#    from rulez import parse_condition, compile_condition
    from rulez import OperatorNotAllowedError
    from rulez import NestedOperationNotAllowedError
    from rulez.operator import Operator

    rule = {
        "operator": "or", "value": [
            {"field": "age", "operator": "<=", "value": 16},
            {"field": "age", "operator": ">=", "value": 21},
            {"field": "age", "operator": "==", "value": 18}
        ]
    }

    engine = Engine()
    parsed = engine.parse_condition(rule)

    assert parsed.operator == 'or'
    assert parsed.value[0].operator == '<='
    assert parsed.value[1].operator == '>='
    assert parsed.value[2].operator == '=='
    assert parsed.value[0].field == 'age'
    assert parsed.value[1].field == 'age'
    assert parsed.value[2].field == 'age'
    assert parsed.value[0].value == 16
    assert parsed.value[1].value == 21
    assert parsed.value[2].value == 18

    f = engine.compile_condition('native', rule)

    assert f({'age': 13}) is True
    assert f({'age': 17}) is False
    assert f({'age': 21}) is True
    assert f({'age': 19}) is False

    f = engine.compile_condition(
        'native', {'field': 'age', 'operator': '>', 'value': 10})
    assert f({'age': 100}) is True
    assert f({'age': 0}) is False

    f = engine.compile_condition('native', {'operator': 'and', 'value': [
        {'field': 'age', 'operator': '>', 'value': 10},
        {'field': 'age', 'operator': '<', 'value': 20}]},
        nestable_operators=['and', 'or'])
    assert f({'age': 1}) is False
    assert f({'age': 40}) is False
    assert f({'age': 15}) is True

    f = engine.compile_condition('native', {'operator': 'in', 'value': [
        'hello', 'world'], 'field': 'word'})
    assert f({'word': 'nope'}) is False
    assert f({'word': 'hello'}) is True

    q = engine.parse_condition({'operator': '==', 'field': 'firstname', 'value': {
        'operator': 'get', 'value': 'lastname'}})
    assert isinstance(q.value, Operator)

    f = engine.compile_condition('native', {
        'operator': '==', 'field': 'firstname',
        'value': {'operator': 'get', 'value': 'lastname'}
    })

    assert f({'firstname': 'A', 'lastname': 'B'}) is False
    assert f({'firstname': 'A', 'lastname': 'A'}) is True

    with pytest.raises(OperatorNotAllowedError):
        engine.compile_condition('native', {'operator': 'and', 'value': [
            {'field': 'age', 'operator': '>', 'value': 10},
            {'field': 'age', 'operator': '<', 'value': 20},
            {'operator': 'and',
                'value': [
                    {'field': 'age', 'operator': '<', 'value': 50},
                    {'field': 'age', 'operator': '>', 'value': 5}
                ]
             }]},
            allowed_operators=['and', '>'])

    with pytest.raises(NestedOperationNotAllowedError):
        engine.compile_condition('native', {'operator': 'and', 'value': [
            {'field': 'age', 'operator': '>', 'value': 10},
            {'field': 'age', 'operator': '<', 'value': 20},
            {'operator': 'and',
                'value': [
                    {'field': 'age', 'operator': '<', 'value': 50},
                    {'field': 'age', 'operator': '>', 'value': 5}
                ]
             }]},
            nestable_operators=['and', 'or'])

def test_native_condition_dt():
    from rulez import Engine
    from datetime import date, datetime

    rule = {"field": "dt", "operator": "<=", "value": '2020-01-01',
            'value_type': 'date'}

    engine = Engine()

    f = engine.compile_condition('native', rule)

    assert f({'dt': date(2019,1,1)}) == True
    assert f({'dt': date(2030,1,1)}) == False


    rule = {"field": "dt", "operator": "<=", "value": '2020-01-01T01:01',
            'value_type': 'datetime'}

    f = engine.compile_condition('native', rule)


    assert f({'dt': datetime(2020,1,1, 0,0)}) == True
    assert f({'dt': datetime(2020,1,1, 2,2)}) == False


