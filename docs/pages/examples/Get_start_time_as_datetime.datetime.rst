Get start time as datetime.datetime
-----------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        time_range.start_datetime

:Output:
    ::

        datetime.datetime(2015, 3, 22, 10, 0, tzinfo=tzoffset(None, 32400))
