#!/usr/bin/python3

import apt_pkg
import glob
import logging
import os
import sys

from CommandNotFound.db.creator import DbCreator
from CommandNotFound import CommandNotFound


if __name__ == "__main__":
    if "--debug" in sys.argv[1:]:
        logging.basicConfig(level=logging.DEBUG)
    elif "--verbose" in sys.argv[1:]:
        logging.basicConfig(level=logging.INFO)

    apt_pkg.init_config()
    db = CommandNotFound.dbpath
    if not os.access(os.path.dirname(db), os.W_OK):
        print("datbase directory %s not writable" % db)
        sys.exit(0)

    if apt_pkg.config.find_b("Acquire::IndexTargets::deb::CNF::DefaultEnabled", True):
        command_files = glob.glob("/var/lib/apt/lists/*Commands-*")
    else:
        command_files = glob.glob("/var/lib/apt/lists/*Contents*")
    if len(command_files) > 0:
        umask = os.umask(0o22)
        col = DbCreator(command_files)
        col.create(db)
        os.umask(umask)
    else:
        print("Could not find any command metadata")
        print("Please run 'apt update' before using this command.")

