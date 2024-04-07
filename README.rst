.. contents:: **DateTimeRange**
   :backlinks: top
   :depth: 2

Summary
=========
`DateTimeRange <https://github.com/thombashi/DateTimeRange>`__ is a Python library to handle a time range. e.g. check whether a time is within the time range, get the intersection of time ranges, truncate a time range, iterate through a time range, and so forth.

|PyPI pkg ver| |conda pkg ver| |Supported Python versions| |CI status| |Test coverage| |CodeQL|

.. |PyPI pkg ver| image:: https://badge.fury.io/py/DateTimeRange.svg
    :target: https://badge.fury.io/py/DateTimeRange
    :alt: PyPI package version

.. |conda pkg ver| image:: https://anaconda.org/conda-forge/datetimerange/badges/version.svg
    :target: https://anaconda.org/conda-forge/datetimerange
    :alt: conda-forge package version

.. |Supported Python versions| image:: https://img.shields.io/pypi/pyversions/DateTimeRange.svg
    :target: https://pypi.org/project/DateTimeRange
    :alt: Supported Python versions

.. |CI status| image:: https://github.com/thombashi/DateTimeRange/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/thombashi/DateTimeRange/actions/workflows/ci.yml
    :alt: CI status of Linux/macOS/Windows

.. |Test coverage| image:: https://coveralls.io/repos/github/thombashi/DateTimeRange/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/DateTimeRange?branch=master
    :alt: Test coverage

.. |CodeQL| image:: https://github.com/thombashi/DateTimeRange/actions/workflows/github-code-scanning/codeql/badge.svg
    :target: https://github.com/thombashi/DateTimeRange/actions/workflows/github-code-scanning/codeql
    :alt: CodeQL

Installation
============

Installation: pip
------------------------------
::

    pip install DateTimeRange


Installation: conda
------------------------------
::

    conda install -c conda-forge datetimerange


Dependencies
============
- Python 3.7+
- `Python package dependencies (automatically installed) <https://github.com/thombashi/DateTimeRange/network/dependencies>`__

Features
============
Features of ``DateTimeRange`` class include:

- Supported operations:
    - Equation
    - Addition
    - Subtraction
    - Intersection
    - Union
    - Contains
    - Truncate
    - Split
    - Iteration
- Timezone support
- Daylight saving time support

Examples
==========
Create a DateTimeRange instance from start and end datetime
-----------------------------------------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        str(time_range)

:Output:
    ::

        '2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900'

Create a DateTimeRange instance from a range text
-----------------------------------------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange.from_range_text("2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900")
        str(time_range)

:Output:
    ::

        '2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900'

Get an iterator
------------------------
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

Test whether a value intersects the time range
----------------------------------------------
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

Examples with Jupyter Notebook are also available at `DateTimeRange.ipynb <https://nbviewer.jupyter.org/github/thombashi/DateTimeRange/tree/master/examples/DateTimeRange.ipynb>`__

Documentation
===============
https://datetimerange.rtfd.io/

Sponsors
====================================
.. image:: https://avatars.githubusercontent.com/u/3658062?s=48&v=4
   :target: https://github.com/b4tman
   :alt: Dmitry Belyaev (b4tman)
.. image:: https://avatars.githubusercontent.com/u/44389260?s=48&u=6da7176e51ae2654bcfd22564772ef8a3bb22318&v=4
   :target: https://github.com/chasbecker
   :alt: Charles Becker (chasbecker)
.. image:: https://avatars.githubusercontent.com/u/46711571?s=48&u=57687c0e02d5d6e8eeaf9177f7b7af4c9f275eb5&v=4
   :target: https://github.com/Arturi0
   :alt: Arturi0

`Become a sponsor <https://github.com/sponsors/thombashi>`__

