<a name="v2.3.0"></a>
# [v2.3.0](https://github.com/thombashi/DateTimeRange/releases/tag/v2.3.0) - 30 Apr 2024

### New Features
* Add `is_time_inversion` method to `DateTimeRange` class
* Add `allow_timezone_mismatch` argument to `validate_time_inversion` method: [#49](https://github.com/thombashi/DateTimeRange/issues/49) (Thanks to [@darkweaver87](https://github.com/darkweaver87))

### Bug Fixes
* Fix the `range` method for when the timezone is mismatched between `start_datetime` and `end_datetime`: [#49](https://github.com/thombashi/DateTimeRange/issues/49) (Thanks to [@darkweaver87](https://github.com/darkweaver87))

---
**Full Changelog**: https://github.com/thombashi/DateTimeRange/compare/v2.2.1...v2.3.0

[Changes][v2.3.0]


<a name="v2.2.1"></a>
# [v2.2.1](https://github.com/thombashi/DateTimeRange/releases/tag/v2.2.1) - 07 Apr 2024

## What's Changed
* Bump actions/setup-python from 4 to 5 by [@dependabot](https://github.com/dependabot) in https://github.com/thombashi/DateTimeRange/pull/47
* Fix an error that `DateTimeRange.intersection` method failed when the ranges are not overlapped and the `intersection_threshold` is not `None`: [#48](https://github.com/thombashi/DateTimeRange/issues/48) (Thanks to [@wernersa](https://github.com/wernersa))
* Keep the timezone when perform `__iadd__` or `__isub__` operations
* Add a build and publish workflow
* Add Sigstore signatures to release assets

## New Contributors
* [@dependabot](https://github.com/dependabot) made their first contribution in https://github.com/thombashi/DateTimeRange/pull/47

**Full Changelog**: https://github.com/thombashi/DateTimeRange/compare/v2.2.0...v2.2.1

[Changes][v2.2.1]


<a name="v2.2.0"></a>
# [v2.2.0](https://github.com/thombashi/DateTimeRange/releases/tag/v2.2.0) - 03 Oct 2023

- Add `timezone` as an optional argument to `set_time_range` method, `from_range_text` method and the `DateTimeRange` class constructor
- Add `timezone` property to `DateTimeRange` class
- Add support for Python 3.12
- Change `start_time_format` and `end_time_format` of the `DateTimeRange` class constructor to optional arguments
  - Default format value would not be changed
- Fix type annotations of `set_start_datetime` and `set_end_datetime` methods
- Bump minimum `typepy` version to 1.3.2


[Changes][v2.2.0]


<a name="v2.1.1"></a>
# [v2.1.1](https://github.com/thombashi/DateTimeRange/releases/tag/v2.1.1) - 01 Oct 2023

- Add `__all__` to `__init__.py`
- Add `docs` extras
- Add `zip_safe=False`
- Add a classifier
- Update `[build-system]`
- Modify to use `pypa/build` for package build

**Full Changelog**: https://github.com/thombashi/DateTimeRange/compare/v2.1.0...v2.1.1

[Changes][v2.1.1]


<a name="v2.1.0"></a>
# [v2.1.0](https://github.com/thombashi/DateTimeRange/releases/tag/v2.1.0) - 19 Feb 2023

## What's Changed
* Add type annotations by [@hauntsaninja](https://github.com/hauntsaninja) in https://github.com/thombashi/DateTimeRange/pull/45
* Changes to make `datetime.timedelta` and `dateutil.relativedelta.relativedelta` transparently usable for arguments.


## New Contributors
* [@hauntsaninja](https://github.com/hauntsaninja) made their first contribution in https://github.com/thombashi/DateTimeRange/pull/45

**Full Changelog**: https://github.com/thombashi/DateTimeRange/compare/v2.0.0...v2.1.0

[Changes][v2.1.0]


<a name="v2.0.0"></a>
# [v2.0.0](https://github.com/thombashi/DateTimeRange/releases/tag/v2.0.0) - 11 Feb 2023

- Add `intersection_threshold` argument to `intersection`/`is_intersection` methods: [#43](https://github.com/thombashi/DateTimeRange/issues/43) (Thanks to [@usman5251](https://github.com/usman5251))
- Modify to accept regular expression for separator argument of `from_range_text` method: [#41](https://github.com/thombashi/DateTimeRange/issues/41) (Thanks to [@pantierra](https://github.com/pantierra))
- Fix the behavior of range when traversing from end to start: [#44](https://github.com/thombashi/DateTimeRange/issues/44) (Thanks to [@4l1fe](https://github.com/4l1fe))
- Drop support for Python 3.6
- Add support for Python 3.11

**Full Changelog**: https://github.com/thombashi/DateTimeRange/compare/v1.2.0...v2.0.0

[Changes][v2.0.0]


<a name="v1.2.0"></a>
# [v1.2.0](https://github.com/thombashi/DateTimeRange/releases/tag/v1.2.0) - 10 Jul 2021

- Add `DateTimeRange.from_range_text` class method: [#38](https://github.com/thombashi/DateTimeRange/issues/38) (Thanks to [@noamsgl](https://github.com/noamsgl))


[Changes][v1.2.0]


<a name="v1.1.0"></a>
# [v1.1.0](https://github.com/thombashi/DateTimeRange/releases/tag/v1.1.0) - 09 Jun 2021

- Add `subtract` method to `DateTimeRange` class: [#36](https://github.com/thombashi/DateTimeRange/issues/36) (Thanks to [@bramski](https://github.com/bramski))
- Add `split` method to `DateTimeRange` class
- Add support for Python 3.10
- Drop support for Python 3.5

[Changes][v1.1.0]


<a name="v0.5.0"></a>
# [v0.5.0](https://github.com/thombashi/DateTimeRange/releases/tag/v0.5.0) - 31 Oct 2018

- Change to return a new instance instead of changing the instance value itself when using `intersection`/`encompass` methods [#31](https://github.com/thombashi/DateTimeRange/issues/31) (Thanks to [@camelia-c](https://github.com/camelia-c))


[Changes][v0.5.0]


<a name="v0.4.0"></a>
# [v0.4.0](https://github.com/thombashi/DateTimeRange/releases/tag/v0.4.0) - 30 Oct 2018

- Add support for `datetime.date` class

[Changes][v0.4.0]


<a name="v0.3.6"></a>
# [v0.3.6](https://github.com/thombashi/DateTimeRange/releases/tag/v0.3.6) - 15 Sep 2018

- Add support for Python 3.7
- Update the package metadata

[Changes][v0.3.6]


<a name="v0.2.6"></a>
# [v0.2.6](https://github.com/thombashi/DateTimeRange/releases/tag/v0.2.6) - 17 Nov 2016

- Fix to apply dependent package update


[Changes][v0.2.6]


<a name="v0.2.5"></a>
# [v0.2.5](https://github.com/thombashi/DateTimeRange/releases/tag/v0.2.5) - 11 Aug 2016

- Refactoring


[Changes][v0.2.5]


<a name="v0.2.4"></a>
# [v0.2.4](https://github.com/thombashi/DateTimeRange/releases/tag/v0.2.4) - 09 Jul 2016

- Drop support for Python 2.6
- Fix datetime detection error with version strings


[Changes][v0.2.4]


<a name="v0.2.3"></a>
# [v0.2.3](https://github.com/thombashi/DateTimeRange/releases/tag/v0.2.3) - 03 Jul 2016



[Changes][v0.2.3]


<a name="v0.2.2"></a>
# [v0.2.2](https://github.com/thombashi/DateTimeRange/releases/tag/v0.2.2) - 19 Jun 2016

- Make pytest-runner a conditional requirement
- Drop support for Python 2.5


[Changes][v0.2.2]


<a name="v0.2.1"></a>
# [v0.2.1](https://github.com/thombashi/DateTimeRange/releases/tag/v0.2.1) - 15 Mar 2016

# Enhancement

[#12](https://github.com/thombashi/DateTimeRange/issues/12): Added support for datetimerange inclusion. Thanks to [@guyzmo](https://github.com/guyzmo)


[Changes][v0.2.1]


<a name="v0.2.0"></a>
# [v0.2.0](https://github.com/thombashi/DateTimeRange/releases/tag/v0.2.0) - 10 Mar 2016

# Enhancement
- Add range method to support iterator.


[Changes][v0.2.0]


<a name="v0.1.3"></a>
# [v0.1.3](https://github.com/thombashi/DateTimeRange/releases/tag/v0.1.3) - 04 Mar 2016

# Fix
- Fix [#8](https://github.com/thombashi/DateTimeRange/issues/8): correct daylight savings time processing. Thanks to [@tweyter](https://github.com/tweyter)


[Changes][v0.1.3]


<a name="v0.1.2"></a>
# [v0.1.2](https://github.com/thombashi/DateTimeRange/releases/tag/v0.1.2) - 25 Feb 2016

## Enhancement
- add operator support: `!=`, `+`, `+=`, `-`, `-=`


[Changes][v0.1.2]


<a name="v0.1.1"></a>
# [v0.1.1](https://github.com/thombashi/DateTimeRange/releases/tag/v0.1.1) - 20 Feb 2016



[Changes][v0.1.1]


<a name="v0.1.0"></a>
# [v0.1.0](https://github.com/thombashi/DateTimeRange/releases/tag/v0.1.0) - 19 Feb 2016



[Changes][v0.1.0]


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

<!-- Generated by https://github.com/rhysd/changelog-from-release v3.7.2 -->
