Set end time
------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange()
    print time_range
    time_range.set_end_datetime("2015-03-22T10:10:00+0900")
    print time_range

::

    NaT - NaT
    NaT - 2015-03-22T10:10:00+0900
