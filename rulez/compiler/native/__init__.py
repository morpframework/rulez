"""
Compile into Python function

This compiler compiles ruleset into an executable Python function.

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
   >>> f = engine.compile_condition('native', rule)
   >>> f({'age': 13})
   True

"""

from . import operator
from . import action
