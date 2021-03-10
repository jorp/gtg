# -----------------------------------------------------------------------------
# Getting Things GNOME! - a personal organizer for the GNOME desktop
# Copyright (c) The GTG Team
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

from gi.repository.Gdk import Color

from uuid import uuid4
from dataclasses import dataclass, field
import logging
import random

from lxml.etree import Element, SubElement
from typing import List

from GTG.core.base_store import BaseStore

log = logging.getLogger(__name__)


@dataclass
class Tag2:
    """A tag that can be applied to a Task."""

    tid: uuid4
    name: str
    icon: str = None
    color: str = None
    actionable: bool = True
    children: List = field(default_factory=list)

    def __str__(self) -> str:
        """String representation."""

        return (f'Tag "{self.name}" with id "{self.tid}"')


class TagStore(BaseStore):
    """A list of tags."""

    #: Tag to look for in XML
    XML_TAG = 'tag'


    def __init__(self) -> None:
        self.used_colors = set()
        super().__init__()


    def __str__(self) -> str:
        """String representation."""

        return f'Tag Store. Holds {len(self.lookup)} tag(s)'


    def get(name: str) -> Tag2:
        """Get a tag by name."""

        return self.lookup[name]


    def new(self, name: str, parent: uuid4 = None) -> Tag2:
        """Create a new tag and add it to the store."""

        try:
            return self.lookup[name]
        except KeyError:
            tag = Tag2(tid=uuid4(), name=name)

            return tag

    def generate_color(self) -> Color:
        """Generate a random color that isn't already used."""

        MAX_VALUE = 65535
        color = None

        while color in self.used_colors:
            color = Color(
                random.randint(0, MAX_VALUE),
                random.randint(0, MAX_VALUE),
                random.randint(0, MAX_VALUE)
            ).to_string()

        self.used_colors.add(color)
        return color
