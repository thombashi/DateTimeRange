Compare time ranges
-------------------

.. code:: python

    from datetimerange import DateTimeRange
    lhs = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    rhs = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    print "lhs == rhs: ", lhs == rhs
    print "lhs != rhs: ", lhs != rhs

::

    lhs == rhs:  True
    lhs != rhs:  False
