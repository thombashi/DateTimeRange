# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import io
import os.path
import sys

import setuptools


MODULE_NAME = "DateTimeRange"
REPOSITORY_URL = "https://github.com/thombashi/{:s}".format(MODULE_NAME.lower())
REQUIREMENT_DIR = "requirements"
ENCODING = "utf8"

pkg_info = {}


with open(os.path.join(MODULE_NAME.lower(), "__version__.py")) as f:
    exec(f.read(), pkg_info)

with io.open("README.rst", encoding=ENCODING) as fp:
    long_description = fp.read()

with io.open(os.path.join("docs", "pages", "introduction", "summary.txt"), encoding=ENCODING) as f:
    summary = f.read().strip()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "docs_requirements.txt")) as f:
    docs_requires = [line.strip() for line in f if line.strip()]

needs_pytest = set(["pytest", "test", "ptr"]).intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []

setuptools.setup(
    name=MODULE_NAME,
    version=pkg_info["__version__"],
    url=REPOSITORY_URL,

    author=pkg_info["__author__"],
    author_email=pkg_info["__email__"],
    description=summary,
    include_package_data=True,
    keywords=["datetimerange", "date", "time", "range"],
    license=pkg_info["__license__"],
    long_description=long_description,
    packages=setuptools.find_packages(exclude=["test*"]),

    install_requires=install_requires,
    setup_requires=pytest_runner,
    tests_require=tests_requires,
    extras_require={
        "test": tests_requires,
        "docs": docs_requires,
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])
