Change string conversion format
-------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        time_range.start_time_format = "%Y/%m/%d"
        time_range.end_time_format = "%Y/%m/%dT%H:%M:%S%z"
        time_range

:Output:
    ::

        2015/03/22 - 2015/03/22T10:10:00+0900
