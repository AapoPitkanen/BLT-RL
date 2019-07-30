from enum import Enum, auto
from bearlibterminal import terminal
import re
from game_map import GameMap


def get_names_under_mouse(cur_coord, entities, game_map):
    # Return a list of names of entity located where the mouse cursor at.
    names = [
        entity.name for entity in entities if entity.x == cur_coord[0]
        and entity.y == cur_coord[1] and game_map.fov[entity.x, entity.y]
    ]

    names = ', '.join(names)

    return names


def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):

    bar_width = int(float(value) / maximum * total_width)

    terminal.color(terminal.color_from_name(back_color))
    for _i in range(total_width):
        terminal.put(x + _i, y, "o")

    if bar_width > 0:
        terminal.color(terminal.color_from_name(bar_color))
        for _i in range(bar_width):
            terminal.put(x + _i, y, "O")

    terminal.composition(terminal.TK_ON)

    text = f"{name}: {value}/{maximum}"

    x_centered = x + int((total_width - len(text)) / 2)

    terminal.color(terminal.color_from_name("white"))
    print_shadowed_text(x_centered, y, text)

    terminal.composition(terminal.TK_OFF)


def render_all(entities, player, game_map, message_log, bar_width, panel_y,
               mouse_coordinates, colors):

    entities_in_render_order = sorted(entities,
                                      key=lambda x: x.render_order.value)
    # Draw the map
    game_map.render(colors=colors)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        if game_map.fov[entity.x, entity.y]:
            entity.draw()

    render_bar(1, panel_y + 5, bar_width, 'HP', player.fighter.hp,
               player.fighter.max_hp, "red", "darker red")

    line_y = panel_y + 1
    for message in message_log.messages:
        terminal.color(terminal.color_from_name(message.color))
        print_shadowed_text(message_log.x, line_y, message.text)
        line_y += 1

    entity_names = get_names_under_mouse(mouse_coordinates, entities, game_map)
    terminal.printf(1, panel_y + 4, f"[color=white]{entity_names.title()}")


def print_shadowed_text(x, y, text, shadow_offset=1):
    """Print text with shadow."""
    # remove color options for drawing shadow which has to be always black
    pattern = r'\[/?color.*?\]'
    no_color_text = re.sub(pattern, '', text)

    terminal.composition(terminal.TK_ON)

    # Print shadowed text
    terminal.printf(
        x, y, '[color=black][offset=0, {0}]{1}'.format(shadow_offset,
                                                       no_color_text))
    terminal.printf(
        x, y,
        '[color=black][offset={0}, {0}]{1}'.format(shadow_offset,
                                                   no_color_text))

    # Print foreground text
    terminal.printf(x, y, text)

    terminal.composition(terminal.TK_OFF)