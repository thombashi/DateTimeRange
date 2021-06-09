.. contents:: **DateTimeRange**
   :backlinks: top
   :depth: 2

Summary
=========
`DateTimeRange <https://github.com/thombashi/DateTimeRange>`__ is a Python library to handle a time range. e.g. check whether a time is within the time range, get the intersection of time ranges, truncating a time range, iterate through a time range, and so forth.

.. image:: https://badge.fury.io/py/DateTimeRange.svg
    :target: https://badge.fury.io/py/DateTimeRange
    :alt: PyPI package version

.. image:: https://img.shields.io/pypi/pyversions/DateTimeRange.svg
    :target: https://pypi.org/project/DateTimeRange
    :alt: Supported Python versions

.. image:: https://github.com/thombashi/DateTimeRange/workflows/Tests/badge.svg
    :target: https://github.com/thombashi/DateTimeRange/actions/workflows/tests.yml
    :alt: Test result of Linux/macOS/Windows

.. image:: https://coveralls.io/repos/github/thombashi/DateTimeRange/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/DateTimeRange?branch=master
    :alt: Test coverage

.. image:: https://img.shields.io/github/stars/thombashi/DateTimeRange.svg?style=social&label=Star
    :target: https://github.com/thombashi/DateTimeRange
    :alt: GitHub stars

Examples
==========
Create and convert to string
----------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        str(time_range)

:Output:
    ::

        '2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900'

Get iterator
------------
:Sample Code 1:
    .. code:: python

        import datetime
        from datetimerange import DateTimeRange

        time_range = DateTimeRange("2015-01-01T00:00:00+0900", "2015-01-04T00:00:00+0900")
        for value in time_range.range(datetime.timedelta(days=1)):
            print(value)

:Output 1:
    ::

        2015-01-01 00:00:00+09:00
        2015-01-02 00:00:00+09:00
        2015-01-03 00:00:00+09:00
        2015-01-04 00:00:00+09:00

:Sample Code 2:
    .. code:: python

        from datetimerange import DateTimeRange
        from dateutil.relativedelta import relativedelta

        time_range = DateTimeRange("2015-01-01T00:00:00+0900", "2016-01-01T00:00:00+0900")
        for value in time_range.range(relativedelta(months=+4)):
            print(value)

:Output 2:
    ::

        2015-01-01 00:00:00+09:00
        2015-05-01 00:00:00+09:00
        2015-09-01 00:00:00+09:00
        2016-01-01 00:00:00+09:00

Test whether a value within the time range
------------------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange

        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        print("2015-03-22T10:05:00+0900" in time_range)
        print("2015-03-22T10:15:00+0900" in time_range)

        time_range_smaller = DateTimeRange("2015-03-22T10:03:00+0900", "2015-03-22T10:07:00+0900")
        print(time_range_smaller in time_range)

:Output:
    ::

        True
        False
        True

Test whether a value intersect the time range
---------------------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        x = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
        time_range.is_intersection(x)

:Output:
    ::

        True

Make an intersected time range
------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        x = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
        time_range.intersection(x)

:Output:
    ::

        2015-03-22T10:05:00+0900 - 2015-03-22T10:10:00+0900

Make an encompassed time range
------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        x = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
        time_range.encompass(x)

:Output:
    ::

        2015-03-22T10:00:00+0900 - 2015-03-22T10:15:00+0900

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

For more information
----------------------
More examples are available at 
https://datetimerange.rtfd.io/en/latest/pages/examples/index.html

Examples with Jupyter Notebook is also available at `DateTimeRange.ipynb <https://nbviewer.jupyter.org/github/thombashi/DateTimeRange/tree/master/examples/DateTimeRange.ipynb>`__

Installation
============

::

    pip install DateTimeRange


Dependencies
============
- Python 3.6+
- `Python package dependencies (automatically installed) <https://github.com/thombashi/DateTimeRange/network/dependencies>`__

Documentation
===============
https://datetimerange.rtfd.io/

Sponsors
====================================
.. image:: https://avatars0.githubusercontent.com/u/44389260?s=48&u=6da7176e51ae2654bcfd22564772ef8a3bb22318&v=4
   :target: https://github.com/chasbecker
   :alt: Charles Becker (chasbecker)

`Become a sponsor <https://github.com/sponsors/thombashi>`__

