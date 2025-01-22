#  sourceslist.py - Provide an abstraction of the sources.list
#
#  Copyright (c) 2004-2023 Canonical Ltd.
#  Copyright (c) 2004 Michiel Sikkes
#  Copyright (c) 2006-2007 Sebastian Heinlein
#
#  Authors: Michiel Sikkes <michiel@eyesopened.nl>
#           Michael Vogt <mvo@debian.org>
#           Sebastian Heinlein <glatzor@ubuntu.com>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation; either version 2 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
#  USA

from __future__ import absolute_import, print_function

import glob
import io
import logging
import os.path
import re
import shutil
import time
from typing import (
    Any,
    Dict,
    Callable,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

import apt_pkg
from .distinfo import DistInfo, Template
from . import _deb822

# from apt_pkg import gettext as _

T = TypeVar("T")

# some global helpers

__all__ = [
    "is_mirror",
    "Deb822SourceEntry",
    "SourceEntry",
    "NullMatcher",
    "SourcesList",
    "SourceEntryMatcher",
]


def is_mirror(master_uri: str, compare_uri: str) -> bool:
    """check if the given add_url is idential or a mirror of orig_uri e.g.:
    master_uri = archive.ubuntu.com
    compare_uri = de.archive.ubuntu.com
    -> True
    """
    # remove traling spaces and "/"
    compare_uri = compare_uri.rstrip("/ ")
    master_uri = master_uri.rstrip("/ ")
    # uri is identical
    if compare_uri == master_uri:
        # print "Identical"
        return True
    # add uri is a master site and orig_uri has the from "XX.mastersite"
    # (e.g. de.archive.ubuntu.com)
    try:
        compare_srv = compare_uri.split("//")[1]
        master_srv = master_uri.split("//")[1]
        # print "%s == %s " % (add_srv, orig_srv)
    except IndexError:  # ok, somethings wrong here
        # print "IndexError"
        return False
    # remove the leading "<country>." (if any) and see if that helps
    if "." in compare_srv and compare_srv[compare_srv.index(".") + 1 :] == master_srv:
        # print "Mirror"
        return True
    return False


def uniq(s: Iterable[T]) -> List[T]:
    """simple and efficient way to return uniq collection

    This is not intended for use with a SourceList. It is provided
    for internal use only. It does not have a leading underscore to
    not break any old code that uses it; but it should not be used
    in new code (and is not listed in __all__)."""
    return list(set(s))


class SingleValueProperty(property):
    def __init__(self, key: str, doc: str):
        self.key = key
        self.__doc__ = doc

    def __get__(
        self, obj: "Deb822SourceEntry", objtype: Optional[type] = None
    ) -> Optional[str]:
        return obj.section.get(self.key, None)

    def __set__(self, obj: "Deb822SourceEntry", value: Optional[str]) -> None:
        if value is None:
            del obj.section[self.key]
        else:
            obj.section[self.key] = value


class MultiValueProperty(property):
    def __init__(self, key: str, doc: str):
        self.key = key
        self.__doc__ = doc

    def __get__(
        self, obj: "Deb822SourceEntry", objtype: Optional[type] = None
    ) -> List[str]:
        return SourceEntry.mysplit(obj.section.get(self.key, ""))

    def __set__(self, obj: "Deb822SourceEntry", values: List[str]) -> None:
        obj.section[self.key] = " ".join(values)


def DeprecatedProperty(prop: T) -> T:
    return prop


class Deb822SourceEntry:
    def __init__(self, section: Optional[Union[_deb822.Section, str]], file: str):
        if section is None:
            self.section = _deb822.Section("")
        elif isinstance(section, str):
            self.section = _deb822.Section(section)
        else:
            self.section = section

        self._line = str(self.section)
        self.file = file
        self.template: Optional[Template] = None  # type DistInfo.Suite

    def __eq__(self, other: Any) -> Any:
        #  FIXME: Implement plurals more correctly
        """equal operator for two sources.list entries"""
        return (
            self.disabled == other.disabled
            and self.type == other.type
            and self.uri
            and self.uri.rstrip("/") == other.uri.rstrip("/")
            and self.dist == other.dist
            and self.comps == other.comps
        )

    architectures = MultiValueProperty("Architectures", "The list of architectures")
    types = MultiValueProperty("Types", "The list of types")
    type = DeprecatedProperty(SingleValueProperty("Types", "The list of types"))
    uris = MultiValueProperty("URIs", "URIs in the source")
    uri = DeprecatedProperty(SingleValueProperty("URIs", "URIs in the source"))
    suites = MultiValueProperty("Suites", "Suites in the source")
    dist = DeprecatedProperty(SingleValueProperty("Suites", "Suites in the source"))
    comps = MultiValueProperty("Components", "Components in the source")

    @property
    def comment(self) -> str:
        """Legacy attribute describing the paragraph header."""
        return self.section.header

    @comment.setter
    def comment(self, comment: str) -> None:
        """Legacy attribute describing the paragraph header."""
        self.section.header = comment

    @property
    def trusted(self) -> Optional[bool]:
        try:
            return apt_pkg.string_to_bool(self.section["Trusted"])
        except KeyError:
            return None

    @trusted.setter
    def trusted(self, value: Optional[bool]) -> None:
        if value is None:
            try:
                del self.section["Trusted"]
            except KeyError:
                pass
        else:
            self.section["Trusted"] = "yes" if value else "no"

    @property
    def disabled(self) -> bool:
        """Check if Enabled: no is set."""
        return not apt_pkg.string_to_bool(self.section.get("Enabled", "yes"))

    @disabled.setter
    def disabled(self, value: bool) -> None:
        if value:
            self.section["Enabled"] = "no"
        else:
            try:
                del self.section["Enabled"]
            except KeyError:
                pass

    @property
    def invalid(self) -> bool:
        """A section is invalid if it doesn't have proper entries."""
        return not self.section

    @property
    def line(self) -> str:
        """The entire (original) paragraph."""
        return self._line

    def __str__(self) -> str:
        return self.str().strip()

    def str(self) -> str:
        """Section as a string, newline terminated."""
        return str(self.section)

    def set_enabled(self, enabled: bool) -> None:
        """Deprecated (for deb822) accessor for .disabled"""
        self.disabled = not enabled


class SourceEntry:
    """single sources.list entry"""

    def __init__(self, line: str, file: Optional[str] = None):
        self.invalid = False  # is the source entry valid
        self.disabled = False  # is it disabled ('#' in front)
        self.type = ""  # what type (deb, deb-src)
        self.architectures: List[str] = []  # architectures
        self.trusted: Optional[bool] = None  # Trusted
        self.uri = ""  # base-uri
        self.dist = ""  # distribution (dapper, edgy, etc)
        self.comps: List[str] = []  # list of available componetns (may empty)
        self.comment = ""  # (optional) comment
        self.line = line  # the original sources.list line
        if file is None:
            file = apt_pkg.config.find_dir("Dir::Etc") + apt_pkg.config.find(
                "Dir::Etc::sourcelist"
            )
        self.file = file  # the file that the entry is located in
        self.parse(line)
        self.template: Optional[Template] = None  # type DistInfo.Suite
        self.children: List[SourceEntry] = []

    def __eq__(self, other: Any) -> Any:
        """equal operator for two sources.list entries"""
        return (
            self.disabled == other.disabled
            and self.type == other.type
            and self.uri.rstrip("/") == other.uri.rstrip("/")
            and self.dist == other.dist
            and self.comps == other.comps
        )

    @staticmethod
    def mysplit(line: str) -> List[str]:
        """a split() implementation that understands the sources.list
        format better and takes [] into account (for e.g. cdroms)"""
        line = line.strip()
        pieces = []
        tmp = ""
        # we are inside a [..] block
        p_found = False
        space_found = False
        for i in range(len(line)):
            if line[i] == "[":
                if space_found:
                    space_found = False
                    p_found = True
                    pieces.append(tmp)
                    tmp = line[i]
                else:
                    p_found = True
                    tmp += line[i]
            elif line[i] == "]":
                p_found = False
                tmp += line[i]
            elif space_found and not line[i].isspace():
                # we skip one or more space
                space_found = False
                pieces.append(tmp)
                tmp = line[i]
            elif line[i].isspace() and not p_found:
                # found a whitespace
                space_found = True
            else:
                tmp += line[i]
        # append last piece
        if len(tmp) > 0:
            pieces.append(tmp)
        return pieces

    def parse(self, line: str) -> None:
        """parse a given sources.list (textual) line and break it up
        into the field we have"""
        self.line = line
        line = line.strip()
        # check if the source is enabled/disabled
        if line == "" or line == "#":  # empty line
            self.invalid = True
            return
        if line[0] == "#":
            self.disabled = True
            pieces = line[1:].strip().split()
            # if it looks not like a disabled deb line return
            if not pieces[0] in ("rpm", "rpm-src", "deb", "deb-src"):
                self.invalid = True
                return
            else:
                line = line[1:]
        # check for another "#" in the line (this is treated as a comment)
        i = line.find("#")
        if i > 0:
            self.comment = line[i + 1 :]
            line = line[:i]
        # source is ok, split it and see what we have
        pieces = self.mysplit(line)
        # Sanity check
        if len(pieces) < 3:
            self.invalid = True
            return
        # Type, deb or deb-src
        self.type = pieces[0].strip()
        # Sanity check
        if self.type not in ("deb", "deb-src", "rpm", "rpm-src"):
            self.invalid = True
            return

        if pieces[1].strip()[0] == "[":
            options = pieces.pop(1).strip("[]").split()
            for option in options:
                try:
                    key, value = option.split("=", 1)
                except Exception:
                    self.invalid = True
                else:
                    if key == "arch":
                        self.architectures = value.split(",")
                    elif key == "trusted":
                        self.trusted = apt_pkg.string_to_bool(value)
                    else:
                        self.invalid = True

        # URI
        self.uri = pieces[1].strip()
        if len(self.uri) < 1:
            self.invalid = True
        # distro and components (optional)
        # Directory or distro
        self.dist = pieces[2].strip()
        if len(pieces) > 3:
            # List of components
            self.comps = pieces[3:]
        else:
            self.comps = []

    def set_enabled(self, new_value: bool) -> None:
        """set a line to enabled or disabled"""
        self.disabled = not new_value
        # enable, remove all "#" from the start of the line
        if new_value:
            self.line = self.line.lstrip().lstrip("#")
        else:
            # disabled, add a "#"
            if self.line.strip()[0] != "#":
                self.line = "#" + self.line

    def __str__(self) -> str:
        """debug helper"""
        return self.str().strip()

    def str(self) -> str:
        """return the current line as string"""
        if self.invalid:
            return self.line
        line = ""
        if self.disabled:
            line = "# "

        line += self.type

        if self.architectures and self.trusted is not None:
            line += " [arch=%s trusted=%s]" % (
                ",".join(self.architectures),
                "yes" if self.trusted else "no",
            )
        elif self.trusted is not None:
            line += " [trusted=%s]" % ("yes" if self.trusted else "no")
        elif self.architectures:
            line += " [arch=%s]" % ",".join(self.architectures)
        line += " %s %s" % (self.uri, self.dist)
        if len(self.comps) > 0:
            line += " " + " ".join(self.comps)
        if self.comment != "":
            line += " #" + self.comment
        line += "\n"
        return line


AnySourceEntry = Union[SourceEntry, Deb822SourceEntry]


class NullMatcher(object):
    """a Matcher that does nothing"""

    def match(self, s: AnySourceEntry) -> bool:
        return True


class SourcesList(object):
    """represents the full sources.list + sources.list.d file"""

    def __init__(
        self,
        withMatcher: bool = True,
        matcherPath: str = "/usr/share/python-apt/templates/",
        *,
        deb822: bool = False,
    ):
        self.list: List[AnySourceEntry] = []  # the actual SourceEntries Type
        self.matcher: Union[NullMatcher, SourceEntryMatcher]
        if withMatcher:
            self.matcher = SourceEntryMatcher(matcherPath)
        else:
            self.matcher = NullMatcher()
        self.deb822 = deb822
        self.refresh()

    def refresh(self) -> None:
        """update the list of known entries"""
        self.list = []
        # read sources.list
        file = apt_pkg.config.find_file("Dir::Etc::sourcelist")
        if os.path.exists(file):
            self.load(file)
        # read sources.list.d
        partsdir = apt_pkg.config.find_dir("Dir::Etc::sourceparts")
        if os.path.exists(partsdir):
            for file in os.listdir(partsdir):
                if (self.deb822 and file.endswith(".sources")) or file.endswith(
                    ".list"
                ):
                    self.load(os.path.join(partsdir, file))
        # check if the source item fits a predefined template
        for source in self.list:
            if not source.invalid:
                self.matcher.match(source)

    def __iter__(self) -> Iterator[AnySourceEntry]:
        """simple iterator to go over self.list, returns SourceEntry
        types"""
        for entry in self.list:
            yield entry

    # typing: ignore
    def __find(
        self, *predicates: Callable[[AnySourceEntry], bool], **attrs: Any
    ) -> Iterator[AnySourceEntry]:
        uri = attrs.pop("uri", None)
        for source in self.list:
            if uri and source.uri and uri.rstrip("/") != source.uri.rstrip("/"):
                continue
            if all(getattr(source, key) == attrs[key] for key in attrs) and all(
                predicate(source) for predicate in predicates
            ):
                yield source

    def add(
        self,
        type: str,
        uri: str,
        dist: str,
        orig_comps: List[str],
        comment: str = "",
        pos: int = -1,
        file: Optional[str] = None,
        architectures: Iterable[str] = [],
    ) -> AnySourceEntry:
        """
        Add a new source to the sources.list.
        The method will search for existing matching repos and will try to
        reuse them as far as possible
        """

        type = type.strip()
        disabled = type.startswith("#")
        if disabled:
            type = type[1:].lstrip()
        architectures = set(architectures)
        # create a working copy of the component list so that
        # we can modify it later
        comps = orig_comps[:]
        sources = self.__find(
            lambda s: set(s.architectures) == architectures,
            disabled=disabled,
            invalid=False,
            type=type,
            uri=uri,
            dist=dist,
        )
        # check if we have this source already in the sources.list
        for source in sources:
            for new_comp in comps:
                if new_comp in source.comps:
                    # we have this component already, delete it
                    # from the new_comps list
                    del comps[comps.index(new_comp)]
                    if len(comps) == 0:
                        return source

        sources = self.__find(
            lambda s: set(s.architectures) == architectures,
            invalid=False,
            type=type,
            uri=uri,
            dist=dist,
        )
        for source in sources:
            if source.disabled == disabled:
                # if there is a repo with the same (disabled, type, uri, dist)
                # just add the components
                if set(source.comps) != set(comps):
                    source.comps = uniq(source.comps + comps)
                return source
            elif source.disabled and not disabled:
                # enable any matching (type, uri, dist), but disabled repo
                if set(source.comps) == set(comps):
                    source.disabled = False
                    return source

        new_entry: AnySourceEntry
        if file is not None and file.endswith(".sources"):
            new_entry = Deb822SourceEntry(None, file=file)
            new_entry.types = [type]
            new_entry.uris = [uri]
            new_entry.suites = [dist]
            new_entry.comps = comps
            if architectures:
                new_entry.architectures = list(architectures)
            new_entry.section.header = comment
            new_entry.disabled = disabled
        else:
            # there isn't any matching source, so create a new line and parse it
            parts = [
                "#" if disabled else "",
                type,
                ("[arch=%s]" % ",".join(architectures)) if architectures else "",
                uri,
                dist,
            ]
            parts.extend(comps)
            if comment:
                parts.append("#" + comment)
            line = " ".join(part for part in parts if part) + "\n"

            new_entry = SourceEntry(line)
            if file is not None:
                new_entry.file = file

        self.matcher.match(new_entry)
        if pos < 0:
            self.list.append(new_entry)
        else:
            self.list.insert(pos, new_entry)
        return new_entry

    def remove(self, source_entry: SourceEntry) -> None:
        """remove the specified entry from the sources.list"""
        self.list.remove(source_entry)

    def restore_backup(self, backup_ext: str) -> None:
        "restore sources.list files based on the backup extension"
        file = apt_pkg.config.find_file("Dir::Etc::sourcelist")
        if os.path.exists(file + backup_ext) and os.path.exists(file):
            shutil.copy(file + backup_ext, file)
        # now sources.list.d
        partsdir = apt_pkg.config.find_dir("Dir::Etc::sourceparts")
        for file in glob.glob("%s/*" % partsdir):
            if os.path.exists(file + backup_ext):
                shutil.copy(file + backup_ext, file)

    def backup(self, backup_ext: Optional[str] = None) -> str:
        """make a backup of the current source files, if no backup extension
        is given, the current date/time is used (and returned)"""
        already_backuped: Iterable[str] = set()
        if backup_ext is None:
            backup_ext = time.strftime("%y%m%d.%H%M")
        for source in self.list:
            if source.file not in already_backuped and os.path.exists(source.file):
                shutil.copy(source.file, "%s%s" % (source.file, backup_ext))
        return backup_ext

    def load(self, file: str) -> None:
        """(re)load the current sources"""
        try:
            with open(file, "r") as f:
                if file.endswith(".sources"):
                    for section in _deb822.File(f):
                        self.list.append(Deb822SourceEntry(section, file))
                else:
                    for line in f:
                        source = SourceEntry(line, file)
                        self.list.append(source)
        except Exception as exc:
            logging.warning("could not open file '%s': %s\n" % (file, exc))

    def save(self) -> None:
        """save the current sources"""
        files: Dict[str, io.TextIOWrapper] = {}
        # write an empty default config file if there aren't any sources
        if len(self.list) == 0:
            path = apt_pkg.config.find_file("Dir::Etc::sourcelist")
            header = (
                "## See sources.list(5) for more information, especialy\n"
                "# Remember that you can only use http, ftp or file URIs\n"
                "# CDROMs are managed through the apt-cdrom tool.\n"
            )

            with open(path, "w") as f:
                f.write(header)
            return

        try:
            for source in self.list:
                if source.file not in files:
                    files[source.file] = open(source.file, "w")
                elif source.file.endswith(".sources"):
                    files[source.file].write("\n")
                files[source.file].write(source.str())
        finally:
            for f in files.values():
                f.close()

    def check_for_relations(
        self, sources_list: Iterable[AnySourceEntry]
    ) -> Tuple[List[AnySourceEntry], Dict[Template, List[AnySourceEntry]]]:
        """get all parent and child channels in the sources list"""
        parents = []
        used_child_templates: Dict[Template, List[AnySourceEntry]] = {}
        for source in sources_list:
            # try to avoid checking uninterressting sources
            if source.template is None:
                continue
            # set up a dict with all used child templates and corresponding
            # source entries
            if source.template.child:
                key = source.template
                if key not in used_child_templates:
                    used_child_templates[key] = []
                temp = used_child_templates[key]
                temp.append(source)
            else:
                # store each source with children aka. a parent :)
                if len(source.template.children) > 0:
                    parents.append(source)
        # print self.used_child_templates
        # print self.parents
        return (parents, used_child_templates)


class SourceEntryMatcher(object):
    """matcher class to make a source entry look nice
    lots of predefined matchers to make it i18n/gettext friendly
    """

    def __init__(self, matcherPath: str):
        self.templates: List[Template] = []
        # Get the human readable channel and comp names from the channel .infos
        spec_files = glob.glob("%s/*.info" % matcherPath)
        for f in spec_files:
            f = os.path.basename(f)
            i = f.find(".info")
            f = f[0:i]
            dist = DistInfo(f, base_dir=matcherPath)
            for template in dist.templates:
                if template.match_uri is not None:
                    self.templates.append(template)
        return

    def match(self, source: AnySourceEntry) -> bool:
        """Add a matching template to the source"""
        found = False
        for template in self.templates:
            if source.uri is None or source.dist is None:
                continue
            if (
                template.match_uri is not None
                and template.match_name is not None
                and source.uri is not None
                and source.dist is not None
                and re.search(template.match_uri, source.uri)
                and re.match(template.match_name, source.dist)
                and
                # deb is a valid fallback for deb-src (if that is not
                # definied, see #760035
                (source.type == template.type or template.type == "deb")
            ):
                found = True
                source.template = template
                break
            elif (
                template.is_mirror(source.uri)
                and template.match_name is not None
                and source.dist is not None
                and re.match(template.match_name, source.dist)
            ):
                found = True
                source.template = template
                break
        return found


# some simple tests
if __name__ == "__main__":
    apt_pkg.init_config()
    sources = SourcesList()

    for entry in sources:
        logging.info("entry %s" % entry.str())
        # print entry.uri

    mirror = is_mirror(
        "http://archive.ubuntu.com/ubuntu/", "http://de.archive.ubuntu.com/ubuntu/"
    )
    logging.info("is_mirror(): %s" % mirror)

    logging.info(
        is_mirror(
            "http://archive.ubuntu.com/ubuntu", "http://de.archive.ubuntu.com/ubuntu/"
        )
    )
    logging.info(
        is_mirror(
            "http://archive.ubuntu.com/ubuntu/", "http://de.archive.ubuntu.com/ubuntu"
        )
    )
