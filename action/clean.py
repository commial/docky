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
import os
import json

import docker

from utils.utils import Utils
from action import Action


class ActionClean(Action):
    _name_ = "clean"
    _desc_ = "Cleanning actions"

    def clean_images_none(self):
        images = self.client.images()
        nones = []
        for img in images:
            if len(img["RepoTags"]) == 1 and img["RepoTags"][0] == "<none>:<none>":
                nones.append(img)

        if len(nones) == 0:
            print "No unamed images found."
            return

        print "%d images unammed ('<none>:<none>') founds." % len(nones)
        if Utils.ask("Remove them", default="N"):
            for img in nones:
                print "Removing %s..." % img["Id"][:10]
                # Force is false to avoid bad moves
                self.client.remove_image(img["Id"], force=False, noprune=False)

    def _clean_status_container(self, status):
        targets = []
        for container in self.client.containers(all=True):
            if container["Status"].startswith(status):
                targets.append(container)

        if len(targets) == 0:
            print "No containers %s found." % (status.lower())
            return

        # Display available elements
        print "%d containers %s founds." % (len(targets), status.lower())
        ligs = [["NAME", "IMAGE", "COMMAND"]]
        ligs += [[",".join(c["Names"]).replace("/", ""), c["Image"], c["Command"]]
                 for c in targets]
        Utils.print_table(ligs)

        if Utils.ask("Remove some of them", default="N"):
            for container in targets:
                if Utils.ask(
                        "\tRemove %s" % container["Names"][0].replace("/", ""),
                        default="N"):
                    # Force is false to avoid bad moves
                    print "\t-> Removing %s..." % container["Id"][:10]
                    self.client.remove_container(container["Id"], v=False,
                                                 link=False,
                                                 force=False)


    def clean_exited_container(self):
        self._clean_status_container("Exited")

    @staticmethod
    def dump_config(credentials):
        config = {}
        for address, creds in credentials.items():
            auth = ("%(username)s:%(password)s" % creds).encode("base64")
            config[address] = {"email": creds["email"],
                               "auth": auth}
        with open(os.path.join(os.environ.get('HOME', '.'),
                               docker.auth.auth.DOCKER_CONFIG_FILENAME),
                  "w") as fdesc:
            json.dump(config, fdesc)

    def clean_creds(self):
        credentials = docker.auth.load_config()
        if len(credentials.keys()) == 0:
            print "No credential founded."
            return

        print "%d identities founds: " % len(credentials.keys())
        for address, creds in credentials.items():
            print "\t- %s@%s" % (creds["username"], address)

        changed = False
        if Utils.ask("Remove some of them", default="N"):
            for address, creds in credentials.items():
                if Utils.ask(
                        "\tRemove %s@%s" % (creds["username"], address),
                        default="N"):
                    del credentials[address]
                    changed = True

        if changed:
            ActionClean.dump_config(credentials)

    def run(self):
        self.clean_images_none()
        self.clean_exited_container()
        self.clean_creds()
