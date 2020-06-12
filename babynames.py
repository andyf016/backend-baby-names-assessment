#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

"""
Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration. Here's what the HTML looks like in the
baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 - Extract all the text from the file and print it
 - Find and extract the year and print it
 - Extract the names and rank numbers and print them
 - Get the names data into a dict and print it
 - Build the [year, 'name rank', ... ] list and print it
 - Fix main() to use the extracted_names list
"""
__author__ = "Andrew Fillenwarth, big thanks to Janell and David R. for helping me find the needle in the hay stack!"

import sys
import re
import argparse


def convert_tuple(tup):
    strg = ' '.join(tup)
    return strg


def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a
    single list starting with the year string followed by
    the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', 'Aaron 57', 'Abagail 895', ...]
    """
    names = []
    names_dict = {}
    with open(filename) as html_file:
        line_list = html_file.readlines()
        #print(line_list)
        year_pattern = re.compile(r'(Popularity in )(\d\d\d\d)')
        name_pattern = re.compile(r'(<tr align="right"><td>)(\d{1,4})(</td><td>)([A-Z][a-z]+)(</td><td>)([A-Z][a-z]+)')
        for line in line_list:
            name_match = name_pattern.finditer(line)                            
            year_match = year_pattern.finditer(line)
            for match in name_match:
                names_dict.setdefault(match.group(4), match.group(2))
                names_dict.setdefault(match.group(6), match.group(2))
            for match in year_match:
                names.append(match.group(2))
        listy = list(names_dict.items())
        for item in listy:
            names.append(convert_tuple(item))
        names.sort()
        return names


def create_parser():
    """Create a command line parser object with 2 argument definitions."""
    parser = argparse.ArgumentParser(
        description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    # The nargs option instructs the parser to expect 1 or more
    # filenames. It will also expand wildcards just like the shell.
    # e.g. 'baby*.html' will work.
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def main(args):
    # Create a command line parser object with parsing rules
    parser = create_parser()
    # Run the parser to collect command line arguments into a
    # NAMESPACE called 'ns'
    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    file_list = ns.files

    # option flag
    create_summary = ns.summaryfile

    # For each filename, call `extract_names()` with that single file.
    # Format the resulting list as a vertical list (separated by newline \n).
    # Use the create_summary flag to decide whether to print the list
    # or to write the list to a summary file (e.g. `baby1990.html.summary`).


    if create_summary:
        for item in file_list:
            name = str(item) + '.summary'
            f = open(name, 'a')
            text = '\n'.join(extract_names(item))
            f.write(text)
            f.close 
    else:
        for item in file_list:
            text = '\n'.join(extract_names(item))
            print(text)
    



if __name__ == '__main__':
    main(sys.argv[1:])
