Test whether the time range is set
----------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange()
        print(time_range.is_set())
        time_range.set_time_range("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        print(time_range.is_set())

:Output:
    ::

        False
        True
