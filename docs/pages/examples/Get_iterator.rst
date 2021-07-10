Get an iterator
------------------------
:Sample Code 1:
    .. code:: python

        import datetime
        from datetimerange import DateTimeRange

        time_range = DateTimeRange("2015-01-01T00:00:00+0900", "2015-01-04T00:00:00+0900")
        for value in time_range.range(datetime.timedelta(days=1)):
            print(value)

:Output 1:
    ::

        2015-01-01 00:00:00+09:00
        2015-01-02 00:00:00+09:00
        2015-01-03 00:00:00+09:00
        2015-01-04 00:00:00+09:00

:Sample Code 2:
    .. code:: python

        from datetimerange import DateTimeRange
        from dateutil.relativedelta import relativedelta

        time_range = DateTimeRange("2015-01-01T00:00:00+0900", "2016-01-01T00:00:00+0900")
        for value in time_range.range(relativedelta(months=+4)):
            print(value)

:Output 2:
    ::

        2015-01-01 00:00:00+09:00
        2015-05-01 00:00:00+09:00
        2015-09-01 00:00:00+09:00
        2016-01-01 00:00:00+09:00
