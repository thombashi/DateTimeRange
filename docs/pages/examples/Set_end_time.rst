Set end time
------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange()
        print(time_range)
        time_range.set_end_datetime("2015-03-22T10:10:00+0900")
        print(time_range)

:Output:
    ::

        NaT - NaT
        NaT - 2015-03-22T10:10:00+0900
