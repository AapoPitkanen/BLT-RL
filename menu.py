from bearlibterminal import terminal
import render_functions
from render_order import RenderLayer
from utils import wrap_tagged

class Menu:
    """A generic menu with header and options."""

    def __init__(self, header, width, options=None, pos='c'):
        """Set attributes."""
        self.header = header
        self.width = width
        self.options = options if options else []  # they say using [] as default value is dangerous

        self.header_wrapped = wrap_tagged(self.header, self.width)
        self.header_height = len(self.header_wrapped)
        self.height = self.header_height + len(self.options)

        if pos == 'l':  # left
            self.topleft_x = 0
        elif pos == 'r':  # right
            self.topleft_x = terminal.state(terminal.TK_WIDTH) - self.width
        else:  # center
            self.topleft_x = int((terminal.state(terminal.TK_WIDTH) - self.width) / 2)

        self.topleft_y = int((terminal.state(terminal.TK_HEIGHT) - self.height) / 2)

def draw(self):
        # Draw the menu to the terminal.
        if len(self.options) > 26:
            raise ValueError('Cannot have a menu with more than 26 options.')

        # calculate total height for the header (after textwrap) and one line per option

        # center the menu on the screen


        previous_layer = terminal.state(terminal.TK_LAYER)
        terminal.layer(RenderLayer.MENU.value)

        self.draw_background()

        # Print the header with wrapped text
        terminal.color('white')
        terminal.composition(terminal.TK_ON)
        for i, _ in enumerate(self.header_wrapped):
            render_functions.print_shadowed_text(
                self.topleft_x, self.topleft_y + i, self.header_wrapped[i])

        current_y = self.header_height
        letter_index = ord('a')
        for option_text in self.options:
            text = f"{letter_index} [color=red]{option_text}[/color]"
            render_functions.print_shadowed_text(self.topleft_x, self.topleft_y + current_y, text)
            current_y += 1
            letter_index += 1

        terminal.composition(terminal.TK_OFF)

        # restore the previous layer
        terminal.layer(previous_layer)

def inventory_menu(player):
    # Create and return a inventory menu instance.

    if not player.inventory.items:
        options = ["Your inventory is empty."]
    else:
        options = []


        for item_entity in player.inventory.items:
            text = item_entity.name
            options.append(text)

    return Menu("This is the inventory menu", 60, options)