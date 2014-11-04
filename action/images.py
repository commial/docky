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
import time

from utils.config import Config
from utils.utils import Utils
from action import Action


class ActionImages(Action):

    _name_ = "images"
    _desc_ = "List available images"
    _FIELDS_ = ["REGISTRY", "REPOSITORY", "TAG",
                "IMAGE ID", "CREATED", "VIRTUAL SIZE"]
    _args_ = [(["-s", "--sort-by"], {"default": "Id",
                                     "help": "Sort result. Available keys: %s" % ', '.join(_FIELDS_)
                                     })]

    @staticmethod
    def printable_size(size):
        if size < 1000:
            coef, unit = 1, "B"
        elif size < 1000 ** 2:
            coef, unit = 1000, "KB"
        elif size < 1000 ** 3:
            coef, unit = 1000 ** 2, "MB"
        else:
            coef, unit = 1000 ** 3, "GB"

        return "%.1f %s" % (size / float(coef), unit)

    @staticmethod
    def printable_date(timestamp):
        return time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(timestamp))

    def parse_repository(self, name):
        "Return registry, repository guessed from @name"

        # Get registry, repository
        info = name.split("/")
        registry = Config._DEFAULT_REGISTRY_
        repository = name
        if "." in info[0]:
            registry = info[0]
            repository = "/".join(info[1:])

        # Replace registry with its name (if it exists)
        registry = self.config.registry_address2name(registry)

        return registry, repository

    def run(self):
        images = self.client.images()

        # Parse images information
        images_enhanced = []
        for img in images:
            for repotag in img["RepoTags"]:
                registry, repository = self.parse_repository(
                    ":".join(repotag.split(":")[:-1]))
                images_enhanced.append({"IMAGE ID": img["Id"][:10],
                                        "CREATED": img["Created"],
                                        "VIRTUAL SIZE": img["VirtualSize"],
                                        "TAG": repotag.split(":")[-1],
                                        "REPOSITORY": repository,
                                        "REGISTRY": registry,
                                        })

        # Sort images (with facilities for sort key)
        sort_by = self.args.sort_by
        for column in self._FIELDS_:
            if column.startswith(sort_by.upper()):
                sort_by = column
                break
        images = sorted(images_enhanced, key=lambda x: x.get(sort_by))

        # Print images information
        for img in images:
            img["VIRTUAL SIZE"] = ActionImages.printable_size(
                img["VIRTUAL SIZE"])
            img["CREATED"] = ActionImages.printable_date(img["CREATED"])

        Utils.print_table([self._FIELDS_] + [[img[k]
                                              for k in self._FIELDS_] for img in images])
