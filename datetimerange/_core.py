"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import datetime
import re
from typing import ClassVar, Iterator, List, Optional, Union

import dateutil.parser
import dateutil.relativedelta as rdelta
import typepy


DEFAULT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def _to_norm_relativedelta(td: Union[datetime.timedelta, rdelta.relativedelta]) -> rdelta.relativedelta:
    if isinstance(td, rdelta.relativedelta):
        return td.normalized()

    return rdelta.relativedelta(seconds=int(td.total_seconds()), microseconds=td.microseconds).normalized()


def _compare_relativedelta(lhs: rdelta.relativedelta, rhs: rdelta.relativedelta) -> int:
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


def _compare_timedelta(lhs: Union[datetime.timedelta, rdelta.relativedelta], seconds: int) -> int:
    return _compare_relativedelta(_to_norm_relativedelta(lhs), rdelta.relativedelta(seconds=seconds))


def _normalize_datetime_value(
    value: Union[datetime.datetime, str, None], timezone: Optional[datetime.tzinfo]
) -> Optional[datetime.datetime]:
    if value is None:
        return None

    try:
        return typepy.type.DateTime(value, strict_level=typepy.StrictLevel.MIN, timezone=timezone).convert()
    except typepy.TypeConversionError as e:
        raise ValueError(e)


class DateTimeRange:
    """
    A class that represents a range of datetime.

    :param Union[datetime.datetime, str, None] start_datetime: |param_start_datetime|
    :param Union[datetime.datetime, str, None] end_datetime: |param_end_datetime|
    :param Optional[str] start_time_format:
        Conversion format string for :py:attr:`.start_datetime`.
    :param Optional[str] end_time_format:
        Conversion format string for :py:attr:`.end_datetime`.
    :param Optional[datetime.tzinfo] timezone:
        Timezone of the time range.

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

    NOT_A_TIME_STR: ClassVar[str] = "NaT"

    def __init__(
        self,
        start_datetime: Union[datetime.datetime, str, None] = None,
        end_datetime: Union[datetime.datetime, str, None] = None,
        start_time_format: Optional[str] = None,
        end_time_format: Optional[str] = None,
        timezone: Optional[datetime.tzinfo] = None,
    ) -> None:
        self.set_time_range(start_datetime, end_datetime, timezone)

        self.start_time_format = start_time_format or DEFAULT_TIME_FORMAT
        self.end_time_format = end_time_format or DEFAULT_TIME_FORMAT

        self.is_output_elapse = False
        self.separator = " - "

    def __repr__(self) -> str:
        if self.is_output_elapse and self.end_datetime and self.start_datetime:
            suffix = f" ({self.end_datetime - self.start_datetime})"
        else:
            suffix = ""

        return self.separator.join((self.get_start_time_str(), self.get_end_time_str())) + suffix

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DateTimeRange):
            return False

        return all([self.start_datetime == other.start_datetime, self.end_datetime == other.end_datetime])

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, DateTimeRange):
            return True

        return any([self.start_datetime != other.start_datetime, self.end_datetime != other.end_datetime])

    def __add__(self, other: Union[datetime.timedelta, rdelta.relativedelta]) -> "DateTimeRange":
        if self.start_datetime is None and self.end_datetime is None:
            raise TypeError("range is not set")

        start_datetime = self.start_datetime
        if start_datetime:
            start_datetime += other

        end_datetime = self.end_datetime
        if end_datetime:
            end_datetime += other

        return DateTimeRange(start_datetime, end_datetime)

    def __iadd__(self, other: Union[datetime.timedelta, rdelta.relativedelta]) -> "DateTimeRange":
        if self.start_datetime is None and self.end_datetime is None:
            raise TypeError("range is not set")

        timezone = self.timezone

        if self.start_datetime:
            self.set_start_datetime(self.start_datetime + other, timezone)

        if self.end_datetime:
            self.set_end_datetime(self.end_datetime + other, timezone)

        return self

    def __sub__(self, other: Union[datetime.timedelta, rdelta.relativedelta]) -> "DateTimeRange":
        if self.start_datetime is None and self.end_datetime is None:
            raise TypeError("range is not set")

        start_datetime = self.start_datetime
        if start_datetime:
            start_datetime -= other

        end_datetime = self.end_datetime
        if end_datetime:
            end_datetime -= other

        return DateTimeRange(start_datetime, end_datetime)

    def __isub__(self, other: Union[datetime.timedelta, rdelta.relativedelta]) -> "DateTimeRange":
        if self.start_datetime is None and self.end_datetime is None:
            raise TypeError("range is not set")

        timezone = self.timezone

        if self.start_datetime:
            self.set_start_datetime(self.start_datetime - other, timezone)

        if self.end_datetime:
            self.set_end_datetime(self.end_datetime - other, timezone)

        return self

    def __contains__(self, x: Union[datetime.datetime, "DateTimeRange", str]) -> bool:
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
        assert self.start_datetime
        assert self.end_datetime

        if isinstance(x, DateTimeRange):
            x.validate_time_inversion()
            assert x.start_datetime
            assert x.end_datetime

            return x.start_datetime >= self.start_datetime and x.end_datetime <= self.end_datetime

        value = dateutil.parser.parse(x) if isinstance(x, str) else x

        return self.start_datetime <= value <= self.end_datetime

    @property
    def start_datetime(self) -> Optional[datetime.datetime]:
        """
        :return: Start time of the time range.
        :rtype: Optional[datetime.datetime]

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
    def end_datetime(self) -> Optional[datetime.datetime]:
        """
        :return: End time of the time range.
        :rtype: Optional[datetime.datetime]

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
    def timezone(self) -> Optional[datetime.tzinfo]:
        """
        :return: Timezone of the time range.
        :rtype: Optional[datetime.tzinfo]
        """

        if self.start_datetime and self.start_datetime.tzinfo:
            return self.start_datetime.tzinfo

        if self.end_datetime and self.end_datetime.tzinfo:
            return self.end_datetime.tzinfo

        return None

    @property
    def timedelta(self) -> datetime.timedelta:
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

        if self.start_datetime is None:
            raise TypeError("Must set start_datetime")
        if self.end_datetime is None:
            raise TypeError("Must set end_datetime")

        return self.end_datetime - self.start_datetime

    def is_set(self) -> bool:
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

    def validate_time_inversion(self) -> None:
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

        assert self.start_datetime
        assert self.end_datetime

        if self.start_datetime.tzinfo != self.end_datetime.tzinfo:
            raise ValueError(f"timezone mismatch: start={self.start_datetime.tzinfo}, end={self.end_datetime.tzinfo}")

        if self.start_datetime > self.end_datetime:
            raise ValueError(
                "time inversion found: {:s} > {:s}".format(str(self.start_datetime), str(self.end_datetime))
            )

    def is_valid_timerange(self) -> bool:
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

    def is_intersection(
        self,
        x: "DateTimeRange",
        intersection_threshold: Union[datetime.timedelta, rdelta.relativedelta, None] = None,
    ) -> bool:
        """
        :param DateTimeRange x: Value to compare
        :param Union[datetime.timedelta, dateutil.relativedelta.relativedelta, None] intersection_threshold:
            Minimum time constraint that an intersection must have.
            Defaults to ``None`` (no constraint).

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

        return self.intersection(x, intersection_threshold).is_set()

    def get_start_time_str(self) -> str:
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

        if self.start_datetime is None:
            return self.NOT_A_TIME_STR

        try:
            return self.start_datetime.strftime(self.start_time_format)
        except AttributeError:
            return self.NOT_A_TIME_STR

    def get_end_time_str(self) -> str:
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

        if self.end_datetime is None:
            return self.NOT_A_TIME_STR

        try:
            return self.end_datetime.strftime(self.end_time_format)
        except AttributeError:
            return self.NOT_A_TIME_STR

    def get_timedelta_second(self) -> float:
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

    def set_start_datetime(
        self, value: Union[datetime.datetime, str, None], timezone: Optional[datetime.tzinfo] = None
    ) -> None:
        """
        Set the start time of the time range.

        :param Union[datetime.datetime, str, None] value: |param_start_datetime|
        :param Optional[datetime.tzinfo] timezone: |param_timezone|
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

        self.__start_datetime = _normalize_datetime_value(value, timezone)

    def set_end_datetime(
        self, value: Union[datetime.datetime, str, None], timezone: Optional[datetime.tzinfo] = None
    ) -> None:
        """
        Set the end time of the time range.

        :param Union[datetime.datetime, str, None] value: |param_end_datetime|
        :param Optional[datetime.tzinfo] timezone: |param_timezone|
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

        self.__end_datetime = _normalize_datetime_value(value, timezone)

    def set_time_range(
        self,
        start: Union[datetime.datetime, str, None],
        end: Union[datetime.datetime, str, None],
        timezone: Optional[datetime.tzinfo] = None,
    ) -> None:
        """
        :param Union[datetime.datetime, str, None] start: |param_start_datetime|
        :param Union[datetime.datetime, str, None] end: |param_end_datetime|
        :param Optional[datetime.tzinfo] timezone: |param_timezone|

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

        self.set_start_datetime(start, timezone)
        self.set_end_datetime(end, timezone)

    def range(self, step: Union[datetime.timedelta, rdelta.relativedelta]) -> Iterator[datetime.datetime]:
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

        cmp_step_w_zero = _compare_timedelta(step, seconds=0)
        if cmp_step_w_zero == 0:
            raise ValueError("step must be not zero")

        is_inversion = False
        try:
            self.validate_time_inversion()
        except ValueError:
            is_inversion = True

        assert self.start_datetime
        assert self.end_datetime

        current_datetime = self.start_datetime

        if not is_inversion:
            if cmp_step_w_zero < 0:
                raise ValueError(f"invalid step: expect greater than 0, actual={step}")

            while current_datetime <= self.end_datetime:
                yield current_datetime
                current_datetime = current_datetime + step
        else:
            if cmp_step_w_zero > 0:
                raise ValueError(f"invalid step: expect less than 0, actual={step}")

            while current_datetime >= self.end_datetime:
                yield current_datetime
                current_datetime = current_datetime + step

    def intersection(
        self,
        x: "DateTimeRange",
        intersection_threshold: Union[datetime.timedelta, rdelta.relativedelta, None] = None,
    ) -> "DateTimeRange":
        """
        Create a new time range that overlaps the input and the current time range.
        If no overlaps found, return a time range that set ``None`` for both start and end time.

        :param DateTimeRange x:
            Value to compute intersection with the current time range.
        :param Union[datetime.timedelta, dateutil.relativedelta.relativedelta, None] intersection_threshold:
            Minimum time constraint that an intersection must have.
            Defaults to ``None`` (no constraint).

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
        assert self.start_datetime
        assert self.end_datetime
        assert x.start_datetime
        assert x.end_datetime

        if any([x.start_datetime in self, self.start_datetime in x]):
            start_datetime = max(self.start_datetime, x.start_datetime)
            end_datetime = min(self.end_datetime, x.end_datetime)
        else:
            start_datetime = None
            end_datetime = None

        if intersection_threshold is not None:
            if start_datetime is None or end_datetime is None:
                return DateTimeRange(
                    start_datetime=None,
                    end_datetime=None,
                    start_time_format=self.start_time_format,
                    end_time_format=self.end_time_format,
                )

            delta = end_datetime - start_datetime

            if (
                _compare_relativedelta(
                    _to_norm_relativedelta(delta),
                    _to_norm_relativedelta(intersection_threshold),
                )
                < 0
            ):
                start_datetime = None
                end_datetime = None

        return DateTimeRange(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            start_time_format=self.start_time_format,
            end_time_format=self.end_time_format,
        )

    def subtract(self, x: "DateTimeRange") -> List["DateTimeRange"]:
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
        if overlap.start_datetime == self.start_datetime and overlap.end_datetime == self.end_datetime:
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

    def encompass(self, x: "DateTimeRange") -> "DateTimeRange":
        """
        Create a new time range that encompasses the input and the current time range.

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
        assert self.start_datetime
        assert self.end_datetime
        assert x.start_datetime
        assert x.end_datetime

        return DateTimeRange(
            start_datetime=min(self.start_datetime, x.start_datetime),
            end_datetime=max(self.end_datetime, x.end_datetime),
            start_time_format=self.start_time_format,
            end_time_format=self.end_time_format,
        )

    def truncate(self, percentage: float) -> None:
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

        if self.__start_datetime:
            self.__start_datetime += discard_time

        if self.__end_datetime:
            self.__end_datetime -= discard_time

    def split(self, separator: Union[str, datetime.datetime]) -> List["DateTimeRange"]:
        """
        Split the DateTimerange in two DateTimerange at a specific datetime.

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

        separatingseparation = _normalize_datetime_value(separator, timezone=None)
        assert separatingseparation

        if (separatingseparation not in self) or (separatingseparation in (self.start_datetime, self.end_datetime)):
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

    @classmethod
    def from_range_text(
        cls,
        range_text: str,
        separator: str = r"\s+\-\s+",
        start_time_format: Optional[str] = None,
        end_time_format: Optional[str] = None,
        timezone: Optional[datetime.tzinfo] = None,
    ) -> "DateTimeRange":
        """Create a ``DateTimeRange`` instance from a datetime range text.

        :param str range_text:
            Input text that includes datetime range.
            e.g. ``2021-01-23T10:00:00+0400 - 2021-01-232T10:10:00+0400``

        :param str separator:
            Regular expression that separating the ``range_text`` to start and end time.

        :return: DateTimeRange
            Created instance.
        """

        datetime_ranges = re.split(separator, range_text.strip())
        if len(datetime_ranges) != 2:
            raise ValueError(f"range_text should include two datetime that separated by hyphen: got={datetime_ranges}")

        return DateTimeRange(
            start_datetime=datetime_ranges[0],
            end_datetime=datetime_ranges[1],
            start_time_format=start_time_format,
            end_time_format=end_time_format,
            timezone=timezone,
        )
