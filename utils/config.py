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
"Docky configuration handler"
import ConfigParser


class Config(object):

    """Docky configuration handler

    Provide:
    @base_url: docker daemon url
    @timeout: docker daemon timeout
    @registries: the list of enabled registries

    For each registry:
    @name: registry preferred name
    @index: index server url
    @registry: registry server url
    """

    _GENERAL_SECTION_ = "General"
    _general_fields_ = {"server": "base_url",
                        "timeout": "timeout",
                        }
    _DEFAULT_REGISTRY_ = "registry.docker.io"
    _DEFAULT_INDEX_ = "index.docker.io"

    def __init__(self, files):
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(files)

        # Parse general configuration
        for name, real_name in self._general_fields_.items():
            try:
                setattr(
                    self, real_name, self.config.get(self._GENERAL_SECTION_,
                                                     name))
            except Exception, error:
                print "Config error: %s" % error
                exit(-1)
        # Ensure correct types
        self.timeout = int(self.timeout)

        # Parse registries configurations
        registries = []
        try:
            for registry in self.config.get(self._GENERAL_SECTION_, "enabled").split(','):
                registries.append({"name": registry,
                                   "index": self.config.get(registry, "index"),
                                   "registry": self.config.get(registry, "registry"),
                                   })
        except Exception, error:
            print "Config error: %s" % error
            exit(-1)

        self.registries = registries

    def registry_address2name(self, address):
        """Try to match a registry address with its name
        @address: registry address
        Return the expected name if found, @address otherwise
        """
        for reg in self.registries:
            if address in reg["registry"] or reg["registry"] in address:
                return reg["name"]
        return address

    def registry_name2address(self, name):
        """Try to match a registry name with its address
        @name: registry name
        Return the expected address if found, @name otherwise
        """
        for reg in self.registries:
            if name == reg["name"]:
                return reg["registry"]
        return name
