Make an subtracted time range
------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-01-22T09:50:00+0900", "2015-01-22T10:00:00+0900")
        x = DateTimeRange("2015-01-22T09:55:00+0900", "2015-01-22T09:56:00+0900")
        time_range.subtract(x)

:Output:
    ::

        [2015-01-22T09:50:00+0900 - 2015-01-22T09:55:00+0900,
         2015-01-22T09:56:00+0900 - 2015-01-22T10:00:00+0900]

