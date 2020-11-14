"""
Compile into ElasticSearch condition factory. 

This compiler compiles ruleset into a factory function 
that returns a json dictionary for use in elasticsearch
``'query'`` body.

Example:

.. code-block:: pycon

   >>> import rulez 
   >>> engine = rulez.Engine()
   >>> rule = {
   ...     "operator": "or", "value": [
   ...         {"field": "age", "operator": "<=", "value": 16},
   ...         {"field": "age", "operator": ">=", "value": 21},
   ...         {"field": "age", "operator": "==", "value": 18}
   ...     ]
   ... }

   >>> f = engine.compile_condition('elasticsearch', rule)
   >>> f()
   {'bool': {'minimum_should_match': 1,
             'should': [{'range': {'age': {'lte': 16}}},
                        {'range': {'age': {'gte': 21}}},
                        {'term': {'age': 18}}]}}
                        
"""

from . import operator
