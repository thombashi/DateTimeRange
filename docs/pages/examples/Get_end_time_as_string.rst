Get end time as string (formatted with ``end_time_format``)
-----------------------------------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        print(time_range.get_end_time_str())
        time_range.end_time_format = "%Y/%m/%d %H:%M:%S"
        print(time_range.get_end_time_str())

:Output:
    ::

        2015-03-22T10:10:00+0900
        2015/03/22 10:10:00
