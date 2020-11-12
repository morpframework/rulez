===========
Quickstart
===========

Installation
=============

::

  pip install rulez

Defining & Compiling Comparators
=================================

``rulez`` provide a way to compile comparators from JSON based 
ruleset.

.. code-block:: python

   from rulez import Engine
   from rulez import OperatorNotAllowedError
   from rulez import NestedOperationNotAllowedError
   from rulez.operator import Operator
 
   rule = {
       "operator": "or", "value": [
           {"field": "age", "operator": "<=", "value": 16},
           {"field": "age", "operator": ">=", "value": 21},
           {"field": "age", "operator": "==", "value": 18}
       ]
   }
 
   engine = Engine()
 
   f = engine.compile_condition('native', rule)
 
   assert f({'age': 13}) is True
   assert f({'age': 17}) is False
   assert f({'age': 21}) is True
   assert f({'age': 19}) is False
 

Available Compilation Method
-----------------------------

* ``native`` - compile to python condition
* ``sqlalchemy`` - compile to a factory function to generate sqlalchemy filter
* ``elasticsearch`` - compile a factory function that generate elasticsearch filter


Defining & Compiling Rule Chain
===============================

Besides compiling conditionals, ``rulez`` also provide a way to compile if-elif-else
ruleset.

.. code-block:: python

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


Available Compilation Method
-----------------------------

* ``native`` - compile to python rulechain
* ``sqlalchemy`` - compile to a factory function to generate sqlalchemy query
  that adds a new result column

