Comparators
============

Comparator operations are declared using JSON with following structure:

.. code-block:: python

   {"field": "<fieldname>", "operator", "<operator>", "value": "<comparison value>"}

Available operators
-------------------

.. automodule:: rulez.operator
   :members:


Comparing contents of 2 fields
------------------------------

We can also compare contents of 2 fields by using comparison operators 

.. code-block:: python

   {
        "field": "<fieldname1>", 
        "operator": "<operator>",
        "value": {
            "operator": "get", 
            "value": "<fieldname2>"
         }
   }
