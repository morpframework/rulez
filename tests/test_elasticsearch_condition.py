from common import elasticsearch, elasticsearch_proc
from pprint import pprint
import time


def test_elasticsearch_condition(elasticsearch):

    from rulez import Engine
    from rulez import OperatorNotAllowedError
    from rulez.operator import Operator

    es = elasticsearch

    for age in [50, 18, 10, 17, 19]:
        es.index(index="test-index", doc_type='people', body={'age': age})

    # give time for es to index
    time.sleep(2)

    engine = Engine()
    rule = {
        "operator": "or", "value": [
            {"field": "age", "operator": "<=", "value": 16},
            {"field": "age", "operator": ">=", "value": 21},
            {"field": "age", "operator": "==", "value": 18}
        ]
    }

    f = engine.compile_condition('elasticsearch', rule)

    r = es.search(index='test-index', doc_type='people', body={
        'query': f()
    })

    data = [o['_source'] for o in r['hits']['hits']]

    assert sorted([d['age'] for d in data]) == [10, 18, 50]

    rule = {
        "operator": "and", "value": [
            {"field": "age", "operator": ">=", "value": 16},
            {"field": "age", "operator": "<=", "value": 21},
        ]
    }

    f = engine.compile_condition('elasticsearch', rule)

    r = es.search(index='test-index', doc_type='people', body={
        'query': f()
    })

    data = [o['_source'] for o in r['hits']['hits']]

    assert sorted([d['age'] for d in data]) == [17, 18, 19]
