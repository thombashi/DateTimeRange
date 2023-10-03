#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import os.path
import sys

from path import Path
from readmemaker import ReadmeMaker


PROJECT_NAME = "DateTimeRange"
OUTPUT_DIR = ".."


def write_examples(maker):
    maker.set_indent_level(0)
    maker.write_chapter("Examples")

    example_root = Path(os.path.join("pages", "examples"))
    example_files = [
        "Create_and_convert_to_string.rst",
        "Create_from_a_string.rst",
        "Get_iterator.rst",
        "Test_whether_a_value_within_the_time_range.rst",
        "Test_whether_a_value_intersect_the_time_range.rst",
        "Make_an_intersected_time_range.rst",
        "Make_an_encompassed_time_range.rst",
        "Truncate_time_range.rst",
    ]

    for example_file in example_files:
        maker.write_file(example_root.joinpath(example_file))

    maker.inc_indent_level()
    maker.write_chapter("For more information")
    maker.write_lines(
        [
            "More examples are available at ",
            "https://datetimerange.rtfd.io/en/latest/pages/examples/index.html",
            "",
            "Examples with Jupyter Notebook are also available at "
            "`DateTimeRange.ipynb <https://nbviewer.jupyter.org/github/thombashi/DateTimeRange/"
            "tree/master/examples/DateTimeRange.ipynb>`__",
        ]
    )


def main():
    maker = ReadmeMaker(
        PROJECT_NAME,
        OUTPUT_DIR,
        is_make_toc=True,
        project_url=f"https://github.com/thombashi/{PROJECT_NAME}",
    )

    maker.write_chapter("Summary")
    maker.write_introduction_file("summary.txt")
    maker.write_introduction_file("badges.txt")
    maker.write_introduction_file("installation.rst")
    maker.write_introduction_file("features.rst")

    write_examples(maker)

    maker.set_indent_level(0)
    maker.write_chapter("Documentation")
    maker.write_lines(["https://datetimerange.rtfd.io/"])

    maker.write_file(maker.doc_page_root_dir_path.joinpath("sponsors.rst"))

    return 0


if __name__ == "__main__":
    sys.exit(main())
