# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

from collections import defaultdict
from tkinter import NW, Text, Toplevel
from tkinter.constants import END

from farg.core.ui.gui.views.list_based_view import ListBasedView


def ShowFocusableDetails(controller, focusable):
    stream = controller.stream
    stored_fringes = stream.stored_fringes
    top = Toplevel()
    tb = Text(top, height=50, width=50)
    tb.pack()
    tb.insert(END, '%s\n\n' % focusable)
    for fringe_element, strength_dict in stored_fringes.items():
        if focusable in strength_dict:
            tb.insert(END, '%.1f\t%s\n' %
                      (strength_dict[focusable], fringe_element))


class StreamView(ListBasedView):

    items_per_page = 3

    def GetAllItemsToDisplay(self, controller):
        """Returns a 2-tuple: A top message, and a list of items."""
        stream = controller.stream
        items = sorted(
            list(stream.foci.items()), reverse=True, key=lambda item: item[1])
        item_fringes = defaultdict(list)
        for fringe_element, item_to_strength_dict in stream.stored_fringes.items():
            for item, strength in item_to_strength_dict.items():
                item_fringes[item].append(fringe_element)
        return (items, 'Stream: %d prior foci' % len(stream.foci), dict(
            fringes=item_fringes))

    def DrawItem(self, widget_x, widget_y, item, extra_dict, controller):
        """Given x, y within the current widget and an item, draws it."""
        item_fringes = extra_dict['fringes']
        focus, strength = item
        x, y = self.CanvasCoordinates(widget_x, widget_y)
        text_id = self.canvas.create_text(
            x, y, text='%2.3f %s' % (strength, focus), anchor=NW)
        self.canvas.tag_bind(text_id, '<1>',
                             lambda e: ShowFocusableDetails(controller, focus))
        fringe_string_for_item = '; '.join(str(x) for x in item_fringes[focus])
        self.canvas.create_text(
            x + 5,
            y + 15,
            anchor=NW,
            text=fringe_string_for_item,
            width=self.width - widget_x - 5)
