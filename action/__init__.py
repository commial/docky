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
"Docky actions implementations"

__all__ = []


from clean import ActionClean
from images import ActionImages
from pull import ActionPull
from search import ActionSearch
from transfer import ActionTransfer


ACTIONS = {"clean": ActionClean,
           "images": ActionImages,
           "pull": ActionPull,
           "search": ActionSearch,
           "transfer": ActionTransfer,
           }
