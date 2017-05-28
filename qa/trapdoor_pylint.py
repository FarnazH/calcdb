#!/usr/bin/env python
# -*- coding: utf-8 -*-
# HORTON: Helpful Open-source Research TOol for N-fermion systems.
# Copyright (C) 2011-2016 The HORTON Development Team
#
# This file is part of HORTON.
#
# HORTON is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# HORTON is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --
"""Trapdoor test using pylint.

This test calls the pylint program, see http://docs.pylint.org/index.html.
"""

import os
import shutil
from collections import Counter

from trapdoor import TrapdoorProgram, Message, get_source_filenames, run_command


def has_failed(returncode, stdout, stderr):
    """Determine if PyLint has failed."""
    return returncode < 0 or returncode >= 32


class PylintTrapdoorProgram(TrapdoorProgram):
    """A trapdoor program counting the number of pylint messages."""

    def __init__(self):
        """Initialize a PylintTrapdoorProgram instance."""
        TrapdoorProgram.__init__(self, 'pylint')

    def prepare(self):
        """Make some preparations in feature branch for running pylint.

        This includes a copy of tools/qa/pylintrc to QAWORKDIR.
        """
        TrapdoorProgram.prepare(self)

    def get_stats(self, config, args):
        """Run tests using Pylint.

        Parameters
        ----------
        config : dict
                 The dictionary loaded from ``trapdoor.cfg``.
        args : argparse.Namespace
            The result of parsing the command line arguments.

        Returns
        -------
        counter : collections.Counter
                  Counts of the number of messages of a specific type in a certain file.
        messages : Set([]) of strings
                   All errors encountered in the current branch.
        """
        # get default rcfile
        qatooldir = os.path.dirname(os.path.abspath(__file__))
        default_rc_file = os.path.join(self.qaworkdir, config['default_rc'])
        # FIXME: not too sure if this should be in prepare
        shutil.copy(os.path.join(qatooldir, os.path.basename(default_rc_file)), default_rc_file)

        # get Pylint version
        command = ['pylint', '--version', '--rcfile={0}'.format(default_rc_file)]
        version_info = ''.join(run_command(command, verbose=False)[0].split('\n')[:2])
        print 'USING              :', version_info

        # Collect python files (pylint ignore is quite bad.. need to ignore manually)
        py_extra = get_source_filenames(config, 'py', unpackaged_only=True)

        def get_filenames(file_or_dir, exclude=tuple()):
            """Recursively finds all of the files within the given file or directory.

            Avoids the files and directories specified in exclude.

            Parameters
            ----------
            file_or_dir : str
                File or directory
            exclude : tuple
                Files or directories to ignore

            Returns
            -------
            list of files as a relative path
            """
            output = []
            if os.path.isfile(file_or_dir) and file_or_dir not in exclude:
                output.append(file_or_dir)
            elif os.path.isdir(file_or_dir):
                for dirpath, _dirnames, filenames in os.walk(file_or_dir):
                    # check if directory is allowed
                    if any(os.path.samefile(dirpath, i) for i in exclude):
                        continue
                    for filename in filenames:
                        # check if filename is allowed
                        if (os.path.splitext(filename)[1] != '.py' or
                                filename in exclude or
                                any(os.path.samefile(os.path.join(dirpath, filename), i)
                                    for i in exclude)):
                            continue
                        output.append(os.path.join(dirpath, filename))
            return output

        output = ''
        exclude_files = []
        # run pylint test using each configuration
        for custom_config in config['custom'].values():
            rc_file = os.path.join(self.qaworkdir, custom_config['rc'])
            shutil.copy(os.path.join(qatooldir, os.path.basename(rc_file)), rc_file)

            # collect files
            py_files = []
            for custom_file in custom_config['files']:
                py_files.extend(get_filenames(custom_file))

            # call Pylint
            output += run_command(['pylint'] +
                                  py_files +
                                  ['--rcfile={0}'.format(rc_file),
                                   '-j 2', ],
                                  has_failed=has_failed)[0]
            # exclude directories/files
            exclude_files.extend(py_files)
        # get files that have not been run
        py_files = []
        for py_file in config['py_packages'] + py_extra:
            py_files.extend(get_filenames(py_file, exclude=exclude_files + config['py_exclude']))
        # call Pylint
        output += run_command(['pylint'] +
                              py_files +
                              ['--rcfile={0}'.format(default_rc_file),
                               '-j 2', ],
                              has_failed=has_failed)[0]

        # parse the output of Pylint into standard return values
        lines = output.split('\n')[:-1]
        score = lines[-2].split()[6]
        print 'SCORE              :', score
        counter = Counter()
        messages = set([])
        for line in lines:
            # skip lines that don't contain error messages
            if '.py:' not in line:
                continue
            if line.startswith('Report'):
                break
            # extract error information
            msg_id, _keyword, location, msg = line.split(' ', 3)
            counter[msg_id] += 1
            filename, pos = location.split(':')
            lineno, charno = pos.split(',')
            lineno = int(lineno)
            charno = int(charno)
            if charno == 0:
                charno = None
            messages.add(Message(filename, lineno, charno, '%s %s' % (msg_id, msg)))
        return counter, messages


if __name__ == '__main__':
    PylintTrapdoorProgram().main()
