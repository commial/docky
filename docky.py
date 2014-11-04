#!/usr/bin/python
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

"Docky client"
import sys

from utils.utils import Utils
from utils.config import Config

from action import ACTIONS

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Minimalist Docker client.\n"
        print "Actions:"
        # Sort actions by name and print them
        actions = [(a._name_, a._desc_) for _, a in sorted(ACTIONS.items(),
                                                           key=lambda x: x[0])]
        Utils.print_table(actions,
                          title=False,
                          separator=" ")
        exit(0)

    action = sys.argv[1]
    if action not in ACTIONS:
        # Try to guess action
        guessed = [act for act in ACTIONS.keys() if act.startswith(action)]
        if len(guessed) == 1:
            action = guessed[0]
        else:
            if len(guessed) == 0:
                print "Unknown action: %s" % action
            else:
                print "Ambiguous action: %s" % " ".join(guessed)
            exit(-1)

    ACTIONS[action](sys.argv[2:], Config("docky.conf"))
