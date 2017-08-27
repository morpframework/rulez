from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
Base = declarative_base()


class Object(Base):

    __tablename__ = 'test_objects'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    age = sa.Column(sa.Integer, name='Age')


def setup():
    engine = sa.create_engine('sqlite://')
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()
    return session


def test_sqlalchemy():
    from rulez import Engine

    session = setup()
    session.add(Object(age=55))
    session.add(Object(age=18))
    session.add(Object(age=10))
    session.add(Object(age=17))
    session.add(Object(age=19))
    session.flush()

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
    c = engine.compile_rulechain('sqlalchemy', rulechain)
    query = c(Object)
    q = session.query(Object, *query)
    res = sorted([{'age': o.age, 'category': c}
                  for o, c in q.all()], key=lambda x: x['age'])
    assert res == [
        {'age': 10, 'category': 'underage'},
        {'age': 17, 'category': 'underage'},
        {'age': 18, 'category': 'adult'},
        {'age': 19, 'category': 'adult'},
        {'age': 55, 'category': 'senior'}]
