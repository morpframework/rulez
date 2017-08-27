def test_dsl():
    from rulez import field, or_, and_

    assert (field['field1'] == 'hello') == {
        'field': 'field1',
        'operator': '==',
        'value': 'hello'
    }

    assert (field['field1'].in_(['val1', 'val2'])) == {
        'field': 'field1',
        'operator': 'in',
        'value': ['val1', 'val2']
    }

    assert or_(field['field1'] == 2, field['field2'] <= 3) == {
        'operator': 'or',
        'value': [
            {'field': 'field1',
             'operator': '==',
             'value': 2},
            {'field': 'field2',
             'operator': '<=',
             'value': 3},
        ]
    }
