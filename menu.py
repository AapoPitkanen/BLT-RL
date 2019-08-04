from bearlibterminal import terminal
import render_functions
from render_order import RenderLayer
import itertools


def menu(header,
         options,
         width,
         screen_width,
         screen_height,
         background_color="white",
         header_margin=1):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    previous_layer = terminal.state(terminal.TK_LAYER)
    terminal.layer(RenderLayer.MENU.value)

    _, header_height = terminal.measuref(header)
    height = len(options) + header_height

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    draw_menu_background(width,
                         height,
                         x,
                         y,
                         background_color=background_color)

    letter_index = ord("a")

    terminal.color(terminal.color_from_name("white"))
    render_functions.print_shadowed_text(x, y, header)

    y += header_margin

    for option_text in options:
        text = f"{chr(letter_index)}) {option_text}"
        render_functions.print_shadowed_text(x, y, text)

        y += 1
        letter_index += 1

    terminal.layer(previous_layer)


def new_inventory_menu(header, inventory, inventory_width, screen_width,
                       screen_height):
    if len(inventory.items) == 0:
        options = ["Your inventory is empty."]

    else:
        options = []

        for item_entity in inventory.items:
            text = f"{item_entity.name} {'(stack of ' + str(item_entity.item.quantity) + ')' if item_entity.item.quantity > 1 else ''}"
            options.append(text)

    menu(header,
         options,
         inventory_width,
         screen_width,
         screen_height,
         header_margin=2)


def draw_menu_background(width,
                         height,
                         topleft_x,
                         topleft_y,
                         margin=2,
                         background_color="white"):
    # Draw the menu background.
    terminal.color(background_color)

    left = -margin
    right = width + margin - 1
    top = -margin
    bot = height + margin - 1

    for term_x, term_y in itertools.product(range(left, right + 1),
                                            range(top, bot + 1)):
        # Draw corners
        if (term_x, term_y) == (left, top):
            terminal.put(topleft_x + term_x, topleft_y + term_y, 0x2000)
        elif (term_x, term_y) == (right, top):
            terminal.put(topleft_x + term_x, topleft_y + term_y, 0x2001)
        elif (term_x, term_y) == (right, bot):
            terminal.put(topleft_x + term_x, topleft_y + term_y, 0x2002)
        elif (term_x, term_y) == (left, bot):
            terminal.put(topleft_x + term_x, topleft_y + term_y, 0x2003)

        # Draw edges
        elif term_y == top:
            terminal.put(topleft_x + term_x, topleft_y + term_y, 0x2005)
        elif term_y == bot:
            terminal.put(topleft_x + term_x, topleft_y + term_y, 0x2004)
        elif term_x == left:
            terminal.put(topleft_x + term_x, topleft_y + term_y, 0x2006)
        elif term_x == right:
            terminal.put(topleft_x + term_x, topleft_y + term_y, 0x2007)
        # Draw remaining tiles
        else:
            terminal.put(topleft_x + term_x, topleft_y + term_y, 0x2008)


def main_menu(screen_width, screen_height):
    menu(header="VOIDSTONE",
         options=["Start a new game", "Load saved game", "Quit game"],
         width=24,
         screen_width=screen_width,
         screen_height=screen_height,
         background_color=terminal.color_from_argb(200, 128, 0, 0))


def message_box(header, width, screen_width, screen_height):
    menu(header=header,
         options=[],
         width=width,
         screen_width=screen_width,
         screen_height=screen_height)
