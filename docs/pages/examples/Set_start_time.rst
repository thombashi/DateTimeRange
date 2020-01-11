Set start time
--------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange()
        print(time_range)
        time_range.set_start_datetime("2015-03-22T10:00:00+0900")
        print(time_range)

:Output:
    ::

        NaT - NaT
        2015-03-22T10:00:00+0900 - NaT
