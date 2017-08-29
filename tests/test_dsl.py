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


def test_text_dsl():
    from rulez import parse_dsl

    s = parse_dsl('field1==2 or field2<=3')
    assert s == {
        'operator': 'or',
        'value': [
            {
                'field': 'field1',
                'operator': '==',
                'value': 2
            }, {
                'field': 'field2',
                'operator': '<=',
                'value': 3
            }
        ]
    }

    s = parse_dsl('field1 == 2 or field2 <= 3')
    assert s == {
        'operator': 'or',
        'value': [
                {
                    'field': 'field1',
                    'operator': '==',
                    'value': 2
                }, {
                    'field': 'field2',
                    'operator': '<=',
                    'value': 3
                }
        ]
    }

    s = parse_dsl('field3=20 and ( field1==2 or field2<=3 )')
    assert s == {
        'operator': 'and',
        'value': [
            {
                'field': 'field3',
                'operator': '=',
                'value': 20
            },
            {
                'operator': 'or',
                'value': [
                    {
                        'field': 'field1',
                        'operator': '==',
                        'value': 2
                    }, {
                        'field': 'field2',
                        'operator': '<=',
                        'value': 3
                    }
                ]
            }]}

    s = parse_dsl(
        'field2==10 and ( field3=="helllooo world" or field10 = "asd" )')
    assert s == {
        'operator': 'and',
        'value': [
            {
                'field': 'field2',
                'operator': '==',
                'value': 10
            },
            {
                'operator': 'or',
                'value': [
                    {
                        'field': 'field3',
                        'operator': '==',
                        'value': "helllooo world"
                    }, {
                        'field': 'field10',
                        'operator': '=',
                        'value': 'asd'
                    }
                ]
            }]}

    s = parse_dsl(
        'field2==10 and ( field3 in [1,2,3] or field10 = "asd" )')
    assert s == {
        'operator': 'and',
        'value': [
            {
                'field': 'field2',
                'operator': '==',
                'value': 10
            },
            {
                'operator': 'or',
                'value': [
                    {
                        'field': 'field3',
                        'operator': 'in',
                        'value': [1, 2, 3]
                    }, {
                        'field': 'field10',
                        'operator': '=',
                        'value': 'asd'
                    }
                ]
            }]}
