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
from docker.errors import APIError

from utils.utils import Utils
from utils.config import Config
from action import Action


class ActionSearch(Action):

    _name_ = "search"
    _desc_ = "Search for an image"
    _args_ = [(["TERM"], {"nargs": "+",
                          "help": "Terms to search for"})]
    _fields_ = ["name", "description",
                "is_trusted", "is_official", "star_count"]
    _fieldnames_ = {"name": "NAME",
                    "description": "DESCRIPTION",
                    "is_trusted": "AUTO-BUILD",
                    "is_official": "OFFICIAL",
                    "star_count": "STARS",
                    }
    _format_ = {False: '',
                True: 'OK',
                }

    @staticmethod
    def print_table(ligs):
        for lig_num, lig in enumerate(ligs):
            for element_num, element in enumerate(lig):
                ligs[lig_num][element_num] = ActionSearch._format_.get(element,
                                                                       element)

        Utils.print_table(ligs)

    def run(self):
        for registry in self.registries:
            # Formatting
            print registry['name']
            print "=" * len(registry['name'])
            print ""

            # Get results
            if Config._DEFAULT_INDEX_ in registry['index']:
                # Special case for docker.io: no index
                terms = self.args.TERM
            else:
                terms = map(lambda x: "%s/%s" % (registry['index'], x),
                            self.args.TERM)
            try:
                results = self.client.search(terms)
            except APIError, error:
                print "Unable to connect (%s)." % error
                continue

            # Print results
            if len(results) == 0:
                print "No results."
                continue

            ligs = []
            for result in [self._fieldnames_] + results:
                ligs.append([result[field] for field in self._fields_])
            ActionSearch.print_table(ligs)
