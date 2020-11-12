===================
Syntax Sugar / DSL
===================

Rulez provide several syntax sugar to help with constructing comparison operations.

Pythonic Operation
===================

You can easily create a comparison operation using ``rulez.field``. Eg:

.. code-block:: pycon

   >>> import rulez

   >>> rulez.field['field1']
   ... { 'operator': 'get', 'value': 'field1' }

   >>> rulez.field['field1'] == 'myvalue'
   ... { 'field': 'field1', 'operator': '==', 'value': 'myvalue' }

   >>> rulez.field['field1'] == rulez.field['field2']
   ... { 'field': 'field1', 'operator': '==', 
   ...   'value': {
   ...         'operator': 'get', 
   ...         'value': 'field2' }}

   >>> rulez.field['field1'] & rulez.field['field2']
   ... {'operator': 'and', 
   ...  'value': [
   ...      {'operator': 'get', 'value': 'field1'}, 
   ...      {'operator': 'get', 'value': 'field2'}]}

   >>> rulez.field['field1'] | rulez.field['field2']
   ... {'operator': 'or', 
   ...  'value': [
   ...      {'operator': 'get', 'value': 'field1'}, 
   ...      {'operator': 'get', 'value': 'field2'}]}

Boolean DSL Statement
======================

Comparison operation can also be created from string using ``rulez.parse_dsl``

.. code-block:: pycon

   >>> import rulez
   >>> rulez.parse_dsl("field1 == field2")
   ... {'field': 'field1', 'operator': '==', 
   ...  'value': {'operator': 'get', 
   ...            'value': 'field2'}}

   >>> rulez.parse_dsl("field1 == 'hello world'")
   ... {'field': 'field1', 'operator': '==', 
   ...  'value': 'hello world'}

   >>> rulez.parse_dsl("(field1 == field2) or (field3 == 'value1')")
   ... {'operator': 'or', 
   ...  'value': [{'field': 'field1', 'operator': '==', 
   ...             'value': {'operator': 'get', 'value': 'field2'}}, 
   ...            {'field': 'field3', 'operator': '==', 
   ...              'value': 'value1'}]}

   >>> rulez.parse_dsl('field1 in ["a","b","c"]')
   ... {'field': 'field1', 'operator': 'in', 'value': ['a', 'b', 'c']}

   >>> rulez.parse_dsl('field1 in in [1.0,2.0,3.0]')
   ... {'field': 'field1', 'operator': 'in', 'value': [1.0, 2.0, 3.0]}

