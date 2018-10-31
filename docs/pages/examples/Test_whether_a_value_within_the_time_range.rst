Test whether a value within the time range
------------------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange

        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        print("2015-03-22T10:05:00+0900" in time_range)
        print("2015-03-22T10:15:00+0900" in time_range)

        time_range_smaller = DateTimeRange("2015-03-22T10:03:00+0900", "2015-03-22T10:07:00+0900")
        print(time_range_smaller in time_range)

:Output:
    ::

        True
        False
        True
