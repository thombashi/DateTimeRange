import time
from datetime import datetime, timedelta, timezone

import pytest
from dateutil.tz import tzstr

from datetimerange import DateTimeRange


@pytest.fixture(params=[None, "UTC0", "JST-9", "EST5", "EST5EDT,M3.2.0/2,M11.1.0/2"])
def local_timezone(request, monkeypatch):
    if request.param is None:
        yield
        return
    if not hasattr(time, "tzset"):
        pytest.skip("Changing the process timezone requires time.tzset")

    # Restore both the environment and libc timezone, even when a test fails.
    with monkeypatch.context() as patch:
        patch.setenv("TZ", request.param)
        time.tzset()
        try:
            yield
        finally:
            patch.undo()
            time.tzset()


def assert_validation(start, end, inverted):
    value = DateTimeRange(start, end)
    for allow_timezone_mismatch in (True, False):
        assert value.is_time_inversion(allow_timezone_mismatch) is inverted
        if inverted:
            with pytest.raises(ValueError, match="time inversion found"):
                value.validate_time_inversion(allow_timezone_mismatch)
        else:
            assert value.validate_time_inversion(allow_timezone_mismatch) is None
    assert value.is_valid_timerange() is not inverted


@pytest.mark.usefixtures("local_timezone")
@pytest.mark.parametrize(
    "start, end, inverted",
    [
        ("0001-01-01", "2026-01-10", False),
        ("0001-01-01", "0001-01-01", False),
        ("0001-01-02", "0001-01-01", True),
        ("9999-12-31T23:59:59.999998", "9999-12-31T23:59:59.999999", False),
        ("9999-12-31T23:59:59.999999", "9999-12-31T23:59:59.999998", True),
        (datetime.min, datetime.max, False),
        (datetime.min, datetime.min, False),
        (datetime.max, datetime.max, False),
        (datetime.min, datetime.min + timedelta(microseconds=1), False),
        (datetime.min + timedelta(microseconds=1), datetime.min, True),
        (datetime.max - timedelta(microseconds=1), datetime.max, False),
        (datetime.max, datetime.min, True),
        # Naive wall-clock ordering must not depend on local DST gap/fold rules.
        (datetime(2022, 3, 13, 2, 30), datetime(2022, 3, 13, 3), False),
        (datetime(2022, 11, 6, 1, 30, fold=0), datetime(2022, 11, 6, 1, 15, fold=1), True),
    ],
)
def test_naive_validation(start, end, inverted):
    assert_validation(start, end, inverted)


@pytest.mark.usefixtures("local_timezone")
@pytest.mark.parametrize("start, end", [(None, None), (None, datetime.min), (datetime.max, None)])
def test_missing_endpoints(start, end):
    value = DateTimeRange(start, end)
    for allow_timezone_mismatch in (True, False):
        with pytest.raises(ValueError, match="range is not set"):
            value.is_time_inversion(allow_timezone_mismatch)
        with pytest.raises(TypeError):
            value.validate_time_inversion(allow_timezone_mismatch)
    assert not value.is_valid_timerange()


@pytest.mark.usefixtures("local_timezone")
@pytest.mark.parametrize("reverse", [False, True])
def test_aware_utc_order_and_mismatch(reverse):
    # Wall-clock order is opposite to UTC order.
    endpoints = ["2022-10-30T02:30:00+0200", "2022-10-30T02:15:00+0100"]
    if reverse:
        endpoints.reverse()
    value = DateTimeRange(endpoints[0], endpoints[1])
    assert value.is_time_inversion() is reverse
    assert value.is_valid_timerange() is not reverse
    if reverse:
        with pytest.raises(ValueError, match="time inversion found"):
            value.validate_time_inversion()
    else:
        value.validate_time_inversion()
    for method in (value.is_time_inversion, value.validate_time_inversion):
        with pytest.raises(ValueError, match="timezone mismatch"):
            method(allow_timezone_mismatch=False)


@pytest.mark.usefixtures("local_timezone")
def test_aware_equal_instants():
    value = DateTimeRange("2022-10-30T02:30:00+0200", "2022-10-30T01:30:00+0100")
    assert not value.is_time_inversion()
    value.validate_time_inversion()
    assert value.is_valid_timerange()
    for method in (value.is_time_inversion, value.validate_time_inversion):
        with pytest.raises(ValueError, match="timezone mismatch"):
            method(allow_timezone_mismatch=False)


@pytest.mark.usefixtures("local_timezone")
def test_aware_utc_boundaries():
    start = datetime.min.replace(tzinfo=timezone.utc)
    end = datetime.max.replace(tzinfo=timezone.utc)
    assert_validation(start, end, False)
    assert_validation(end, start, True)


@pytest.mark.usefixtures("local_timezone")
@pytest.mark.parametrize(
    "endpoint",
    [
        datetime.min.replace(tzinfo=timezone(timedelta(hours=1))),
        datetime.max.replace(tzinfo=timezone(timedelta(hours=-1))),
    ],
)
def test_aware_utc_overflow_contract(endpoint):
    value = DateTimeRange(endpoint, endpoint)
    # Do not turn an unrepresentable aware UTC conversion into a valid range.
    for method in (value.is_time_inversion, value.validate_time_inversion, value.is_valid_timerange):
        with pytest.raises(OverflowError):
            method()


@pytest.mark.usefixtures("local_timezone")
@pytest.mark.parametrize("reverse", [False, True])
def test_aware_fold_order(reverse):
    # POSIX rules avoid relying on the host's zoneinfo database (e.g. Windows).
    zone = tzstr("EST5EDT,M3.2.0/2,M11.1.0/2")
    start = datetime(2022, 11, 6, 1, 30, tzinfo=zone, fold=0)
    end = datetime(2022, 11, 6, 1, 15, tzinfo=zone, fold=1)
    assert start.utcoffset() == timedelta(hours=-4)
    assert end.utcoffset() == timedelta(hours=-5)
    if reverse:
        start, end = end, start
    assert_validation(start, end, reverse)


@pytest.mark.usefixtures("local_timezone")
@pytest.mark.parametrize("reverse", [False, True])
def test_mixed_naive_aware_preserves_local_time_contract(reverse):
    start = datetime(2022, 6, 1, 12)
    # Existing mixed-timezone semantics interpret the naive endpoint as local time.
    end = start.astimezone(timezone.utc) + timedelta(minutes=1)
    if reverse:
        start, end = end, start
    value = DateTimeRange(start, end)
    assert value.is_time_inversion() is reverse
    assert value.is_valid_timerange() is not reverse
    if reverse:
        with pytest.raises(ValueError, match="time inversion found"):
            value.validate_time_inversion()
    else:
        value.validate_time_inversion()
    for method in (value.is_time_inversion, value.validate_time_inversion):
        with pytest.raises(ValueError, match="timezone mismatch"):
            method(allow_timezone_mismatch=False)


@pytest.mark.usefixtures("local_timezone")
def test_boundary_validation_consumers():
    start = datetime.min
    middle = start + timedelta(days=1)
    end = start + timedelta(days=2)
    value = DateTimeRange(start, end)
    inner = DateTimeRange(start, middle)
    assert middle in value
    assert inner in value
    assert value.intersection(inner) == inner
    assert value.encompass(inner) == value
    assert value.split(middle) == [inner, DateTimeRange(middle, end)]
    assert list(value.range(timedelta(days=1))) == [start, middle, end]
    assert list(DateTimeRange(end, middle).range(timedelta(days=-1))) == [end, middle]
