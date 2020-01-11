Move the time range
-------------------
:Sample Code:
    .. code:: python

        import datetime
        from datetimerange import DateTimeRange
        value = DateTimeRange("2015-03-22T10:10:00+0900", "2015-03-22T10:20:00+0900")
        print(value + datetime.timedelta(seconds=10 * 60))
        print(value - datetime.timedelta(seconds=10 * 60))

:Output:
    ::

        2015-03-22T10:20:00+0900 - 2015-03-22T10:30:00+0900
        2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900
