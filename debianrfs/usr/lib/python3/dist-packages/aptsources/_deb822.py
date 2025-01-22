#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) Canonical Ltd
#
# SPDX-License-Identifier: GPL-2.0+

"""deb822 parser with support for comment headers and footers."""

import io
import collections
import typing

import apt_pkg


T = typing.TypeVar("T")


class Section:
    """A single deb822 section, possibly with comments.

    This represents a single deb822 section.
    """

    def __init__(self, section: str):
        comments = ["", ""]
        in_section = False
        trimmed_section = ""

        for line in section.split("\n"):
            if line.startswith("#"):
                # remove the leading #
                line = line[1:]
                comments[in_section] += line + "\n"
                continue

            in_section = True
            trimmed_section += line + "\n"

        self.tags = collections.OrderedDict(apt_pkg.TagSection(trimmed_section))
        self.header, self.footer = comments

    def __getitem__(self, key: str) -> str:
        """Get the value of a field."""
        return self.tags[key]

    def __delitem__(self, key: str) -> None:
        """Delete a field"""
        del self.tags[key]

    def __setitem__(self, key: str, val: str) -> None:
        """Set the value of a field."""
        self.tags[key] = val

    def __bool__(self) -> bool:
        return bool(self.tags)

    @typing.overload
    def get(self, key: str) -> typing.Optional[str]:
        ...

    @typing.overload
    def get(self, key: str, default: T) -> typing.Union[T, str]:
        ...

    def get(
        self, key: str, default: typing.Optional[T] = None
    ) -> typing.Union[typing.Optional[T], str]:
        try:
            return self.tags[key]
        except KeyError:
            return default

    @staticmethod
    def __comment_lines(content: str) -> str:
        return (
            "\n".join("#" + line for line in content.splitlines()) + "\n"
            if content
            else ""
        )

    def __str__(self) -> str:
        """Canonical string rendering of this section."""
        return (
            self.__comment_lines(self.header)
            + "".join(f"{k}: {v}\n" for k, v in self.tags.items())
            + self.__comment_lines(self.footer)
        )


class File:
    """
    Parse a given file object into a list of Section objects.
    """

    def __init__(self, fobj: io.TextIOBase):
        sections = fobj.read().split("\n\n")
        self.sections = [Section(s) for s in sections]

    def __iter__(self) -> typing.Iterator[Section]:
        return iter(self.sections)

    def __str__(self) -> str:
        return "\n\n".join(str(s) for s in self.sections)


if __name__ == "__main__":
    st = """# Header
# More header
K1: V1
# Inline
K2: V2
 # not a comment
# Footer
# More footer
"""

    s = Section(st)

    print(s)
