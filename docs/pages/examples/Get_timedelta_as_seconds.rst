Get timedelta as seconds (from start\_datetime to the end\_datetime)
--------------------------------------------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        time_range.get_timedelta_second()

:Output:
    ::

        600.0
