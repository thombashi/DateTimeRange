from __future__ import with_statement
import setuptools


with open("README.rst") as fp:
    long_description = fp.read()

with open("requirements.txt") as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open("test_requirements.txt") as f:
    tests_require = [line.strip() for line in f if line.strip()]

setuptools.setup(
    name="DateTimeRange",
    version="0.1.2",
    author="Tsuyoshi Hombashi",
    author_email="gogogo.vm@gmail.com",
    url="https://github.com/thombashi/DateTimeRange",
    description="""
    Python library to handle the routine work associated with the time range,
    such as test whether a time is within the time range,
    get time intersection, truncating time etc.
    """,
    keywords="date time range",
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
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
