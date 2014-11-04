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

from utils.config import Config
from utils.utils import Utils
from action import Action


class ActionTransfer(Action):
    _name_ = "transfer"
    _desc_ = "Transfer an image from a registry to another"
    _args_ = [(["-f", "--from"], {"default": Config._DEFAULT_REGISTRY_,
                                  "help": "Source registry (default is Docker.io)"}),
              (["-t", "--to"], {"default": Config._DEFAULT_REGISTRY_,
                                "help": "Destination registry (default is Docker.io)"}),
              (["IMGSRC"], {"help": "Source image"}),
              (["IMGDST"],
               {"help": "Destination image. '-' for same as IMGSRC"}),
              ]

    def get_registryaddr(self, reg_src):
        src = getattr(self.args, reg_src)
        if src.startswith("http"):
            src = "/".join(src.split("/")[2:])
        reg = self.config.registry_name2address(src)
        if reg == Config._DEFAULT_REGISTRY_:
            reg = ""

        if reg:
            reg += "/"
        return reg

    def run(self):
        # Format inputs
        reg_from = self.get_registryaddr("from")
        reg_to = self.get_registryaddr("to")
        imgsrc = self.args.IMGSRC
        if ":" not in imgsrc:
            imgsrc += ":latest"
        imgdst = self.args.IMGDST if (self.args.IMGDST != '-') else imgsrc
        if ":" not in imgdst:
            imgdst += ":latest"
        isrc = reg_from + imgsrc
        idst = reg_to + imgdst

        # Confirm transfer
        if not Utils.ask("Transfer %s -> %s" % (isrc, idst)):
            return

        # Search for source image avaibility
        isrc_id = None
        for img in self.client.images():
            if isrc in img["RepoTags"]:
                isrc_id = img["Id"]
                print "'%s' is locally available (%s), use it" % (isrc, img["Id"][:10])

        # Source image is not available, pull it
        if isrc_id is None:
            if not Utils.ask("'%s' is not locally available, try to pull it" % isrc):
                return
            # Try to pull Image without creds
            res = self.client.pull(isrc, insecure_registry=True)
            if "error" in res:
                print "An error as occurred (DEBUG: %s)" % res
                return
            print "'%s' successfully pulled !" % isrc

            raise NotImplementedError("Get image id")

        # Tag the element
        idst, idst_tag = ":".join(idst.split(":")[:-1]), idst.split(":")[-1]
        self.client.tag(isrc_id, idst, tag=idst_tag, force=False)

        # Push the element, insecure mode
        print "Pushing..."
        for status in self.client.push(idst, tag=idst_tag, stream=True,
                                       insecure_registry=True):
            sys.stdout.write("\r" + json.loads(status)["status"])
            sys.stdout.flush()
        print "\nTransfer complete !"
