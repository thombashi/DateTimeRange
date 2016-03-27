Set time range (set both start and end time)
--------------------------------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange()
    print time_range
    time_range.set_time_range("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    print time_range

::

    NaT - NaT
    2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900
