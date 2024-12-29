<a id="v2.3.1"></a>
# [v2.3.1](https://github.com/thombashi/DateTimeRange/releases/tag/v2.3.1) - 2024-12-29

## What's Changed
* Drop support for Python 3.7/3.8
* Add support for Python 3.13
* Remove deprecated `tests_require` from `setup.py`
* Update copyright years
* Bump sigstore/gh-action-sigstore-python from 2.1.1 to 3.0.0 in the actions-dependencies group by [@dependabot](https://github.com/dependabot) in [#50](https://github.com/thombashi/DateTimeRange/pull/50)


**Full Changelog**: https://github.com/thombashi/DateTimeRange/compare/v2.3.0...v2.3.1

[Changes][v2.3.1]


<a id="v2.3.0"></a>
# [v2.3.0](https://github.com/thombashi/DateTimeRange/releases/tag/v2.3.0) - 2024-04-30

### New Features
* Add `is_time_inversion` method to `DateTimeRange` class
* Add `allow_timezone_mismatch` argument to `validate_time_inversion` method: [#49](https://github.com/thombashi/DateTimeRange/issues/49) (Thanks to [@darkweaver87](https://github.com/darkweaver87))

### Bug Fixes
* Fix the `range` method for when the timezone is mismatched between `start_datetime` and `end_datetime`: [#49](https://github.com/thombashi/DateTimeRange/issues/49) (Thanks to [@darkweaver87](https://github.com/darkweaver87))

---
**Full Changelog**: https://github.com/thombashi/DateTimeRange/compare/v2.2.1...v2.3.0

[Changes][v2.3.0]


<a id="v2.2.1"></a>
# [v2.2.1](https://github.com/thombashi/DateTimeRange/releases/tag/v2.2.1) - 2024-04-07

## What's Changed
* Bump actions/setup-python from 4 to 5 by [@dependabot](https://github.com/dependabot) in [#47](https://github.com/thombashi/DateTimeRange/pull/47)
* Fix an error that `DateTimeRange.intersection` method failed when the ranges are not overlapped and the `intersection_threshold` is not `None`: [#48](https://github.com/thombashi/DateTimeRange/issues/48) (Thanks to [@wernersa](https://github.com/wernersa))
* Keep the timezone when perform `__iadd__` or `__isub__` operations
* Add a build and publish workflow
* Add Sigstore signatures to release assets

## New Contributors
* [@dependabot](https://github.com/dependabot) made their first contribution in [#47](https://github.com/thombashi/DateTimeRange/pull/47)

**Full Changelog**: https://github.com/thombashi/DateTimeRange/compare/v2.2.0...v2.2.1

[Changes][v2.2.1]


<a id="v2.2.0"></a>
# [v2.2.0](https://github.com/thombashi/DateTimeRange/releases/tag/v2.2.0) - 2023-10-03

- Add `timezone` as an optional argument to `set_time_range` method, `from_range_text` method and the `DateTimeRange` class constructor
- Add `timezone` property to `DateTimeRange` class
- Add support for Python 3.12
- Change `start_time_format` and `end_time_format` of the `DateTimeRange` class constructor to optional arguments
  - Default format value would not be changed
- Fix type annotations of `set_start_datetime` and `set_end_datetime` methods
- Bump minimum `typepy` version to 1.3.2


[Changes][v2.2.0]


<a id="v2.1.1"></a>
# [v2.1.1](https://github.com/thombashi/DateTimeRange/releases/tag/v2.1.1) - 2023-10-01

- Add `__all__` to `__init__.py`
- Add `docs` extras
- Add `zip_safe=False`
- Add a classifier
- Update `[build-system]`
- Modify to use `pypa/build` for package build

**Full Changelog**: https://github.com/thombashi/DateTimeRange/compare/v2.1.0...v2.1.1

[Changes][v2.1.1]


<a id="v2.1.0"></a>
# [v2.1.0](https://github.com/thombashi/DateTimeRange/releases/tag/v2.1.0) - 2023-02-19

## What's Changed
* Add type annotations by [@hauntsaninja](https://github.com/hauntsaninja) in [#45](https://github.com/thombashi/DateTimeRange/pull/45)
* Changes to make `datetime.timedelta` and `dateutil.relativedelta.relativedelta` transparently usable for arguments.


## New Contributors
* [@hauntsaninja](https://github.com/hauntsaninja) made their first contribution in [#45](https://github.com/thombashi/DateTimeRange/pull/45)

**Full Changelog**: https://github.com/thombashi/DateTimeRange/compare/v2.0.0...v2.1.0

[Changes][v2.1.0]


<a id="v2.0.0"></a>
# [v2.0.0](https://github.com/thombashi/DateTimeRange/releases/tag/v2.0.0) - 2023-02-11

- Add `intersection_threshold` argument to `intersection`/`is_intersection` methods: [#43](https://github.com/thombashi/DateTimeRange/issues/43) (Thanks to [@usman5251](https://github.com/usman5251))
- Modify to accept regular expression for separator argument of `from_range_text` method: [#41](https://github.com/thombashi/DateTimeRange/issues/41) (Thanks to [@pantierra](https://github.com/pantierra))
- Fix the behavior of range when traversing from end to start: [#44](https://github.com/thombashi/DateTimeRange/issues/44) (Thanks to [@4l1fe](https://github.com/4l1fe))
- Drop support for Python 3.6
- Add support for Python 3.11

**Full Changelog**: https://github.com/thombashi/DateTimeRange/compare/v1.2.0...v2.0.0

[Changes][v2.0.0]


<a id="v1.2.0"></a>
# [v1.2.0](https://github.com/thombashi/DateTimeRange/releases/tag/v1.2.0) - 2021-07-10

- Add `DateTimeRange.from_range_text` class method: [#38](https://github.com/thombashi/DateTimeRange/issues/38) (Thanks to [@noamsgl](https://github.com/noamsgl))


[Changes][v1.2.0]


<a id="v1.1.0"></a>
# [v1.1.0](https://github.com/thombashi/DateTimeRange/releases/tag/v1.1.0) - 2021-06-09

- Add `subtract` method to `DateTimeRange` class: [#36](https://github.com/thombashi/DateTimeRange/issues/36) (Thanks to [@bramski](https://github.com/bramski))
- Add `split` method to `DateTimeRange` class
- Add support for Python 3.10
- Drop support for Python 3.5

[Changes][v1.1.0]


<a id="v0.5.0"></a>
# [v0.5.0](https://github.com/thombashi/DateTimeRange/releases/tag/v0.5.0) - 2018-10-31

- Change to return a new instance instead of changing the instance value itself when using `intersection`/`encompass` methods [#31](https://github.com/thombashi/DateTimeRange/issues/31) (Thanks to [@camelia-c](https://github.com/camelia-c))


[Changes][v0.5.0]


<a id="v0.4.0"></a>
# [v0.4.0](https://github.com/thombashi/DateTimeRange/releases/tag/v0.4.0) - 2018-10-30

- Add support for `datetime.date` class

[Changes][v0.4.0]


<a id="v0.3.6"></a>
# [v0.3.6](https://github.com/thombashi/DateTimeRange/releases/tag/v0.3.6) - 2018-09-15

- Add support for Python 3.7
- Update the package metadata

[Changes][v0.3.6]


<a id="v0.2.6"></a>
# [v0.2.6](https://github.com/thombashi/DateTimeRange/releases/tag/v0.2.6) - 2016-11-17

- Fix to apply dependent package update


[Changes][v0.2.6]


<a id="v0.2.5"></a>
# [v0.2.5](https://github.com/thombashi/DateTimeRange/releases/tag/v0.2.5) - 2016-08-11

- Refactoring


[Changes][v0.2.5]


<a id="v0.2.4"></a>
# [v0.2.4](https://github.com/thombashi/DateTimeRange/releases/tag/v0.2.4) - 2016-07-09

- Drop support for Python 2.6
- Fix datetime detection error with version strings


[Changes][v0.2.4]


<a id="v0.2.3"></a>
# [v0.2.3](https://github.com/thombashi/DateTimeRange/releases/tag/v0.2.3) - 2016-07-03



[Changes][v0.2.3]


<a id="v0.2.2"></a>
# [v0.2.2](https://github.com/thombashi/DateTimeRange/releases/tag/v0.2.2) - 2016-06-19

- Make pytest-runner a conditional requirement
- Drop support for Python 2.5


[Changes][v0.2.2]


<a id="v0.2.1"></a>
# [v0.2.1](https://github.com/thombashi/DateTimeRange/releases/tag/v0.2.1) - 2016-03-15

# Enhancement

[#12](https://github.com/thombashi/DateTimeRange/issues/12): Added support for datetimerange inclusion. Thanks to [@guyzmo](https://github.com/guyzmo)


[Changes][v0.2.1]


<a id="v0.2.0"></a>
# [v0.2.0](https://github.com/thombashi/DateTimeRange/releases/tag/v0.2.0) - 2016-03-10

# Enhancement
- Add range method to support iterator.


[Changes][v0.2.0]


<a id="v0.1.3"></a>
# [v0.1.3](https://github.com/thombashi/DateTimeRange/releases/tag/v0.1.3) - 2016-03-04

# Fix
- Fix [#8](https://github.com/thombashi/DateTimeRange/issues/8): correct daylight savings time processing. Thanks to [@tweyter](https://github.com/tweyter)


[Changes][v0.1.3]


<a id="v0.1.2"></a>
# [v0.1.2](https://github.com/thombashi/DateTimeRange/releases/tag/v0.1.2) - 2016-02-25

## Enhancement
- add operator support: `!=`, `+`, `+=`, `-`, `-=`


[Changes][v0.1.2]


<a id="v0.1.1"></a>
# [v0.1.1](https://github.com/thombashi/DateTimeRange/releases/tag/v0.1.1) - 2016-02-20



[Changes][v0.1.1]


<a id="v0.1.0"></a>
# [v0.1.0](https://github.com/thombashi/DateTimeRange/releases/tag/v0.1.0) - 2016-02-19



[Changes][v0.1.0]


[v2.3.1]: https://github.com/thombashi/DateTimeRange/compare/v2.3.0...v2.3.1
[v2.3.0]: https://github.com/thombashi/DateTimeRange/compare/v2.2.1...v2.3.0
[v2.2.1]: https://github.com/thombashi/DateTimeRange/compare/v2.2.0...v2.2.1
[v2.2.0]: https://github.com/thombashi/DateTimeRange/compare/v2.1.1...v2.2.0
[v2.1.1]: https://github.com/thombashi/DateTimeRange/compare/v2.1.0...v2.1.1
[v2.1.0]: https://github.com/thombashi/DateTimeRange/compare/v2.0.0...v2.1.0
[v2.0.0]: https://github.com/thombashi/DateTimeRange/compare/v1.2.0...v2.0.0
[v1.2.0]: https://github.com/thombashi/DateTimeRange/compare/v1.1.0...v1.2.0
[v1.1.0]: https://github.com/thombashi/DateTimeRange/compare/v0.5.0...v1.1.0
[v0.5.0]: https://github.com/thombashi/DateTimeRange/compare/v0.4.0...v0.5.0
[v0.4.0]: https://github.com/thombashi/DateTimeRange/compare/v0.3.6...v0.4.0
[v0.3.6]: https://github.com/thombashi/DateTimeRange/compare/v0.2.6...v0.3.6
[v0.2.6]: https://github.com/thombashi/DateTimeRange/compare/v0.2.5...v0.2.6
[v0.2.5]: https://github.com/thombashi/DateTimeRange/compare/v0.2.4...v0.2.5
[v0.2.4]: https://github.com/thombashi/DateTimeRange/compare/v0.2.3...v0.2.4
[v0.2.3]: https://github.com/thombashi/DateTimeRange/compare/v0.2.2...v0.2.3
[v0.2.2]: https://github.com/thombashi/DateTimeRange/compare/v0.2.1...v0.2.2
[v0.2.1]: https://github.com/thombashi/DateTimeRange/compare/v0.2.0...v0.2.1
[v0.2.0]: https://github.com/thombashi/DateTimeRange/compare/v0.1.3...v0.2.0
[v0.1.3]: https://github.com/thombashi/DateTimeRange/compare/v0.1.2...v0.1.3
[v0.1.2]: https://github.com/thombashi/DateTimeRange/compare/v0.1.1...v0.1.2
[v0.1.1]: https://github.com/thombashi/DateTimeRange/compare/v0.1.0...v0.1.1
[v0.1.0]: https://github.com/thombashi/DateTimeRange/tree/v0.1.0

<!-- Generated by https://github.com/rhysd/changelog-from-release v3.8.1 -->
