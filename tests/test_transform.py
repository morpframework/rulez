from rulez.transformer import Engine as BaseEngine


class Engine(BaseEngine):
    pass


@Engine.register(name='testfunc')
def func(field1, field2, request=None):
    assert field1 == 'hello'
    assert field2 == 'world'
    return '%s %s' % (field1, field2)


def test_engine():
    engine = Engine()
    engine.commit()
    dest = {
        'text': None
    }
    src = {
        'input': 'world'
    }
    dest = engine.remap({
        '$.text': {
            'function': 'testfunc',
            'field1': 'hello',
            'field2': '$.input'
        }
    }, src, dest, request=None)
    assert dest['text'] == 'hello world'
