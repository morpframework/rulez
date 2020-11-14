===================
Syntax Sugar / DSL
===================

Rulez provide several syntax sugar to help with constructing comparison operations.

Pythonic Operation
===================

You can easily create a comparison operation using ``rulez.field``. Eg:

.. automethod:: rulez.dsl.FieldGetter.__call__

.. automethod:: rulez.dsl.FieldGetter.__getitem__

Boolean DSL Statement
======================

Comparison operation can also be created from string using ``rulez.parse_dsl``

.. autofunction:: rulez.parse_dsl