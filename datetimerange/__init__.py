# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import division
from __future__ import unicode_literals
import datetime

import dataproperty as dp
import dateutil.parser
import dateutil.relativedelta as rdelta


class DateTimeRange(object):
    """
    The class that represents the time range.

    :param datetime.datetime/str start: |param_start_datetime|
    :param datetime.datetime/str end: |param_end_datetime|

    :Examples:

        .. code:: python

            from datetimerange import DateTimeRange
            time_range = DateTimeRange(
                "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
            time_range

        .. parsed-literal::

            2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900

    .. py:attribute:: start_time_format

        Conversion format string for :py:attr:`.start_datetime`.

        .. seealso:: :py:meth:`.get_start_time_str`

    .. py:attribute:: end_time_format

        Conversion format string for :py:attr:`.end_datetime`.

        .. seealso:: :py:meth:`.get_end_time_str`
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
            suffix = " ({})".format(self.end_datetime - self.start_datetime)
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
            datetime or datetimerange to compare.
            Parse and convert to datetime if the value type is ``str``.
        :return: |True| if the ``x`` is within the time range
        :rtype: bool

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                print "2015-03-22T10:05:00+0900" in time_range
                print "2015-03-22T10:15:00+0900" in time_range
                time_range_smaller = DateTimeRange(
                    "2015-03-22T10:03:00+0900", "2015-03-22T10:07:00+0900")
                print time_range_smaller in time_range

            .. parsed-literal::

                True
                False

        .. seealso::

            :py:meth:`.validate_time_inversion`
        """

        self.validate_time_inversion()

        if isinstance(x, DateTimeRange):
            return x.start_datetime >= self.start_datetime and x.end_datetime <= self.end_datetime

        try:
            value = dateutil.parser.parse(x)
        except (TypeError, AttributeError):
            value = x

        return self.start_datetime <= value <= self.end_datetime

    @property
    def start_datetime(self):
        """
        :return: Start time of the time range.
        :rtype: datetime.datetime

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                time_range.start_datetime

            .. parsed-literal::

                datetime.datetime(2015, 3, 22, 10, 0, tzinfo=tzoffset(None, 32400))
        """

        return self.__start_datetime

    @property
    def end_datetime(self):
        """
        :return: End time of the time range.
        :rtype: datetime.datetime

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                time_range.end_datetime

            .. parsed-literal::

                datetime.datetime(2015, 3, 22, 10, 10, tzinfo=tzoffset(None, 32400))
        """

        return self.__end_datetime

    @property
    def timedelta(self):
        """
        :return:
            (|attr_end_datetime| - |attr_start_datetime|) as |timedelta|
        :rtype: datetime.timedelta

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                time_range.timedelta

            .. parsed-literal::

                datetime.timedelta(0, 600)
        """

        return self.end_datetime - self.start_datetime

    def is_set(self):
        """
        :return:
            |True| if both |attr_start_datetime| and
            |attr_end_datetime| were not |None|.
        :rtype: bool

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange()
                print time_range.is_set()
                time_range.set_time_range(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
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

        :raises ValueError:
            If |attr_start_datetime| is
            bigger than |attr_end_datetime|.
        :raises TypeError:
            Any one of |attr_start_datetime| and |attr_end_datetime|,
            or both is inappropriate datetime value.

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange(
                    "2015-03-22T10:10:00+0900", "2015-03-22T10:00:00+0900")
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
            message = "time inversion found: {:s} > {:s}".format(
                str(self.start_datetime), str(self.end_datetime))
            raise ValueError(message)

    def is_valid_timerange(self):
        """
        :return:
            |True| if the time range is
            not null and not time inversion.
        :rtype: bool

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange()
                print time_range.is_valid_timerange()
                time_range.set_time_range(
                    "2015-03-22T10:20:00+0900", "2015-03-22T10:10:00+0900")
                print time_range.is_valid_timerange()
                time_range.set_time_range(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                print time_range.is_valid_timerange()

            .. parsed-literal::

                False
                False
                True

        .. seealso::

            :py:meth:`.is_set`
            :py:meth:`.validate_time_inversion`
        """

        try:
            self.validate_time_inversion()
        except (TypeError, ValueError):
            return False

        return self.is_set()

    def is_intersection(self, x):
        """
        :param DateTimeRange x: Value to compare
        :return: |True| if intersect with ``x``
        :rtype: bool

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                x = DateTimeRange(
                    "2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
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
            |attr_start_datetime| as |str| formatted with
            |attr_start_time_format|.
            Return |NaT| if invalid datetime or format.
        :rtype: str

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
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
            |attr_end_datetime| as a |str| formatted with
            |attr_end_time_format|.
            Return |NaT| if invalid datetime or format.
        :rtype: str

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
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
        :return: (|attr_end_datetime| - |attr_start_datetime|) as seconds
        :rtype: float

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                time_range.get_timedelta_second()

            .. parsed-literal::

                600.0
        """

        return self.__get_timedelta_sec(self.timedelta)

    def set_start_datetime(self, value):
        """
        Set the start time of the time range.

        :param datetime.datetime/str value: |param_start_datetime|

        :Examples:

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

        data_prop = dp.DataProperty(
            value, strict_type_mapping=dp.NOT_STRICT_TYPE_MAPPING)
        self.__validate_value(data_prop)
        self.__start_datetime = data_prop.data

    def set_end_datetime(self, value):
        """
        Set the end time of the time range.

        :param datetime.datetime/str value: |param_end_datetime|

        :Examples:

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

        data_prop = dp.DataProperty(
            value, strict_type_mapping=dp.NOT_STRICT_TYPE_MAPPING)
        self.__validate_value(data_prop)
        self.__end_datetime = data_prop.data

    def set_time_range(self, start, end):
        """
        :param datetime.datetime/str start: |param_start_datetime|
        :param datetime.datetime/str end: |param_end_datetime|

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange()
                print time_range
                time_range.set_time_range(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                print time_range

            .. parsed-literal::

                NaT - NaT
                2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900
        """

        self.set_start_datetime(start)
        self.set_end_datetime(end)

    @staticmethod
    def __compare_relativedelta(lhs, rhs):
        if lhs.years < rhs.years:
            return -1
        if lhs.years > rhs.years:
            return 1

        if lhs.months < rhs.months:
            return -1
        if lhs.months > rhs.months:
            return 1

        if lhs.days < rhs.days:
            return -1
        if lhs.days > rhs.days:
            return 1

        if lhs.hours < rhs.hours:
            return -1
        if lhs.hours > rhs.hours:
            return 1

        if lhs.minutes < rhs.minutes:
            return -1
        if lhs.minutes > rhs.minutes:
            return 1

        if lhs.seconds < rhs.seconds:
            return -1
        if lhs.seconds > rhs.seconds:
            return 1

        if lhs.microseconds < rhs.microseconds:
            return -1
        if lhs.microseconds > rhs.microseconds:
            return 1

        return 0

    def __compare_timedelta(self, lhs, seconds):
        try:
            rhs = datetime.timedelta(seconds=seconds)

            if lhs < rhs:
                return -1
            if lhs > rhs:
                return 1

            return 0
        except TypeError:
            return self.__compare_relativedelta(
                lhs.normalized(), rdelta.relativedelta(seconds=seconds))

    def range(self, step):
        """
        Return an iterator object.

        :param datetime.timedelta/dateutil.relativedelta.relativedelta step:
            Step of iteration.
        :return: iterator
        :rtype: iterator

        :Examples:

            .. code:: python

                import datetime
                from datetimerange import DateTimeRange

                time_range = DateTimeRange(
                    "2015-01-01T00:00:00+0900", "2015-01-04T00:00:00+0900")
                for value in time_range.range(datetime.timedelta(days=1)):
                    print value

            .. parsed-literal::

                2015-01-01 00:00:00+09:00
                2015-01-02 00:00:00+09:00
                2015-01-03 00:00:00+09:00
                2015-01-04 00:00:00+09:00
        """

        if self.__compare_timedelta(step, 0) == 0:
            raise ValueError("step must be not zero")

        is_inversion = False
        try:
            self.validate_time_inversion()
        except ValueError:
            is_inversion = True

        if not is_inversion:
            if self.__compare_timedelta(step, seconds=0) < 0:
                raise ValueError(
                    "invalid step: expect greater than 0, actual={}".format(
                        step))
        else:
            if self.__compare_timedelta(step, seconds=0) > 0:
                raise ValueError(
                    "invalid step: expect less than 0, actual={}".format(
                        step))

        current_datetime = self.start_datetime
        while current_datetime <= self.end_datetime:
            yield current_datetime
            current_datetime = current_datetime + step

    def intersection(self, x):
        """
        Newly set a time range that overlaps
        the input and the current time range.

        :param DateTimeRange x:
            Value to compute intersection with the current time range.

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                x = DateTimeRange(
                    "2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
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
        Newly set a time range that encompasses
        the input and the current time range.

        :param DateTimeRange x:
            Value to compute encompass with the current time range.

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                x = DateTimeRange(
                    "2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
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

        :param float percentage: Percentage of truncate.

        :Examples:

            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
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

        discard_time = self.timedelta // int(100) * int(percentage / 2)

        self.__start_datetime += discard_time
        self.__end_datetime -= discard_time

    def __validate_value(self, data_prop):
        if data_prop.typecode not in [dp.Typecode.DATETIME, dp.Typecode.NONE]:
            raise ValueError("invalid datetime value: {}".format(data_prop))

    @staticmethod
    def __get_timedelta_sec(dt):
        return int(
            dt.days * 60 ** 2 * 24 + float(dt.seconds) +
            dt.microseconds / (1000.0 ** 2))
