PACKAGE := DateTimeRange

BIN_DIR := $(shell pwd)/bin
BUILD_WORK_DIR := _work
PKG_BUILD_DIR := $(BUILD_WORK_DIR)/$(PACKAGE)

PYTHON := python3
BIN_CHANGELOG_FROM_RELEASE := $(BIN_DIR)/changelog-from-release

AUTHOR := Tsuyoshi Hombashi
FIRST_RELEASE_YEAR := 2016
LAST_UPDATE_YEAR := $(shell git log -1 --format=%cd --date=format:%Y)


$(BIN_CHANGELOG_FROM_RELEASE):
	GOBIN=$(BIN_DIR) go install github.com/rhysd/changelog-from-release/v3@latest

.PHONY: build-remote
build-remote: clean
	@mkdir -p $(BUILD_WORK_DIR)
	@cd $(BUILD_WORK_DIR) && \
		git clone https://github.com/thombashi/$(PACKAGE).git --depth 1 && \
		cd $(PACKAGE) && \
		$(PYTHON) -m tox -e build
	ls -lh $(PKG_BUILD_DIR)/dist/*

.PHONY: build
build: clean
	$(PYTHON) -m tox -e build
	ls -lh dist/*

.PHONY: changelog
changelog: $(BIN_CHANGELOG_FROM_RELEASE)
	$(BIN_CHANGELOG_FROM_RELEASE) > CHANGELOG.md
	cp -a CHANGELOG.md docs/pages/CHANGELOG.md

.PHONY: check
check:
	$(PYTHON) -m tox -e lint

.PHONY: clean
clean:
	rm -rf $(BIN_DIR) $(BUILD_WORK_DIR)
	$(PYTHON) -m tox -e clean

.PHONY: docs
docs:
	@$(PYTHON) -m tox -e docs

.PHONY: fmt
fmt:
	$(PYTHON) -m tox -e fmt

.PHONY: readme
readme:
	$(PYTHON) -m tox -e readme

.PHONY: release
release:
	$(PYTHON) -m tox -e release
	$(MAKE) clean

.PHONY: setup-ci
setup-ci:
	$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade pip
	$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade tox

.PHONY: setup-dev
setup-dev: setup-ci
	$(PYTHON) -m pip install --upgrade -e .[test]
	$(PYTHON) -m pip check

.PHONY: test
test:
	$(PYTHON) -m tox -e py

.PHONY: update-copyright
update-copyright:
	sed -i "s/^__copyright__ = .*/__copyright__ = f\"Copyright $(FIRST_RELEASE_YEAR)-$(LAST_UPDATE_YEAR), {__author__}\"/" datetimerange/__version__.py
	sed -i "s/^Copyright (c) .* $(AUTHOR)/Copyright (c) $(FIRST_RELEASE_YEAR)-$(LAST_UPDATE_YEAR) $(AUTHOR)/" LICENSE
