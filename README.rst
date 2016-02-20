**DateTimeRange**

.. image:: https://travis-ci.org/thombashi/DateTimeRange.svg?branch=master
    :target: https://travis-ci.org/thombashi/DateTimeRange
.. image:: https://ci.appveyor.com/api/projects/status/jhy67bw2y3c8s016/branch/master?svg=true
   :target: https://ci.appveyor.com/project/thombashi/datetimerange/branch/master
.. image:: https://coveralls.io/repos/github/thombashi/DateTimeRange/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/DateTimeRange?branch=master

.. contents:: Table of contents
   :backlinks: top
   :local:

About
=====

Python library for time range.

Installation
============

::

    pip install DateTimeRange

Usage
=====

Create
------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    time_range

::

    2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900

Change output format
--------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    time_range.start_time_format = "%Y/%m/%d"
    time_range.end_time_format = "%Y/%m/%dT%H:%M:%S%z"
    time_range

::

    2015/03/22 - 2015/03/22T10:10:00+0900

Output elapsed time
-------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    time_range.is_output_elapse = True
    time_range

::

    2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900 (0:10:00)

Change separator
----------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    time_range.separator = " to "
    time_range

::

    2015-03-22T10:00:00+0900 to 2015-03-22T10:10:00+0900

Get start time as datetime
--------------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    time_range.start_datetime

::

    datetime.datetime(2015, 3, 22, 10, 0, tzinfo=tzoffset(None, 32400))

Get start time as string
------------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    print time_range.get_start_time_str()
    time_range.start_time_format = "%Y/%m/%d %H:%M:%S"
    print time_range.get_start_time_str()

::

    2015-03-22T10:00:00+0900
    2015/03/22 10:00:00

Get end time as datetime
------------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    time_range.end_datetime

::

    datetime.datetime(2015, 3, 22, 10, 10, tzinfo=tzoffset(None, 32400))

Get end time as string
----------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    print time_range.get_end_time_str()
    time_range.end_time_format = "%Y/%m/%d %H:%M:%S"
    print time_range.get_end_time_str()

::

    2015-03-22T10:10:00+0900
    2015/03/22 10:10:00

Get timedelta
-------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    time_range.timedelta

::

    datetime.timedelta(0, 600)

Get timedelta as seconds
------------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    time_range.get_timedelta_second()

::

    600.0

Set start time
--------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange()
    print time_range
    time_range.set_start_datetime("2015-03-22T10:00:00+0900")
    print time_range

::

    NaT - NaT
    2015-03-22T10:00:00+0900 - NaT

Set end time
------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange()
    print time_range
    time_range.set_end_datetime("2015-03-22T10:10:00+0900")
    print time_range

::

    NaT - NaT
    NaT - 2015-03-22T10:10:00+0900

Set time range
--------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange()
    print time_range
    time_range.set_time_range("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    print time_range

::

    NaT - NaT
    2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900

Check whether the time range is set or not
------------------------------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange()
    print time_range.is_set()
    time_range.set_time_range("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    print time_range.is_set()

::

    False
    True

Validate time inversion
-----------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:10:00+0900", "2015-03-22T10:00:00+0900")
    try:
        time_range.validate_time_inversion()
    except ValueError:
        print "time inversion"

::

    time inversion

Check whether the time range is valid or not
--------------------------------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange()
    print time_range.is_valid_timerange()
    time_range.set_time_range("2015-03-22T10:20:00+0900", "2015-03-22T10:10:00+0900")
    print time_range.is_valid_timerange()
    time_range.set_time_range("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    print time_range.is_valid_timerange()

::

    False
    False
    True

Check whether a value within the time range
-------------------------------------------

.. code:: python

    from datetimerange import DateTimeRange
    time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
    print "2015-03-22T10:05:00+0900" in time_range
    print "2015-03-22T10:15:00+0900" in time_range

::

    True
    False

Check whether a value intersect the time range
----------------------------------------------

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
    print time_range
    time_range.truncate(10)
    print time_range

::

    2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900 (0:10:00)
    2015-03-22T10:00:30+0900 - 2015-03-22T10:09:30+0900 (0:09:00)

Documentation
=============

http://datetimerange.readthedocs.org/en/latest/

Dependencies
============

Python 2.5+ or 3.3+

-  `python-dateutil <https://pypi.python.org/pypi/python-dateutil/>`__

Test dependencies
-----------------

-  `pytest <https://pypi.python.org/pypi/pytest>`__
-  `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
-  `tox <https://pypi.python.org/pypi/tox>`__
