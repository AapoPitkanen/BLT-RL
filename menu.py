from typing import Any, List, TYPE_CHECKING
from bearlibterminal import terminal
import render_functions
from render_order import RenderLayer
import itertools

if TYPE_CHECKING:
    from components.inventory import Inventory
    from components.equipment import Equipment


def menu(header: str,
         options: List[Any],
         width: int,
         screen_width: int,
         screen_height: int,
         background_margin: int = 2,
         header_margin: int = 1,
         y_offset: int = 0) -> None:

    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    previous_layer = terminal.state(terminal.TK_LAYER)
    terminal.layer(RenderLayer.MENU.value)

    _, header_height = terminal.measuref(header)
    height = len(options) + header_height

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2)) + y_offset

    draw_menu_background(width + 4, height + 2, x, y, margin=background_margin)

    letter_index = ord("a")

    terminal.color(terminal.color_from_name("white"))

    # Draw menu header to the center of the menu

    render_functions.print_shadowed_text(
        int(round(screen_width / 2)) + 5,
        y + 2,
        header,
        align=[terminal.TK_ALIGN_DEFAULT, terminal.TK_ALIGN_CENTER])

    y += header_margin

    for option_text in options:
        text = f"{chr(letter_index)}) {option_text}"
        render_functions.print_shadowed_text(x + 4, y + 2, text)

        y += 1
        letter_index += 1

    terminal.layer(previous_layer)


def menu_colored_options(header: str,
                         options: List[Any],
                         width: int,
                         screen_width: int,
                         screen_height: int,
                         background_margin: int = 2,
                         header_margin: int = 1,
                         y_offset: int = 0) -> None:

    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    previous_layer = terminal.state(terminal.TK_LAYER)
    terminal.layer(RenderLayer.MENU.value)

    _, header_height = terminal.measuref(header)
    height = len(options) + header_height

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2)) + y_offset

    terminal.color(terminal.color_from_name("white"))

    draw_menu_background(width + 4, height + 2, x, y, margin=background_margin)

    letter_index = ord("a")

    # Draw menu header to the center of the menu

    render_functions.print_shadowed_text(
        int(round(screen_width / 2)) + 5,
        y + 2,
        header,
        align=[terminal.TK_ALIGN_DEFAULT, terminal.TK_ALIGN_CENTER])

    y += header_margin

    for option_text, option_text_color in options:
        text = f"{chr(letter_index)}) {option_text}"
        colored_text = f"{chr(letter_index)}) [color={option_text_color}]{option_text}[/color]"
        render_functions.print_colored_shadowed_text(x + 4,
                                                     y + 2,
                                                     text,
                                                     colored_text,
                                                     shadow_offset=1)

        y += 1
        letter_index += 1

    terminal.layer(previous_layer)


def hud_background_menu(panel_height):
    height = panel_height - 2
    width = terminal.state(terminal.TK_WIDTH) - 8

    x = 0
    y = terminal.state(terminal.TK_HEIGHT) - height - 3

    draw_menu_background(
        width,
        height,
        x,
        y,
        margin=0,
    )


def inventory_menu(header: str, inventory: "Inventory", inventory_width: int,
                   screen_width: int, screen_height: int) -> None:
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
         header_margin=2,
         y_offset=-6)


def equipment_menu(header: str, inventory: "Inventory",
                   player_equipment: "Equipment", inventory_width: int,
                   screen_width: int, screen_height: int) -> None:
    if len(inventory.equipment) == 0:
        options = [("You don't have any equipment.", "white")]
    else:
        options = []

        for equipment in inventory.equipment:
            if player_equipment.HEAD == equipment:
                options.append(
                    (f"{equipment.name} (worn on head)", equipment.equippable.
                     equippable_type.rarity["rarity_color"]))
            elif player_equipment.SHOULDERS == equipment:
                options.append(
                    (f"{equipment.name} (worn on shoulders)", equipment.
                     equippable.equippable_type.rarity["rarity_color"]))
            elif player_equipment.CLOAK == equipment:
                options.append(
                    (f"{equipment.name} (fastened on shoulders)", equipment.
                     equippable.equippable_type.rarity["rarity_color"]))
            elif player_equipment.NECKLACE == equipment:
                options.append(
                    (f"{equipment.name} (worn on neck)", equipment.equippable.
                     equippable_type.rarity["rarity_color"]))
            elif player_equipment.TORSO == equipment:
                options.append(
                    (f"{equipment.name} (worn on body)", equipment.equippable.
                     equippable_type.rarity["rarity_color"]))
            elif player_equipment.LEGS == equipment:
                options.append(
                    (f"{equipment.name} (worn on legs)", equipment.equippable.
                     equippable_type.rarity["rarity_color"]))
            elif player_equipment.WRISTS == equipment:
                options.append(
                    (f"{equipment.name} (worn on wrists)", equipment.
                     equippable.equippable_type.rarity["rarity_color"]))
            elif player_equipment.GLOVES == equipment:
                options.append(
                    (f"{equipment.name} (worn on hands)", equipment.equippable.
                     equippable_type.rarity["rarity_color"]))
            elif player_equipment.BOOTS == equipment:
                options.append(
                    (f"{equipment.name} (worn on feet)", equipment.equippable.
                     equippable_type.rarity["rarity_color"]))
            elif player_equipment.RIGHT_RING == equipment:
                options.append(
                    (f"{equipment.name} (worn on right finger)", equipment.
                     equippable.equippable_type.rarity["rarity_color"]))
            elif player_equipment.LEFT_RING == equipment:
                options.append(
                    (f"{equipment.name} (worn on left finger)", equipment.
                     equippable.equippable_type.rarity["rarity_color"]))
            elif player_equipment.MAIN_HAND == equipment:
                options.append(
                    (f"{equipment.name} (equipped on main hand)", equipment.
                     equippable.equippable_type.rarity["rarity_color"]))
            elif player_equipment.OFF_HAND == equipment:
                options.append(
                    (f"{equipment.name} (equipped on off hand)", equipment.
                     equippable.equippable_type.rarity["rarity_color"]))
            elif player_equipment.RANGED_WEAPON == equipment:
                options.append(
                    (f"{equipment.name} (equipped as ranged weapon)",
                     equipment.equippable.equippable_type.
                     rarity["rarity_color"]))
            elif player_equipment.RANGED_WEAPON_AMMUNITION == equipment:
                options.append((
                    f"{equipment.name} {'(stack of ' + str(equipment.item.quantity) + ')' if equipment.item.quantity > 1 else ''} (equipped as ammunition)",
                    equipment.equippable.equippable_type.rarity["rarity_color"]
                ))
            else:
                options.append((
                    f"{equipment.name} {'(stack of ' + str(equipment.item.quantity) + ')' if equipment.item.quantity > 1 else ''}",
                    equipment.equippable.equippable_type.rarity["rarity_color"]
                ))

    menu_colored_options(header,
                         options,
                         inventory_width,
                         screen_width,
                         screen_height,
                         header_margin=2,
                         y_offset=-6)


def draw_menu_background(width: int,
                         height: int,
                         topleft_x: int,
                         topleft_y: int,
                         margin: int = 1) -> None:

    left = 0
    right = int(width / 4) + 1
    top = 0
    bottom = int(height / 2) + 1

    for term_x, term_y in itertools.product(range(left, right + 1),
                                            range(top, bottom + 1)):
        if (term_x, term_y) == (left, top):
            terminal.put(topleft_x + term_x * 4, topleft_y + term_y * 2,
                         0x2000)
        elif (term_x, term_y) == (right, top):
            terminal.put(topleft_x + term_x * 4, topleft_y + term_y * 2,
                         0x2001)
        elif (term_x, term_y) == (right, bottom):
            terminal.put(topleft_x + term_x * 4, topleft_y + term_y * 2,
                         0x2002)
        elif (term_x, term_y) == (left, bottom):
            terminal.put(topleft_x + term_x * 4, topleft_y + term_y * 2,
                         0x2003)
        elif term_y == top:
            terminal.put(topleft_x + term_x * 4, topleft_y + term_y * 2,
                         0x2005)
        elif term_y == bottom:
            terminal.put(topleft_x + term_x * 4, topleft_y + term_y * 2,
                         0x2004)
        elif term_x == left:
            terminal.put(topleft_x + term_x * 4, topleft_y + term_y * 2,
                         0x2006)
        elif term_x == right:
            terminal.put(topleft_x + term_x * 4, topleft_y + term_y * 2,
                         0x2007)
        else:
            terminal.put(topleft_x + term_x * 4, topleft_y + term_y * 2,
                         0x2008)


def main_menu(screen_width: int, screen_height: int) -> None:
    menu(header="VOIDSTONE",
         options=["Start a new game", "Load saved game", "Quit game"],
         width=24,
         screen_width=screen_width,
         screen_height=screen_height,
         header_margin=2)


def message_box(header: str, width: int, screen_width: int,
                screen_height: int) -> None:
    menu(header=header,
         options=[],
         width=width,
         screen_width=screen_width,
         screen_height=screen_height)
