"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import datetime
import re
from typing import List, Optional, Union

import dateutil.parser
import dateutil.relativedelta as rdelta
import typepy

from .__version__ import __author__, __copyright__, __email__, __license__, __version__


class DateTimeRange:
    """
    A class that represents a range of datetime.

    :param datetime.datetime/str start_datetime: |param_start_datetime|
    :param datetime.datetime/str end_datetime: |param_end_datetime|

    :Examples:
        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")

        :Output:
            .. parsed-literal::

                2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900

    .. py:attribute:: start_time_format
        :type: str
        :value: "%Y-%m-%dT%H:%M:%S%z"

        Conversion format string for :py:attr:`.start_datetime`.

        .. seealso:: :py:meth:`.get_start_time_str`

    .. py:attribute:: end_time_format
        :type: str
        :value: "%Y-%m-%dT%H:%M:%S%z"

        Conversion format string for :py:attr:`.end_datetime`.

        .. seealso:: :py:meth:`.get_end_time_str`
    """

    NOT_A_TIME_STR = "NaT"

    def __init__(
        self,
        start_datetime=None,
        end_datetime=None,
        start_time_format="%Y-%m-%dT%H:%M:%S%z",
        end_time_format="%Y-%m-%dT%H:%M:%S%z",
    ):
        self.set_time_range(start_datetime, end_datetime)

        self.start_time_format = start_time_format
        self.end_time_format = end_time_format

        self.is_output_elapse = False
        self.separator = " - "

    def __repr__(self):
        if self.is_output_elapse:
            suffix = f" ({self.end_datetime - self.start_datetime})"
        else:
            suffix = ""

        return self.separator.join((self.get_start_time_str(), self.get_end_time_str())) + suffix

    def __eq__(self, other):
        if not isinstance(other, DateTimeRange):
            return False

        return all(
            [self.start_datetime == other.start_datetime, self.end_datetime == other.end_datetime]
        )

    def __ne__(self, other):
        if not isinstance(other, DateTimeRange):
            return True

        return any(
            [self.start_datetime != other.start_datetime, self.end_datetime != other.end_datetime]
        )

    def __add__(self, other):
        return DateTimeRange(self.start_datetime + other, self.end_datetime + other)

    def __iadd__(self, other):
        self.set_start_datetime(self.start_datetime + other)
        self.set_end_datetime(self.end_datetime + other)

        return self

    def __sub__(self, other):
        return DateTimeRange(self.start_datetime - other, self.end_datetime - other)

    def __isub__(self, other):
        self.set_start_datetime(self.start_datetime - other)
        self.set_end_datetime(self.end_datetime - other)

        return self

    def __contains__(self, x):
        """
        :param x:
            |datetime|/``DateTimeRange`` instance to compare.
            Parse and convert to |datetime| if the value type is |str|.
        :type x: |datetime|/``DateTimeRange``/|str|
        :return: |True| if the ``x`` is within the time range
        :rtype: bool

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange

                time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                print("2015-03-22T10:05:00+0900" in time_range)
                print("2015-03-22T10:15:00+0900" in time_range)

                time_range_smaller = DateTimeRange("2015-03-22T10:03:00+0900", "2015-03-22T10:07:00+0900")
                print(time_range_smaller in time_range)
        :Output:
            .. parsed-literal::

                True
                False
                True

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

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                time_range.start_datetime
        :Output:
            .. parsed-literal::

                datetime.datetime(2015, 3, 22, 10, 0, tzinfo=tzoffset(None, 32400))
        """

        return self.__start_datetime

    @property
    def end_datetime(self):
        """
        :return: End time of the time range.
        :rtype: datetime.datetime

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                time_range.end_datetime
        :Output:
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

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                time_range.timedelta
        :Output:
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

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange

                time_range = DateTimeRange()
                print(time_range.is_set())

                time_range.set_time_range("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                print(time_range.is_set())
        :Output:
            .. parsed-literal::

                False
                True
        """

        return all([self.start_datetime is not None, self.end_datetime is not None])

    def validate_time_inversion(self):
        """
        Check time inversion of the time range.

        :raises ValueError:
            If |attr_start_datetime| is
            bigger than |attr_end_datetime|.
        :raises TypeError:
            Any one of |attr_start_datetime| and |attr_end_datetime|,
            or both is inappropriate datetime value.

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange("2015-03-22T10:10:00+0900", "2015-03-22T10:00:00+0900")
                try:
                    time_range.validate_time_inversion()
                except ValueError:
                    print("time inversion")
        :Output:
            .. parsed-literal::

                time inversion
        """

        if not self.is_set():
            # for python2/3 compatibility
            raise TypeError

        if self.start_datetime > self.end_datetime:
            raise ValueError(
                "time inversion found: {:s} > {:s}".format(
                    str(self.start_datetime), str(self.end_datetime)
                )
            )

    def is_valid_timerange(self):
        """
        :return:
            |True| if the time range is
            not null and not time inversion.
        :rtype: bool

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange()
                print(time_range.is_valid_timerange())
                time_range.set_time_range("2015-03-22T10:20:00+0900", "2015-03-22T10:10:00+0900")
                print(time_range.is_valid_timerange())
                time_range.set_time_range("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                print(time_range.is_valid_timerange())
        :Output:
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

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                x = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
                time_range.is_intersection(x)
        :Output:
            .. parsed-literal::

                True
        """

        return self.intersection(x).is_set()

    def get_start_time_str(self):
        """
        :return:
            |attr_start_datetime| as |str| formatted with
            |attr_start_time_format|.
            Return |NaT| if the invalid value or the invalid format.
        :rtype: str

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                print(time_range.get_start_time_str())
                time_range.start_time_format = "%Y/%m/%d %H:%M:%S"
                print(time_range.get_start_time_str())
        :Output:
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

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                print(time_range.get_end_time_str())
                time_range.end_time_format = "%Y/%m/%d %H:%M:%S"
                print(time_range.get_end_time_str())
        :Output:
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

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                time_range.get_timedelta_second()
        :Output:
            .. parsed-literal::

                600.0
        """

        return self.timedelta.total_seconds()

    def set_start_datetime(self, value, timezone=None):
        """
        Set the start time of the time range.

        :param value: |param_start_datetime|
        :type value: |datetime|/|str|
        :raises ValueError: If the value is invalid as a |datetime| value.

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange()
                print(time_range)
                time_range.set_start_datetime("2015-03-22T10:00:00+0900")
                print(time_range)
        :Output:
            .. parsed-literal::

                NaT - NaT
                2015-03-22T10:00:00+0900 - NaT
        """

        self.__start_datetime = self.__normalize_datetime_value(value, timezone)

    def set_end_datetime(self, value, timezone=None):
        """
        Set the end time of the time range.

        :param datetime.datetime/str value: |param_end_datetime|
        :raises ValueError: If the value is invalid as a |datetime| value.

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange()
                print(time_range)
                time_range.set_end_datetime("2015-03-22T10:10:00+0900")
                print(time_range)
        :Output:
            .. parsed-literal::

                NaT - NaT
                NaT - 2015-03-22T10:10:00+0900
        """

        self.__end_datetime = self.__normalize_datetime_value(value, timezone)

    def set_time_range(self, start, end):
        """
        :param datetime.datetime/str start: |param_start_datetime|
        :param datetime.datetime/str end: |param_end_datetime|

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange()
                print(time_range)
                time_range.set_time_range("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                print(time_range)
        :Output:
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
                lhs.normalized(), rdelta.relativedelta(seconds=seconds)
            )

    def range(self, step):
        """
        Return an iterator object.

        :param step: Step of iteration.
        :type step: |timedelta|/dateutil.relativedelta.relativedelta
        :return: iterator
        :rtype: iterator

        :Sample Code:
            .. code:: python

                import datetime
                from datetimerange import DateTimeRange

                time_range = DateTimeRange("2015-01-01T00:00:00+0900", "2015-01-04T00:00:00+0900")
                for value in time_range.range(datetime.timedelta(days=1)):
                    print(value)
        :Output:
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
                raise ValueError(f"invalid step: expect greater than 0, actual={step}")
        else:
            if self.__compare_timedelta(step, seconds=0) > 0:
                raise ValueError(f"invalid step: expect less than 0, actual={step}")

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

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                dtr0 = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                dtr1 = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
                dtr0.intersection(dtr1)
        :Output:
            .. parsed-literal::

                2015-03-22T10:05:00+0900 - 2015-03-22T10:10:00+0900
        """

        self.validate_time_inversion()
        x.validate_time_inversion()

        if any([x.start_datetime in self, self.start_datetime in x]):
            start_datetime = max(self.start_datetime, x.start_datetime)
            end_datetime = min(self.end_datetime, x.end_datetime)
        else:
            start_datetime = None
            end_datetime = None

        return DateTimeRange(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            start_time_format=self.start_time_format,
            end_time_format=self.end_time_format,
        )

    def subtract(self, x):
        """
        Remove a time range from this one and return the result.

        - The result will be ``[self.copy()]`` if the second range does not overlap the first
        - The result will be ``[]`` if the second range wholly encompasses the first range
        - The result will be ``[new_range]`` if the second range overlaps one end of the range
        - The result will be ``[new_range1, new_range2]`` if the second range is
          an internal sub range of the first

        :param DateTimeRange x:
            Range to remove from this one.
        :return: List(DateTimeRange)
            List of new ranges when the second range is removed from this one
        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                dtr0 = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                dtr1 = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
                dtr0.subtract(dtr1)
        :Output:
          .. parsed-literal::

                [2015-03-22T10:00:00+0900 - 2015-03-22T10:05:00+0900]
        """
        overlap = self.intersection(x)
        # No intersection, return a copy of the original
        if not overlap.is_set() or overlap.get_timedelta_second() <= 0:
            return [
                DateTimeRange(
                    start_datetime=self.start_datetime,
                    end_datetime=self.end_datetime,
                    start_time_format=self.start_time_format,
                    end_time_format=self.end_time_format,
                )
            ]

        # Case 2, full overlap, subtraction results in empty set
        if (
            overlap.start_datetime == self.start_datetime
            and overlap.end_datetime == self.end_datetime
        ):
            return []

        # Case 3, overlap on start
        if overlap.start_datetime == self.start_datetime:
            return [
                DateTimeRange(
                    start_datetime=overlap.end_datetime,
                    end_datetime=self.end_datetime,
                    start_time_format=self.start_time_format,
                    end_time_format=self.end_time_format,
                )
            ]

        # Case 4, overlap on end
        if overlap.end_datetime == self.end_datetime:
            return [
                DateTimeRange(
                    start_datetime=self.start_datetime,
                    end_datetime=overlap.start_datetime,
                    start_time_format=self.start_time_format,
                    end_time_format=self.end_time_format,
                )
            ]

        # Case 5, underlap, two new ranges are needed.
        return [
            DateTimeRange(
                start_datetime=self.start_datetime,
                end_datetime=overlap.start_datetime,
                start_time_format=self.start_time_format,
                end_time_format=self.end_time_format,
            ),
            DateTimeRange(
                start_datetime=overlap.end_datetime,
                end_datetime=self.end_datetime,
                start_time_format=self.start_time_format,
                end_time_format=self.end_time_format,
            ),
        ]

    def encompass(self, x):
        """
        Newly set a time range that encompasses
        the input and the current time range.

        :param DateTimeRange x:
            Value to compute encompass with the current time range.

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                dtr0 = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                dtr1 = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
                dtr0.encompass(dtr1)
        :Output:
            .. parsed-literal::

                2015-03-22T10:00:00+0900 - 2015-03-22T10:15:00+0900
        """

        self.validate_time_inversion()
        x.validate_time_inversion()

        return DateTimeRange(
            start_datetime=min(self.start_datetime, x.start_datetime),
            end_datetime=max(self.end_datetime, x.end_datetime),
            start_time_format=self.start_time_format,
            end_time_format=self.end_time_format,
        )

    def truncate(self, percentage):
        """
        Truncate ``percentage`` / 2 [%] of whole time from first and last time.

        :param float percentage: Percentage of truncate.

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                time_range = DateTimeRange(
                    "2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                time_range.is_output_elapse = True
                print(time_range)
                time_range.truncate(10)
                print(time_range)
        :Output:
            .. parsed-literal::

                2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900 (0:10:00)
                2015-03-22T10:00:30+0900 - 2015-03-22T10:09:30+0900 (0:09:00)
        """

        self.validate_time_inversion()

        if percentage < 0:
            raise ValueError("discard_percent must be greater or equal to zero: " + str(percentage))

        if percentage == 0:
            return

        discard_time = self.timedelta // int(100) * int(percentage / 2)

        self.__start_datetime += discard_time
        self.__end_datetime -= discard_time

    def split(self, separator: Union[str, datetime.datetime]) -> List["DateTimeRange"]:
        """
        Split the DateTimerange in two DateTimerange at a specifit datetime.

        :param Union[str, datetime.datetime] separator:
            Date and time to split the DateTimeRange.
            This value will be included for both of the ranges after split.

        :Sample Code:
            .. code:: python

                from datetimerange import DateTimeRange
                dtr = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
                dtr.split("2015-03-22T10:05:00+0900")
        :Output:
            .. parsed-literal::

                [2015-03-22T10:00:00+0900 - 2015-03-22T10:05:00+0900,
                2015-03-22T10:05:00+0900 - 2015-03-22T10:10:00+0900]
        """

        self.validate_time_inversion()

        separatingseparation = self.__normalize_datetime_value(separator, timezone=None)

        if (separatingseparation not in self) or (
            separatingseparation in (self.start_datetime, self.end_datetime)
        ):
            return [
                DateTimeRange(
                    start_datetime=self.start_datetime,
                    end_datetime=self.end_datetime,
                    start_time_format=self.start_time_format,
                    end_time_format=self.end_time_format,
                )
            ]

        return [
            DateTimeRange(
                start_datetime=self.start_datetime,
                end_datetime=separatingseparation,
                start_time_format=self.start_time_format,
                end_time_format=self.end_time_format,
            ),
            DateTimeRange(
                start_datetime=separatingseparation,
                end_datetime=self.end_datetime,
                start_time_format=self.start_time_format,
                end_time_format=self.end_time_format,
            ),
        ]

    def __normalize_datetime_value(self, value, timezone):
        if value is None:
            return None

        try:
            return typepy.type.DateTime(
                value, strict_level=typepy.StrictLevel.MIN, timezone=timezone
            ).convert()
        except typepy.TypeConversionError as e:
            raise ValueError(e)

    @classmethod
    def from_range_text(
        cls,
        range_text: str,
        separator: str = "-",
        start_time_format: Optional[str] = None,
        end_time_format: Optional[str] = None,
    ) -> "DateTimeRange":
        """Create a ``DateTimeRange`` instance from a datetime range text.

        :param str range_text:
            Input text that includes datetime range.
            e.g. ``2021-01-23T10:00:00+0400 - 2021-01-232T10:10:00+0400``

        :param str separator:
            Text that separating the ``range_text``.

        :return: DateTimeRange
            Created instance.
        """

        dattime_ranges = re.split(r"\s+{}\s+".format(re.escape(separator)), range_text.strip())
        if len(dattime_ranges) != 2:
            raise ValueError("range_text should include two datetime that separated by hyphen")

        start, end = dattime_ranges
        kwargs = {
            "start_datetime": start,
            "end_datetime": end,
        }
        if start_time_format:
            kwargs["start_time_format"] = start_time_format
        if end_time_format:
            kwargs["end_time_format"] = end_time_format

        return DateTimeRange(**kwargs)
