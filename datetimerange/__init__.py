# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''

import datetime

import dateutil.parser


class DateTimeRange(object):
    """
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        time_range

    .. parsed-literal::

        2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900
    """

    NOT_A_TIME_STR = "NaT"

    def __init__(
            self, start_datetime=None, end_datetime=None,
            start_time_format="%Y-%m-%dT%H:%M:%S%z",
            end_time_format="%Y-%m-%dT%H:%M:%S%z"):

        self.set_time_range(start_datetime, end_datetime)

        self.start_time_format = start_time_format
        self.end_time_format = end_time_format

        self.is_output_elapse = False
        self.separator = " - "

    def __repr__(self):
        text_list = [
            self.get_start_time_str(),
            self.get_end_time_str(),
        ]

        if self.is_output_elapse:
            suffix = " (%s)" % (self.end_datetime - self.start_datetime)
        else:
            suffix = ""

        return self.separator.join(text_list) + suffix

    def __eq__(self, other):
        return all([
            self.start_datetime == other.start_datetime,
            self.end_datetime == other.end_datetime,
        ])

    def __ne__(self, other):
        return any([
            self.start_datetime != other.start_datetime,
            self.end_datetime != other.end_datetime,
        ])

    def __add__(self, other):
        return DateTimeRange(
            self.start_datetime + other, self.end_datetime + other)

    def __iadd__(self, other):
        self.set_start_datetime(self.start_datetime + other)
        self.set_end_datetime(self.end_datetime + other)

        return self

    def __sub__(self, other):
        return DateTimeRange(
            self.start_datetime - other, self.end_datetime - other)

    def __isub__(self, other):
        self.set_start_datetime(self.start_datetime - other)
        self.set_end_datetime(self.end_datetime - other)

        return self

    def __contains__(self, x):
        """
        :param datetime.datetime/str x:
            datetime to compare.
            Parse and convert to datetime if the value type is string.
        :return: ``True`` if the ``x`` is within the time range
        :rtype: bool
        :raises: See also
            :py:func:`validate_time_inversion() <datetimerange.DateTimeRange.validate_time_inversion>`

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            print "2015-03-22T10:05:00+0900" in time_range
            print "2015-03-22T10:15:00+0900" in time_range

        .. parsed-literal::

            True
            False
        """

        self.validate_time_inversion()

        try:
            value = dateutil.parser.parse(x)
        except AttributeError:
            value = x

        return self.start_datetime <= value <= self.end_datetime

    @property
    def start_datetime(self):
        """
        :return: Start time of the time range
        :rtype: datetime.datetime

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            time_range.start_datetime

        .. parsed-literal::

            datetime.datetime(2015, 3, 22, 10, 0, tzinfo=tzoffset(None, 32400))
        """

        return self.__start_datetime

    @property
    def end_datetime(self):
        """
        :return: End time of the time range
        :rtype: datetime.datetime

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            time_range.end_datetime

        .. parsed-literal::

            datetime.datetime(2015, 3, 22, 10, 10, tzinfo=tzoffset(None, 32400))
        """

        return self.__end_datetime

    @property
    def timedelta(self):
        """
        :return: (end_time - start_time) as datetime.timedelta
        :rtype: datetime.timedelta

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            time_range.timedelta

        .. parsed-literal::

            datetime.timedelta(0, 600)
        """

        return self.end_datetime - self.start_datetime

    def is_set(self):
        """
        :return: True if start_datetime and end_datetime is not None
        :rtype: bool

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange()
            print time_range.is_set()
            time_range.set_time_range("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            print time_range.is_set()

        .. parsed-literal::

            False
            True
        """

        return all([
            self.start_datetime is not None,
            self.end_datetime is not None,
        ])

    def validate_time_inversion(self):
        """
        Check time inversion of the time range.

        :raises ValueError: If ``start_time`` is bigger than ``end_time``
        :raises TypeError:
            Any one of ``start_time`` and ``end_time``,
            or both, is not a appropriate datetime value.


        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange("2015-03-22T10:10:00+0900", "2015-03-22T10:00:00+0900")
            try:
                time_range.validate_time_inversion()
            except ValueError:
                print "time inversion"

        .. parsed-literal::

            time inversion
        """

        if not self.is_set():
            # for python2/3 compatibility
            raise TypeError

        if self.start_datetime > self.end_datetime:
            message = "time inversion found: %s > %s" % (
                str(self.start_datetime), str(self.end_datetime))
            raise ValueError(message)

    def is_valid_timerange(self):
        """
        :return: ``True`` if the timerange is not null and not time inversion.
        :rtype: bool

        See also
            :py:func:`is_set() <datetimerange.DateTimeRange.is_set>`
            :py:func:`validate_time_inversion() <datetimerange.DateTimeRange.validate_time_inversion>`

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange()
            print time_range.is_valid_timerange()
            time_range.set_time_range("2015-03-22T10:20:00+0900", "2015-03-22T10:10:00+0900")
            print time_range.is_valid_timerange()
            time_range.set_time_range("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            print time_range.is_valid_timerange()

        .. parsed-literal::

            False
            False
            True
        """

        try:
            self.validate_time_inversion()
        except (TypeError, ValueError):
            return False

        return self.is_set()

    def is_intersection(self, x):
        """
        :param datetime.datetime x: datetime to compare
        :return: ``True`` if intersect with ``x``
        :rtype: bool
        :raises: See also
            :py:func:`intersection() <datetimerange.DateTimeRange.intersection>`

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            x = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
            time_range.is_intersection(x)

        .. parsed-literal::

            True
        """

        import copy

        dtr = copy.deepcopy(self)
        dtr.intersection(x)

        return dtr.is_set()

    def get_start_time_str(self):
        """
        :return:
            ``start_datetime`` as string formatted with ``start_time_format``.
            Return `'NaT'` if invalid datetime or format.
        :rtype: str

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            print time_range.get_start_time_str()
            time_range.start_time_format = "%Y/%m/%d %H:%M:%S"
            print time_range.get_start_time_str()

        .. parsed-literal::

            2015-03-22T10:00:00+0900
            2015/03/22 10:00:00
        """

        try:
            return self.start_datetime.strftime(self.start_time_format)
        except AttributeError:
            return self.NOT_A_TIME_STR

    def get_end_time_str(self):
        """
        :return:
            ``end_datetime`` as string formatted with ``end_time_format``.
            Return `'NaT'` if invalid datetime or format.
        :rtype: str

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            print time_range.get_end_time_str()
            time_range.end_time_format = "%Y/%m/%d %H:%M:%S"
            print time_range.get_end_time_str()

        .. parsed-literal::

            2015-03-22T10:10:00+0900
            2015/03/22 10:10:00
        """

        try:
            return self.end_datetime.strftime(self.end_time_format)
        except AttributeError:
            return self.NOT_A_TIME_STR

    def get_timedelta_second(self):
        """
        :return: (end_time - start_time) as seconds
        :rtype: float

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            time_range.get_timedelta_second()

        .. parsed-literal::

            600.0
        """

        dt = self.timedelta

        return (
            dt.days * 60 ** 2 * 24 +
            float(dt.seconds) + float(dt.microseconds / (1000.0 ** 2)))

    def set_start_datetime(self, value):
        """
        Set the start time of the time range.

        :param datetime.datetime/str value:
            Value to set.
            Parse and convert to datetime if the value type is string.
            Parser engine of datetime string is the dateutil.parser.

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange()
            print time_range
            time_range.set_start_datetime("2015-03-22T10:00:00+0900")
            print time_range

        .. parsed-literal::

            NaT - NaT
            2015-03-22T10:00:00+0900 - NaT
        """

        if is_datetime(value):
            self.__start_datetime = value
            return

        try:
            dt = dateutil.parser.parse(value)
        except AttributeError:
            dt = None

        self.__start_datetime = dt

    def set_end_datetime(self, value):
        """
        Set the end time of the time range.

        :param datetime.datetime/str value:
            Value to set.
            Parse and convert to datetime if the value type is string.
            Parser engine of datetime string is the dateutil.parser.

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange()
            print time_range
            time_range.set_end_datetime("2015-03-22T10:10:00+0900")
            print time_range

        .. parsed-literal::

            NaT - NaT
            NaT - 2015-03-22T10:10:00+0900
        """

        if is_datetime(value):
            self.__end_datetime = value
            return

        try:
            dt = dateutil.parser.parse(value)
        except AttributeError:
            dt = None

        self.__end_datetime = dt

    def set_time_range(self, start, end):
        """
        :param datetime.datetime/str start:
        :param datetime.datetime/str end:

        See also
            :py:func:`set_start_datetime() <datetimerange.DateTimeRange.set_start_datetime>`
            :py:func:`set_end_datetime() <datetimerange.DateTimeRange.set_end_datetime>`

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange()
            print time_range
            time_range.set_time_range("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            print time_range

        .. parsed-literal::

            NaT - NaT
            2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900
        """

        self.set_start_datetime(start)
        self.set_end_datetime(end)

    def intersection(self, x):
        """
        Newly set a time range that overlaps the input and the current time range.

        :param DateTimeRange x:

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            x = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
            time_range.intersection(x)
            time_range

        .. parsed-literal::

            2015-03-22T10:05:00+0900 - 2015-03-22T10:10:00+0900
        """

        self.validate_time_inversion()
        x.validate_time_inversion()

        if any([
            x.start_datetime in self,
            self.start_datetime in x,
        ]):
            self.set_start_datetime(max(self.start_datetime, x.start_datetime))
            self.set_end_datetime(min(self.end_datetime, x.end_datetime))
        else:
            self.set_start_datetime(None)
            self.set_end_datetime(None)

    def encompass(self, x):
        """
        Newly set a time range that encompasses the input and the current time range.

        :param DateTimeRange x:

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            x = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
            time_range.encompass(x)
            time_range

        .. parsed-literal::

            2015-03-22T10:00:00+0900 - 2015-03-22T10:15:00+0900        
        """

        self.validate_time_inversion()
        x.validate_time_inversion()

        self.set_start_datetime(min(self.start_datetime, x.start_datetime))
        self.set_end_datetime(max(self.end_datetime, x.end_datetime))

    def truncate(self, percentage):
        """
        Truncate ``percentage`` / 2 [%] of whole time from first and last time.

        :param float percentage: Percentage of truncate

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            time_range.is_output_elapse = True
            print time_range
            time_range.truncate(10)
            print time_range

        .. parsed-literal::

            2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900 (0:10:00)
            2015-03-22T10:00:30+0900 - 2015-03-22T10:09:30+0900 (0:09:00)
        """

        self.validate_time_inversion()

        if percentage < 0:
            raise ValueError(
                "discard_percent must be greater or equal to zero: " +
                str(percentage))

        if percentage == 0:
            return

        discard_time = self.timedelta // int(100) * \
            int(percentage / 2.0)

        self.__start_datetime += discard_time
        self.__end_datetime -= discard_time


def is_datetime(value):
    return value is not None and isinstance(value, datetime.datetime)
