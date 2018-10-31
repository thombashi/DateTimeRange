Make an encompassed time range
------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        x = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
        time_range.encompass(x)

:Output:
    ::

        2015-03-22T10:00:00+0900 - 2015-03-22T10:15:00+0900
