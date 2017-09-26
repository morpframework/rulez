import os
import pytest
import shutil
import mirakuru
from elasticsearch import Elasticsearch


@pytest.fixture(scope='session')
def elasticsearch_proc(request):
    port = 9085
    home_dir = '/tmp/elasticsearch_%s' % port
    os.environ['ES_HOME'] = home_dir
    command = [
        os.environ['ELASTICSEARCH_EXECUTABLE'],
        '-p', '/tmp/elasticsearch.%s.pid' % port,
        '-E', 'http.port=%s' % port,
        '-E', 'default.path.logs=/tmp/elasticsearch_%s_logs' % port,
        '-E', 'cluster.name=elasticsearch_cluster_%s' % port,
        '-E', "network.publish_host='127.0.0.1'",
        '-E', 'index.store.type=mmapfs'
    ]
    es_proc = mirakuru.HTTPExecutor(
        command, shell=True, url='http://127.0.0.1:%s' % port)
    es_proc.start()

    def finalize_elasticsearch():
        es_proc.stop()
        if os.path.exists(home_dir):
            shutil.rmtree(home_dir)

    request.addfinalizer(finalize_elasticsearch)
    return es_proc


@pytest.fixture(scope='session')
def elasticsearch(request):
    process = request.getfixturevalue('elasticsearch_proc')
    if not process.running():
        process.start()

    hosts = "%s:%s" % (process.host, process.port)

    client = Elasticsearch(hosts=hosts)

    def drop_indexes():
        client.indices.delete(index='*')

    request.addfinalizer(drop_indexes)

    return client
