Validate time inversion
-----------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-03-22T10:10:00+0900", "2015-03-22T10:00:00+0900")
        try:
            time_range.validate_time_inversion()
        except ValueError:
            print("time inversion")

:Output:
    ::

        time inversion
