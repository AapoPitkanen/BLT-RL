from bearlibterminal import terminal
import render_functions
from render_order import RenderLayer
from utils import wrap_tagged
import itertools


class Menu:
    # A generic menu with header and options.
    def __init__(self,
                 header,
                 width,
                 options=None,
                 pos='c',
                 background_color="white"):
        self.header = header
        self.width = width
        self.options = options if options else [
        ]  # Avoid default argument mutation

        self.header_wrapped = wrap_tagged(self.header, self.width)
        self.header_height = len(self.header_wrapped)
        self.height = self.header_height + len(self.options)

        if pos == 'l':  # Position menu to the left
            self.topleft_x = 0
        elif pos == 'r':  # Position menu to the right
            self.topleft_x = terminal.state(terminal.TK_WIDTH) - self.width
        else:  # Position menu to the center
            self.topleft_x = int(
                (terminal.state(terminal.TK_WIDTH) - self.width) / 2)

        self.topleft_y = int(
            (terminal.state(terminal.TK_HEIGHT) - self.height) / 2)
        self.background_color = background_color

    def draw(self):
        # Draw the menu to the terminal.
        if len(self.options) > 26:
            raise ValueError('Cannot have a menu with more than 26 options.')

        previous_layer = terminal.state(terminal.TK_LAYER)
        terminal.layer(RenderLayer.MENU.value)

        self.draw_background(background_color=self.background_color)

        # Print the header with wrapped text to the center of the menu
        terminal.color('white')
        terminal.composition(terminal.TK_ON)
        for i, _ in enumerate(self.header_wrapped):
            render_functions.print_shadowed_text(
                self.topleft_x + int((self.width / 2) + 1),
                self.topleft_y + i,
                self.header_wrapped[i],
                align=[terminal.TK_ALIGN_DEFAULT, terminal.TK_ALIGN_CENTER])

        # Print options under the menu, aligned to the left (left is the default)
        current_y = self.header_height + 1
        letter_index = ord('a')
        for option_text in self.options:
            text = f"{chr(letter_index)}) {option_text}"
            render_functions.print_shadowed_text(self.topleft_x,
                                                 self.topleft_y + current_y,
                                                 text)
            current_y += 1
            letter_index += 1

        terminal.composition(terminal.TK_OFF)

        terminal.layer(previous_layer)

    def draw_background(self, margin=2, background_color="white"):
        # Draw the menu background.
        terminal.color(background_color)

        left = -margin
        right = self.width + margin - 1
        top = -margin
        bot = self.height + margin - 1

        for term_x, term_y in itertools.product(range(left, right + 1),
                                                range(top, bot + 1)):
            # Draw corners
            if (term_x, term_y) == (left, top):
                terminal.put(self.topleft_x + term_x, self.topleft_y + term_y,
                             0x2000)
            elif (term_x, term_y) == (right, top):
                terminal.put(self.topleft_x + term_x, self.topleft_y + term_y,
                             0x2001)
            elif (term_x, term_y) == (right, bot):
                terminal.put(self.topleft_x + term_x, self.topleft_y + term_y,
                             0x2002)
            elif (term_x, term_y) == (left, bot):
                terminal.put(self.topleft_x + term_x, self.topleft_y + term_y,
                             0x2003)

            # Draw edges
            elif term_y == top:
                terminal.put(self.topleft_x + term_x, self.topleft_y + term_y,
                             0x2005)
            elif term_y == bot:
                terminal.put(self.topleft_x + term_x, self.topleft_y + term_y,
                             0x2004)
            elif term_x == left:
                terminal.put(self.topleft_x + term_x, self.topleft_y + term_y,
                             0x2006)
            elif term_x == right:
                terminal.put(self.topleft_x + term_x, self.topleft_y + term_y,
                             0x2007)
            # Draw remaining tiles
            else:
                terminal.put(self.topleft_x + term_x, self.topleft_y + term_y,
                             0x2008)


def inventory_menu(player, title):
    # Create and return a inventory menu instance.

    if not player.inventory.items:
        options = ["Your inventory is empty."]
    else:
        options = []

        for item_entity in player.inventory.items:
            text = f"{item_entity.name} {'(stack of ' + str(item_entity.item.quantity) + ')' if item_entity.item.quantity > 1 else ''}"
            options.append(text)

    return Menu(title, 90, options)


def main_menu():

    main_menu = Menu('Voidstone',
                     20, ["New game", "Load saved game", "Quit game"],
                     background_color=terminal.color_from_argb(200, 128, 0, 0))

    return main_menu