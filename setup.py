from __future__ import with_statement
import sys
import setuptools


with open("README.rst") as fp:
    long_description = fp.read()

with open("requirements.txt") as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open("test_requirements.txt") as f:
    tests_require = [line.strip() for line in f if line.strip()]

setuptools.setup(
    name="DateTimeRange",
    version="0.1.0",
    author="Tsuyoshi Hombashi",
    author_email="gogogo.vm@gmail.com",
    url="https://github.com/thombashi/DateTimeRange",
    description="Python library for time of range.",
    long_description=long_description,
    license="MIT License",
    include_package_data=True,
    packages=setuptools.find_packages(exclude=['test*']),
    install_requires=install_requires,
    setup_requires=["pytest-runner"],
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
