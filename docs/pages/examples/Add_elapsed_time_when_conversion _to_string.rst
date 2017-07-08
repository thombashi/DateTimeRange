Add elapsed time when conversion to string
------------------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        time_range.is_output_elapse = True
        time_range

:Output:
    ::

        2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900 (0:10:00)
