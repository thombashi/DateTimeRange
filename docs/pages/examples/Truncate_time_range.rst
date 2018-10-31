Truncate time range
-------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange

        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        time_range.is_output_elapse = True
        print("before truncate: ", time_range)

        time_range.truncate(10)
        print("after truncate:  ", time_range)

:Output:
    ::

        before truncate:  2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900 (0:10:00)
        after truncate:   2015-03-22T10:00:30+0900 - 2015-03-22T10:09:30+0900 (0:09:00)
