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
import json

from action import Action


class ActionPull(Action):
    _name_ = "pull"
    _desc_ = "Pull an image or a repository from a registry"
    _args_ = [(["-r", "--registry"], {"default": "",
                                      "help": "Source registry (default is Docker.io)"}),
              (["-w", "--with-creds"], {"default": False,
                                        "action": "store_true",
                                        "help": "Include credential while pulling (default is not)"}),
              (["REPOSITORY"], {"help": "Repository to pull"})]

    def run(self):
        # Get element to pull
        to_pull = self.args.REPOSITORY
        if self.args.registry:
            to_pull = self.config.registry_name2address(
                self.args.registry) + "/" + to_pull

        # Launch pulling
        print "Pulling %s..." % to_pull
        insecure_registry = False if self.args.with_creds else True
        for status in self.client.pull(to_pull, tag=None, stream=True,
                                       insecure_registry=insecure_registry):
            sys.stdout.write("\r" + json.loads(status)["status"])
            sys.stdout.flush()
        print ""
