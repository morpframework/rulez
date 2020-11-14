"""
Compile into SQLAlchemy condition factory. 

This compiler compiles into a factory function that that accepts
SQLAlchemy ORM model as its parameter, and outputs a SQLAlchemy
condition object for use in ``.filter()`` method in queries. 

Example:

.. code-block:: pycon

   >>> from sqlalchemy.ext.declarative import declarative_base
   >>> import sqlalchemy as sa
   >>> from sqlalchemy.orm import sessionmaker
   >>> import rulez

   >>> Session = sessionmaker()
   >>> Base = declarative_base()
   
   >>> class Object(Base):
   ...    __tablename__ = 'test_objects'
   ...    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
   ...    age = sa.Column(sa.Integer, name='Age')

   >>> engine = sa.create_engine('sqlite://')
   >>> Session.configure(bind=engine)
   >>> Base.metadata.create_all(engine)
   >>> session = Session()

   >>> session.add(Object(age=50))
   >>> session.add(Object(age=18))
   >>> session.add(Object(age=10))
   >>> session.add(Object(age=17))
   >>> session.add(Object(age=19))
   >>> session.flush()

   >>> rule = {
   ...     "operator": "or", "value": [
   ...         {"field": "age", "operator": "<=", "value": 16},
   ...         {"field": "age", "operator": ">=", "value": 21},
   ...         {"field": "age", "operator": "==", "value": 18}
   ...     ]
   ... }

   >>> engine = rulez.Engine()
   >>> cond = engine.compile_condition('sqlalchemy', rule)

   >>> q = session.query(Object).filter(cond(Object))
   >>> sorted([o.age for o in q.all()])
   [10, 18, 50]

"""

from . import operator
from . import action
