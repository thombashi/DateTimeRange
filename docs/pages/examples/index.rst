Examples
========
:py:class:`datetime.datetime` instance can be used as an argument value as well as
time-string in the following examples.

.. note::

    Use not the :abbr:`DST(Daylight Saving Time)` offset, but the standard time
    offset when you use datetime string as an argument. :py:class:`~datetimerange.DateTimeRange` class
    automatically calculate daylight saving time. Some examples are below

        .. code:: console

            >>>from datetimerange import DateTimeRange
            >>>time_range = DateTimeRange("2015-03-08T00:00:00-0400", "2015-03-08T12:00:00-0400")
            >>>time_range.timedelta
            datetime.timedelta(0, 39600)  # 11 hours

        .. code:: console

            >>>from datetimerange import DateTimeRange
            >>>time_range = DateTimeRange("2015-11-01T00:00:00-0400", "2015-11-01T12:00:00-0400")
            >>>time_range.timedelta
            datetime.timedelta(0, 46800)  # 13 hours


.. include:: Create_and_convert_to_string.rst
.. include:: Compare_time_ranges.rst
.. include:: Move_the_time_range.rst
.. include:: Change_string_conversion_format.rst
.. include:: Add_elapsed_time_when_conversion _to_string.rst
.. include:: Change_separator_of_the_converted_string.rst
.. include:: Get_start_time_as_datetime.datetime.rst
.. include:: Get_start_time_as_string.rst
.. include:: Get_end_time_as_datetime.datetime.rst
.. include:: Get_end_time_as_string.rst
.. include:: Get_datetime.timedelta.rst
.. include:: Get_timedelta_as_seconds.rst
.. include:: Get_iterator.rst
.. include:: Set_start_time.rst
.. include:: Set_end_time.rst
.. include:: Set_time_range.rst
.. include:: Test_whether_the_time_range_is_set.rst
.. include:: Validate_time_inversion.rst
.. include:: Test_whether_the_time_range_is_valid.rst
.. include:: Test_whether_a_value_within_the_time_range.rst
.. include:: Test_whether_a_value_intersect_the_time_range.rst
.. include:: Make_an_intersected_time_range.rst
.. include:: Make_a_subtracted_time_range.rst
.. include:: Make_an_encompassed_time_range.rst
.. include:: Truncate_time_range.rst
