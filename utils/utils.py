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
"Usefull shared functions"


class Utils(object):

    """Usefull shared functions"""

    @staticmethod
    def ask(question, default="Y"):
        resp = "?"
        while (resp.lower()[0] not in ["y", "n"]):
            resp = raw_input("%s (%s)? " % (question, default))
            if resp == "":
                resp = default
        return resp.lower()[0] == "y"

    @staticmethod
    def print_table(ligs, title=True, separator='|'):
        "Print nicely @ligs. If title, @ligs[0] is title ligne"

        # Calc max by col
        columns = [0] * len(ligs[0])
        for lig in ligs:
            for index, element in enumerate(lig):
                columns[index] = max(columns[index], len(element))

        fmt_l = ["{%d:^%d}" % (i, l + 2) for i, l in enumerate(columns)]
        fmt = separator.join(fmt_l)

        for i, lig in enumerate(ligs):
            if i == 1 and title:
                print "-" * len(fmt.format(*lig))
            print fmt.format(*lig)
