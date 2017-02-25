DateTimeRange
=============

.. image:: https://badge.fury.io/py/DateTimeRange.svg
    :target: https://badge.fury.io/py/DateTimeRange

.. image:: https://img.shields.io/pypi/pyversions/DateTimeRange.svg
   :target: https://pypi.python.org/pypi/DateTimeRange

.. image:: https://img.shields.io/travis/thombashi/DateTimeRange/master.svg?label=Linux
    :target: https://travis-ci.org/thombashi/DateTimeRange

.. image:: https://img.shields.io/appveyor/ci/thombashi/datetimerange/master.svg?label=Windows
   :target: https://ci.appveyor.com/project/thombashi/datetimerange/branch/master

.. image:: https://coveralls.io/repos/github/thombashi/DateTimeRange/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/DateTimeRange?branch=master

.. image:: https://img.shields.io/github/stars/thombashi/DateTimeRange.svg?style=social&label=Star
   :target: https://github.com/thombashi/DateTimeRange

Summary
-------

DateTimeRange is a python library to handle routine work associated with a time range,
such as test whether a time is within the time range,
get time range intersection, truncating the time range, etc.

Examples
========

Create and convert to string
----------------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    str(time_range)

::

    '2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900'

Get iterator
------------

.. code:: python

    import datetime
    from datetimerange import DateTimeRange

    time_range = DateTimeRange("2015-01-01T00:00:00+0900", "2015-01-04T00:00:00+0900")
    for value in time_range.range(datetime.timedelta(days=1)):
        print value

::

    2015-01-01 00:00:00+09:00
    2015-01-02 00:00:00+09:00
    2015-01-03 00:00:00+09:00
    2015-01-04 00:00:00+09:00

.. code:: python

    from datetimerange import DateTimeRange
    from dateutil.relativedelta import relativedelta

    time_range = DateTimeRange("2015-01-01T00:00:00+0900", "2016-01-01T00:00:00+0900")
    for value in time_range.range(relativedelta(months=+4)):
        print value

::

    2015-01-01 00:00:00+09:00
    2015-05-01 00:00:00+09:00
    2015-09-01 00:00:00+09:00
    2016-01-01 00:00:00+09:00

Test whether a value within the time range
------------------------------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    print "2015-03-22T10:05:00+0900" in time_range
    print "2015-03-22T10:15:00+0900" in time_range

    time_range_smaller = DateTimeRange("2015-03-22T10:03:00+0900", "2015-03-22T10:07:00+0900")
    print time_range_smaller in time_range

::

    True
    False
    True

Test whether a value intersect the time range
---------------------------------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    x = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
    time_range.is_intersection(x)

::

    True

Make an intersected time range
------------------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    x = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
    time_range.intersection(x)
    time_range

::

    2015-03-22T10:05:00+0900 - 2015-03-22T10:10:00+0900

Make an encompassed time range
------------------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    x = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
    time_range.encompass(x)
    time_range

::

    2015-03-22T10:00:00+0900 - 2015-03-22T10:15:00+0900

Truncate time range
-------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    time_range.is_output_elapse = True
    print "before truncate: ", time_range
    time_range.truncate(10)
    print "after truncate:  ", time_range

::

    before truncate:  2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900 (0:10:00)
    after truncate:   2015-03-22T10:00:30+0900 - 2015-03-22T10:09:30+0900 (0:09:00)

For more information
--------------------

More examples are available at 
http://datetimerange.rtfd.io/en/latest/pages/examples/index.html

Examples with IPython Notebook is also available at 
http://nbviewer.jupyter.org/github/thombashi/DateTimeRange/tree/master/ipynb/DateTimeRange.ipynb

Installation
============

::

    pip install DateTimeRange


Dependencies
============

Python 2.7 or 3.3+

- `python-dateutil <https://pypi.python.org/pypi/python-dateutil/>`__
- `typepy <https://github.com/thombashi/typepy>`__

Test dependencies
-----------------

-  `pytest <http://pytest.org/latest/>`__
-  `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
-  `tox <https://testrun.org/tox/latest/>`__

Documentation
=============

http://datetimerange.rtfd.io/

