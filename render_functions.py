from render_order import RenderLayer, Visible
from bearlibterminal import terminal
import re
from game_map import GameMap
import itertools


def get_names_under_mouse(cur_coord, camera, entities, game_map):
    # Return a list of names of entity located where the mouse cursor at.

    (x, y) = (cur_coord[0], cur_coord[1])
    (x, y) = (camera.camera_x + x, camera.camera_y + y)

    names = [
        entity.name for entity in entities
        if entity.x == x and entity.y == y and game_map.fov[entity.x, entity.y]
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
               coordinates, menu, camera, colors):

    entities_in_render_order = sorted(entities,
                                      key=lambda x: x.render_order.value)
    # Draw the map

    camera_moved = camera.move_camera(player.x, player.y, game_map)

    terminal.layer(RenderLayer.MAP.value)

    if camera_moved:
        clear_map_layer()

    game_map.render_from_camera(camera)

    # Draw all entities in the list
    terminal.layer(RenderLayer.ENTITIES.value)
    for entity in entities_in_render_order:
        entity.draw(camera, game_map)

    terminal.layer(RenderLayer.HUD.value)
    clear_layer()

    # HP bar
    render_bar(1, panel_y + 5, bar_width, 'HP', player.fighter.hp,
               player.fighter.max_hp, "red", "darker red")

    entity_names = get_names_under_mouse(coordinates, camera, entities,
                                         game_map)
    terminal.printf(1, panel_y + 4, f"[color=white]{entity_names.title()}")

    terminal.layer(RenderLayer.HUD.value)
    line_y = panel_y + 1
    for message in message_log.messages:
        terminal.color(terminal.color_from_name(message.color))
        print_shadowed_text(message_log.x, line_y, message.text)
        line_y += 1

    if menu:
        menu.draw()


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


def clear_layer(layer=None):
    # Clear the current (default) layer or a specified layer.
    prev_layer = terminal.state(terminal.TK_LAYER)

    if hasattr(layer, 'value'):
        terminal.layer(layer.value)
    elif layer:
        terminal.layer(layer)

    terminal.clear_area(0, 0, terminal.state(terminal.TK_WIDTH),
                        terminal.state(terminal.TK_HEIGHT))

    terminal.layer(prev_layer)


def clear_map_layer():
    """Clear map layer."""
    prev_layer = terminal.state(terminal.TK_LAYER)
    terminal.layer(RenderLayer.MAP.value)

    terminal.bkcolor('black')
    terminal.clear_area(0, 0, terminal.state(terminal.TK_WIDTH),
                        terminal.state(terminal.TK_HEIGHT))

    terminal.layer(prev_layer)


def clear_menu_layer():
    """Clear menu and menu icon layer."""
    prev_layer = terminal.state(terminal.TK_LAYER)
    terminal.layer(RenderLayer.MENU.value)
    terminal.clear_area(0, 0, terminal.state(terminal.TK_WIDTH),
                        terminal.state(terminal.TK_HEIGHT))

    #terminal.layer(RenderLayer.MENU_ICON.value)
    terminal.clear_area(0, 0, terminal.state(terminal.TK_WIDTH),
                        terminal.state(terminal.TK_HEIGHT))

    terminal.layer(prev_layer)


def clear_all_entities(entities, camera):
    """Clear all entities on the terminal."""
    prev_layer = terminal.state(terminal.TK_LAYER)
    terminal.layer(RenderLayer.ENTITIES.value)

    for ent in entities:
        clear_entity(ent, camera)

    terminal.layer(prev_layer)


def clear_entity(ent, camera):
    """Clear an entity display on the terminal."""
    prev_layer = terminal.state(terminal.TK_LAYER)
    terminal.layer(RenderLayer.ENTITIES.value)

    (term_x, term_y) = camera.to_camera_coordinates(ent.x, ent.y)
    terminal.put_ext(term_x, term_y, 0, 0, ' ', None)

    terminal.layer(prev_layer)
