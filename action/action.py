# This file is part of Docky.
# Copyright 2014 Camille MOUGEY <commial@gmail.com>
#
# Miasm2-Docker is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Docky is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Docky. If not, see <http://www.gnu.org/licenses/>.
import sys
import argparse

import docker


class Action(object):

    "Parent class for actions"

    _name_ = ""
    _desc_ = ""
    _args_ = []  # List of (*args, **kwargs)

    def __init__(self, command_line, config):
        # Parse command line
        parser = argparse.ArgumentParser(
            prog="%s %s" % (sys.argv[0], self._name_))
        for args, kwargs in self._args_:
            parser.add_argument(*args, **kwargs)
        self.args = parser.parse_args(command_line)

        # Store client
        self.client = docker.Client(base_url=config.base_url,
                                    timeout=config.timeout)

        # Store registry
        self.registries = config.registries

        # Store config
        self.config = config

        # Run action
        self.run()

    def run(self):
        raise NotImplementedError("Abstract method")
