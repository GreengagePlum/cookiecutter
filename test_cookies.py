#! /usr/bin/env python

"""This script tests if each of the cookiecutter templates work without errors."""

import argparse
import pathlib
import sys
import os
import tempfile
from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import RepositoryNotFound

# Setup  argparse to parse command line options
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
        "-k", "--keep", metavar="output_dir", type=pathlib.Path, default=tempfile.TemporaryDirectory(), help="Whether to keep the cookiecutter generated content at the end and the directory to output to (default: A temporary directory, artifacts deleted)"
        )
args = parser.parse_args()

# Take a list of the directories where this script is located (project root)
project_root_dir = os.path.dirname(os.path.realpath(__file__))
dirs_list = next(os.walk(project_root_dir))[1]

# List of directories that don't contain a cookiecutter template
excluded_dirs = (".git", ".venv", "images", "templates")

# Remove excluded directories
cookiecutters = []
for e in dirs_list:
    if e not in excluded_dirs:
        cookiecutters.append(os.path.join(project_root_dir, e))
cookiecutters.sort()

for cookie in cookiecutters:
    try:
        cookiecutter(cookie, no_input=True, output_dir=args.keep.name, overwrite_if_exists=True)
        print(f"{cookie} ...PASSED", file=sys.stderr)
    except RepositoryNotFound:
        print(f"{cookie} ...SKIPPED (not a template)", file=sys.stderr)

if type(args.keep) is not tempfile.TemporaryDirectory:
    print(f"Generated content written to: {args.keep.name}", file=sys.stderr)
