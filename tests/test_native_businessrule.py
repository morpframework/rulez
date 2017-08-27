
def test_native_businessrule():
    from rulez import Engine

    rulechain = [
        {'condition': {
            'field': 'age',
            'operator': '<',
            'value': 18},
         'actions': [{
             'action': 'set',
             'parameter': {
                 'field': 'category',
                 'value': 'underage'
             }
         }]},
        {'condition': {
            'field': 'age',
            'operator': '>',
            'value': 50},
         'actions': [{
             'action': 'set',
             'parameter': {
                 'field': 'category',
                 'value': 'senior'}}]},
        {'actions': [{
            'action': 'set',
            'parameter': {
                'field': 'category',
                'value': 'adult'}}]}
    ]

    engine = Engine()
    c = engine.compile_rulechain('native', rulechain)

    assert c({'age': 10}) == {'age': 10, 'category': 'underage'}
    assert c({'age': 18}) == {'age': 18, 'category': 'adult'}
    assert c({'age': 55}) == {'age': 55, 'category': 'senior'}
