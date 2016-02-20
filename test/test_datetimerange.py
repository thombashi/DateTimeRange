# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''

import datetime

import dateutil
from dateutil.parser import *
import pytest

from datetimerange import DateTimeRange


TIMEZONE = "+0900"
START_DATETIME_TEXT = "2015-03-22T10:00:00" + TIMEZONE
END_DATETIME_TEXT = "2015-03-22T10:10:00" + TIMEZONE

TEST_START_DATETIME = parse(START_DATETIME_TEXT)
TEST_END_DATETIME = parse(END_DATETIME_TEXT)
ISO_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def setup_module(module):
    import locale

    locale.setlocale(locale.LC_ALL, 'C')


@pytest.fixture
def datetimerange_normal():
    value = DateTimeRange(
        TEST_START_DATETIME, TEST_END_DATETIME)
    value.start_time_format = ISO_TIME_FORMAT
    value.end_time_format = ISO_TIME_FORMAT

    return value


@pytest.fixture
def datetimerange_inversion():
    value = DateTimeRange(
        TEST_END_DATETIME, TEST_START_DATETIME)
    value.start_time_format = ISO_TIME_FORMAT
    value.end_time_format = ISO_TIME_FORMAT

    return value


@pytest.fixture
def datetimerange_null():
    value = DateTimeRange(None, None)
    value.time_format = None
    value.end_time_format = None

    return value


@pytest.fixture
def datetimerange_null_start():
    value = DateTimeRange(None, TEST_END_DATETIME)
    value.time_format = None
    value.end_time_format = ISO_TIME_FORMAT

    return value


class Test_DateTimeRange_repr:

    @pytest.mark.parametrize(
        [
            "start", "start_format",
            "end", "end_format",
            "separator", "is_output_elapse", "expected"
        ],
        [
            [
                TEST_START_DATETIME, ISO_TIME_FORMAT,
                TEST_END_DATETIME, ISO_TIME_FORMAT,
                " - ", False,
                "2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900"
            ],
            [
                "2015-03-22T09:00:00+0900", ISO_TIME_FORMAT,
                "2015-03-22T10:10:00+0900", ISO_TIME_FORMAT,
                " - ", False,
                "2015-03-22T09:00:00+0900 - 2015-03-22T10:10:00+0900"
            ],
            [
                TEST_START_DATETIME, ISO_TIME_FORMAT,
                TEST_END_DATETIME, ISO_TIME_FORMAT,
                " - ", True,
                "2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900 (0:10:00)"
            ],
            [
                TEST_END_DATETIME, ISO_TIME_FORMAT,
                TEST_START_DATETIME, ISO_TIME_FORMAT,
                " - ", True,
                "2015-03-22T10:10:00+0900 - 2015-03-22T10:00:00+0900 (-1 day, 23:50:00)"
            ],
            [
                TEST_START_DATETIME, "%Y%m%d%H%M%S",
                TEST_END_DATETIME, "%Y/%m/%d %H:%M:%S%z",
                " to ", False,
                "20150322100000 to 2015/03/22 10:10:00+0900"
            ],
            [
                None, ISO_TIME_FORMAT,
                TEST_END_DATETIME, ISO_TIME_FORMAT,
                " - ", False,
                "NaT - 2015-03-22T10:10:00+0900"
            ],
            [
                TEST_START_DATETIME, ISO_TIME_FORMAT,
                None, ISO_TIME_FORMAT,
                " - ", False,
                "2015-03-22T10:00:00+0900 - NaT"
            ],
            [
                None, ISO_TIME_FORMAT,
                None, ISO_TIME_FORMAT,
                " - ", False,
                "NaT - NaT"
            ],
        ])
    def test_normal(
            self, start, start_format, end, end_format,
            separator, is_output_elapse, expected):
        dtr = DateTimeRange(start, end, start_format, end_format)
        dtr.separator = separator
        dtr.is_output_elapse = is_output_elapse
        assert str(dtr) == expected

    @pytest.mark.parametrize(
        [
            "start", "start_format",
            "end", "end_format",
            "separator", "is_output_elapse", "expected"
        ],
        [
            [
                TEST_START_DATETIME, None,
                TEST_END_DATETIME, ISO_TIME_FORMAT,
                " - ", False,
                TypeError
            ],
            [
                TEST_START_DATETIME, ISO_TIME_FORMAT,
                TEST_END_DATETIME, None,
                " - ", False,
                TypeError
            ],
            [
                TEST_START_DATETIME, ISO_TIME_FORMAT,
                TEST_END_DATETIME, ISO_TIME_FORMAT,
                None, False,
                AttributeError
            ],
        ])
    def test_exception(
            self, start, start_format, end, end_format,
            separator, is_output_elapse, expected):
        dtr = DateTimeRange(start, end, start_format, end_format)
        dtr.separator = separator
        dtr.is_output_elapse = is_output_elapse
        with pytest.raises(expected):
            str(dtr)


class Test_DateTimeRange_eq:

    def test_normal(self, datetimerange_normal):
        assert datetimerange_normal == datetimerange_normal

    def test_null(self, datetimerange_null):
        assert datetimerange_null == datetimerange_null

    def test_neq(self, datetimerange_normal, datetimerange_null):
        assert datetimerange_normal != datetimerange_null


class Test_DateTimeRange_contains:

    @pytest.mark.parametrize(["value", "expected"], [
        [START_DATETIME_TEXT, True],
        [END_DATETIME_TEXT, True],
        [TEST_START_DATETIME, True],
        [TEST_END_DATETIME, True],
        ["2015-03-22 09:59:59" + TIMEZONE, False],
        ["2015-03-22 10:10:01" + TIMEZONE, False],
    ])
    def test_normal(self, datetimerange_normal, value, expected):
        assert (value in datetimerange_normal) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [None, TypeError],
        [False, TypeError],
        [20140513221937, TypeError],
    ])
    def test_exception(
            self, datetimerange_normal, value, expected):
        with pytest.raises(expected):
            value in datetimerange_normal

    @pytest.mark.parametrize(["value", "expected"], [
        [TEST_START_DATETIME, TypeError],
        ["aaa", TypeError],
        [None, TypeError],
    ])
    def test_null_start(self, datetimerange_null_start, value, expected):
        with pytest.raises(expected):
            value in datetimerange_null_start


class Test_DateTimeRange_timedelta:

    def test_normal(self, datetimerange_normal):
        assert datetimerange_normal.timedelta == datetime.timedelta(
            seconds=10 * 60)

    def test_inversion(self, datetimerange_inversion):
        assert datetimerange_inversion.timedelta == datetime.timedelta(
            -1, 85800)

    def test_null(self, datetimerange_null):
        with pytest.raises(TypeError):
            datetimerange_null.timedelta

    def test_exception(self, datetimerange_null_start):
        with pytest.raises(TypeError):
            datetimerange_null_start.timedelta


class Test_DateTimeRange_is_set:

    @pytest.mark.parametrize(["value", "expected"], [
        [DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME), True],
        [DateTimeRange(TEST_END_DATETIME, TEST_START_DATETIME), True],
        [DateTimeRange(TEST_START_DATETIME, None), False],
        [DateTimeRange(None, TEST_START_DATETIME), False],
        [DateTimeRange(None, None), False],
    ])
    def test_normal(self, value, expected):
        assert value.is_set() == expected


class Test_DateTimeRange_validate_time_inversion:

    @pytest.mark.parametrize(["value"], [
        [DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME)],
        [DateTimeRange(TEST_START_DATETIME, TEST_START_DATETIME)],
    ])
    def test_normal(self, value):
        value.validate_time_inversion()

    def test_inversion(self, datetimerange_inversion):
        with pytest.raises(ValueError):
            datetimerange_inversion.validate_time_inversion()

    @pytest.mark.parametrize(["value"], [
        [DateTimeRange(None, None)],
        [DateTimeRange(None, TEST_END_DATETIME)],
        [DateTimeRange(TEST_START_DATETIME, None)],
    ])
    def test_exception(self, value):
        with pytest.raises(TypeError):
            value.validate_time_inversion()


class Test_DateTimeRange_is_valid_timerange:

    @pytest.mark.parametrize(["value", "expected"], [
        [DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME), True],
        [DateTimeRange(TEST_END_DATETIME, TEST_START_DATETIME), False],
        [DateTimeRange(TEST_START_DATETIME, None), False],
        [DateTimeRange(None, TEST_START_DATETIME), False],
        [DateTimeRange(None, None), False],
    ])
    def test_normal(self, value, expected):
        assert value.is_valid_timerange() == expected


class Test_DateTimeRange_is_intersection:

    @pytest.mark.parametrize(["lhs", "rhs", "expected"], [
        [
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            True,
        ],
        [
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:00:00 JST"),
            DateTimeRange(
                "2015-01-22T10:10:00 JST",
                "2015-03-22T10:20:00 JST"),
            False,
        ],
        [
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:00:00 JST"),
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-03-22T10:20:00 JST"),
            True,
        ],
        [
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:05:00 JST"),
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-03-22T10:20:00 JST"),
            True,
        ],
        [
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-03-22T10:20:00 JST"),
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:05:00 JST"),
            True,
        ],
        [
            DateTimeRange(
                "2014-01-22T10:00:00 JST",
                "2016-03-22T10:20:00 JST"),
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:05:00 JST"),
            True,
        ],
        [
            DateTimeRange(
                "2015-01-12T10:00:00 JST",
                "2015-02-22T10:10:00 JST"),
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-03-22T10:10:00 JST"),
            True,
        ],
    ])
    def test_normal(self, lhs, rhs, expected):
        assert lhs.is_intersection(rhs) == expected

    @pytest.mark.parametrize(["lhs", "rhs", "expected"], [
        [
            DateTimeRange(None, None),
            DateTimeRange(None, None),
            TypeError,
        ],
        [
            DateTimeRange(None, TEST_END_DATETIME),
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            TypeError,
        ],
        [
            DateTimeRange(TEST_END_DATETIME, TEST_START_DATETIME),
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            ValueError,
        ],
        [
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            DateTimeRange(None, TEST_END_DATETIME),
            TypeError,
        ],
        [
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            DateTimeRange(TEST_END_DATETIME, TEST_START_DATETIME),
            ValueError,
        ],
    ])
    def test_exception(self, lhs, rhs, expected):
        with pytest.raises(expected):
            lhs.is_intersection(rhs)


class Test_DateTimeRange_get_start_time_str:

    @pytest.mark.parametrize(["time_format", "expected"], [
        [ISO_TIME_FORMAT, START_DATETIME_TEXT],
        ["%Y/%m/%d %H:%M:%S%z", "2015/03/22 10:00:00+0900"]
    ])
    def test_normal(self, datetimerange_normal, time_format, expected):
        datetimerange_normal.start_time_format = time_format
        assert datetimerange_normal.get_start_time_str() == expected

    def test_abnormal_1(self, datetimerange_null):
        assert datetimerange_null.get_start_time_str(
        ) == DateTimeRange.NOT_A_TIME_STR

    def test_abnormal_2(self, datetimerange_normal):
        datetimerange_normal.start_time_format = "aaa"
        assert datetimerange_normal.get_start_time_str(
        ) == "aaa"

    @pytest.mark.parametrize(["time_format", "expected"], [
        [None, TypeError],
    ])
    def test_exception(self, datetimerange_normal, time_format, expected):
        datetimerange_normal.start_time_format = time_format
        with pytest.raises(expected):
            datetimerange_normal.get_start_time_str()


class Test_DateTimeRange_get_end_time_str:

    @pytest.mark.parametrize(["time_format", "expected"], [
        [ISO_TIME_FORMAT, END_DATETIME_TEXT],
        ["%Y/%m/%d %H:%M:%S%z", "2015/03/22 10:10:00+0900"]
    ])
    def test_normal(self, datetimerange_normal, time_format, expected):
        datetimerange_normal.end_time_format = time_format
        assert datetimerange_normal.get_end_time_str() == expected

    def test_abnormal_1(self, datetimerange_null):
        assert datetimerange_null.get_end_time_str(
        ) == DateTimeRange.NOT_A_TIME_STR

    def test_abnormal_2(self, datetimerange_normal):
        datetimerange_normal.end_time_format = "aaa"
        assert datetimerange_normal.get_end_time_str(
        ) == "aaa"

    @pytest.mark.parametrize(["time_format", "expected"], [
        [None, TypeError],
    ])
    def test_exception(self, datetimerange_normal, time_format, expected):
        datetimerange_normal.end_time_format = time_format
        with pytest.raises(expected):
            datetimerange_normal.get_end_time_str()


class Test_DateTimeRange_get_timedelta_second:

    def test_normal(self, datetimerange_normal):
        assert datetimerange_normal.get_timedelta_second() == 600

    def test_inversion(self, datetimerange_inversion):
        assert datetimerange_inversion.get_timedelta_second() == -600

    def test_null(self, datetimerange_null):
        with pytest.raises(TypeError):
            datetimerange_null.get_timedelta_second()

    def test_exception(self, datetimerange_null_start):
        with pytest.raises(TypeError):
            datetimerange_null_start.get_timedelta_second()


class Test_DateTimeRange_set_start_datetime:

    @pytest.mark.parametrize(["value", "expected"], [
        [START_DATETIME_TEXT, TEST_START_DATETIME],
        [TEST_START_DATETIME, TEST_START_DATETIME],
        [None, None],
        [11111, None],
    ])
    def test_normal(self, value, expected):
        dtr = DateTimeRange(TEST_END_DATETIME, TEST_END_DATETIME)
        dtr.set_start_datetime(value)
        assert dtr.start_datetime == expected

    @pytest.mark.parametrize(["value", "expected"], [
        ["invalid time string", ValueError],
    ])
    def test_null_start(self, datetimerange_null_start, value, expected):
        with pytest.raises(expected):
            datetimerange_null_start.set_start_datetime(value)


class Test_DateTimeRange_set_end_datetime:

    @pytest.mark.parametrize(["value", "expected"], [
        [START_DATETIME_TEXT, TEST_START_DATETIME],
        [TEST_START_DATETIME, TEST_START_DATETIME],
        [None, None],
    ])
    def test_normal(self, value, expected):
        dtr = DateTimeRange(TEST_END_DATETIME, TEST_END_DATETIME)
        dtr.set_end_datetime(value)
        assert dtr.end_datetime == expected

    @pytest.mark.parametrize(["value", "expected"], [
        ["invalid time string", ValueError],
    ])
    def test_null_start(self, datetimerange_null_start, value, expected):
        with pytest.raises(expected):
            datetimerange_null_start.set_end_datetime(value)


class Test_DateTimeRange_set_time_range:

    @pytest.mark.parametrize(["start", "end", "expected"], [
        [
            START_DATETIME_TEXT, END_DATETIME_TEXT,
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
        ],
        [None, None, DateTimeRange(None, None)],
    ])
    def test_normal(self, start, end, expected):
        dtr = DateTimeRange()
        dtr.set_time_range(start, end)
        assert dtr == expected

    @pytest.mark.parametrize(["start", "end", "expected"], [
        [
            "invalid time string", END_DATETIME_TEXT,
            ValueError,
        ],
        [
            START_DATETIME_TEXT, "invalid time string",
            ValueError,
        ],
        [
            "invalid time string", "invalid time string",
            ValueError,
        ],
    ])
    def test_exception(self, start, end, expected):
        dtr = DateTimeRange()
        with pytest.raises(expected):
            dtr.set_time_range(start, end)


class Test_DateTimeRange_intersection:

    @pytest.mark.parametrize(["lhs", "rhs", "expected"], [
        [
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
        ],
        [
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:00:00 JST"),
            DateTimeRange(
                "2015-01-22T10:10:00 JST",
                "2015-03-22T10:20:00 JST"),
            DateTimeRange(None, None),
        ],
        [
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:00:00 JST"),
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-03-22T10:20:00 JST"),
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-01-22T10:00:00 JST"),
        ],
        [
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:05:00 JST"),
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-03-22T10:20:00 JST"),
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-01-22T10:05:00 JST"),
        ],
        [
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-03-22T10:20:00 JST"),
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:05:00 JST"),
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-01-22T10:05:00 JST"),
        ],
        [
            DateTimeRange(
                "2014-01-22T10:00:00 JST",
                "2016-03-22T10:20:00 JST"),
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:05:00 JST"),
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:05:00 JST"),
        ],
        [
            DateTimeRange(
                "2015-01-12T10:00:00 JST",
                "2015-02-22T10:10:00 JST"),
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-03-22T10:10:00 JST"),
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-02-22T10:10:00 JST"),
        ],
    ])
    def test_normal(self, lhs, rhs, expected):
        lhs.intersection(rhs)
        assert lhs == expected

    @pytest.mark.parametrize(["lhs", "rhs", "expected"], [
        [
            DateTimeRange(None, None),
            DateTimeRange(None, None),
            TypeError,
        ],
        [
            DateTimeRange(None, TEST_END_DATETIME),
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            TypeError,
        ],
        [
            DateTimeRange(TEST_END_DATETIME, TEST_START_DATETIME),
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            ValueError,
        ],
        [
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            DateTimeRange(None, TEST_END_DATETIME),
            TypeError,
        ],
        [
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            DateTimeRange(TEST_END_DATETIME, TEST_START_DATETIME),
            ValueError,
        ],
    ])
    def test_exception(self, lhs, rhs, expected):
        with pytest.raises(expected):
            lhs.intersection(rhs)


class Test_DateTimeRange_encompass:

    @pytest.mark.parametrize(["lhs", "rhs", "expected"], [
        [
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
        ],
        [
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:00:00 JST"),
            DateTimeRange(
                "2015-01-22T10:10:00 JST",
                "2015-01-22T10:20:00 JST"),
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:20:00 JST"),
        ],
        [
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:00:00 JST"),
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-01-22T10:20:00 JST"),
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:20:00 JST"),
        ],
        [
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:05:00 JST"),
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-01-22T10:20:00 JST"),
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:20:00 JST"),
        ],
        [
            DateTimeRange(
                "2015-01-22T10:00:00 JST",
                "2015-03-22T10:20:00 JST"),
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-01-22T10:05:00 JST"),
            DateTimeRange(
                "2015-01-22T09:50:00 JST",
                "2015-03-22T10:20:00 JST"),
        ],
    ])
    def test_normal(self, lhs, rhs, expected):
        lhs.encompass(rhs)
        assert lhs == expected

    @pytest.mark.parametrize(["lhs", "rhs", "expected"], [
        [
            DateTimeRange(None, None),
            DateTimeRange(None, None),
            TypeError,
        ],
        [
            DateTimeRange(None, TEST_END_DATETIME),
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            TypeError,
        ],
        [
            DateTimeRange(TEST_END_DATETIME, TEST_START_DATETIME),
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            ValueError,
        ],
        [
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            DateTimeRange(None, TEST_END_DATETIME),
            TypeError,
        ],
        [
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
            DateTimeRange(TEST_END_DATETIME, TEST_START_DATETIME),
            ValueError,
        ],
    ])
    def test_exception(self, lhs, rhs, expected):
        with pytest.raises(expected):
            lhs.encompass(rhs)


class Test_DateTimeRange_truncate:

    @pytest.mark.parametrize(["value", "expected"], [
        [
            0,
            DateTimeRange(TEST_START_DATETIME, TEST_END_DATETIME),
        ],
        [
            10,
            DateTimeRange(
                "2015-03-22 10:00:30" + TIMEZONE,
                "2015-03-22 10:09:30" + TIMEZONE),
        ],
    ])
    def test_normal(self, datetimerange_normal, value, expected):
        datetimerange_normal.truncate(value)
        assert datetimerange_normal == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [
            -10,
            ValueError,
        ],
    ])
    def test_exception(self, datetimerange_normal, value, expected):
        with pytest.raises(expected):
            datetimerange_normal.truncate(value)

    @pytest.mark.parametrize(["value"], [
        [10],
    ])
    def test_null(self, datetimerange_null_start, value):
        with pytest.raises(TypeError):
            datetimerange_null_start.truncate(value)
