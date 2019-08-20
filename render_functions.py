from render_order import RenderLayer, Visible
from bearlibterminal import terminal
from game import GameStates
from menu import inventory_menu, hud_background_menu, menu, equipment_menu
from map_objects.game_map import GameMap
import tcod
from utils import disk, circle, sector
import re


def get_names_under_mouse(cur_coord, camera, entities, game_map):
    # Return a list of names of the entities under the mouse cursor.
    # We'll have to account for the 8x16 cellsize here
    mouse_x = int((cur_coord[0] / 4))
    mouse_y = int((cur_coord[1] / 2))

    (x, y) = (mouse_x, mouse_y)
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
        terminal.put(x + _i, y, 0x2588)

    if bar_width > 0:
        terminal.color(terminal.color_from_name(bar_color))
        for _i in range(bar_width):
            terminal.put(x + _i, y, 0x2588)

    terminal.composition(terminal.TK_ON)

    text = f"{name}: {value}/{maximum}"

    x_centered = x + int((total_width - len(text)) / 2)

    terminal.color(terminal.color_from_name("white"))
    print_shadowed_text(x_centered, y, text)

    terminal.composition(terminal.TK_OFF)


def render_all(entities, player, game_map, message_log, bar_width, panel_y,
               coordinates, camera, game_state, targeting_item):
    entities_in_render_order = sorted(entities,
                                      key=lambda x: x.render_order.value)

    camera.move_camera(player.x, player.y, game_map)

    terminal.layer(RenderLayer.MAP.value)

    game_map.render_from_camera(camera)

    terminal.layer(RenderLayer.ENTITIES.value)
    for entity in entities_in_render_order:
        entity.draw(camera, game_map)

    # This layer contains all stuff that goes over the entities,
    # such as targeting assistance and graphical effects
    terminal.layer(RenderLayer.OVERLAY.value)
    for gfx in game_map.gfx_effects:
        gfx.update()
        if gfx.expired:
            game_map.gfx_effects.remove(gfx)
        elif gfx.render:
            if gfx.projectile:
                terminal.put(gfx.x, gfx.y, gfx.gfx_effect_tile)
            else:
                (term_x, term_y) = camera.map_to_term_coord(gfx.x, gfx.y)
                terminal.put(term_x, term_y, gfx.gfx_effect_tile)

    if game_state == GameStates.TARGETING:
        from entity import get_blocking_entities_at_location
        terminal.composition(terminal.TK_ON)

        mouse_map_x = int(coordinates[0] / 4)
        mouse_map_y = int(coordinates[1] / 2)

        mouse_map_x += camera.camera_x
        mouse_map_y += camera.camera_y

        line = tcod.line_iter(player.x, player.y, mouse_map_x, mouse_map_y)

        for coord in line:
            if coord[0] == player.x and coord[1] == player.y:
                continue
            cell_term_x, cell_term_y = camera.map_to_term_coord(
                coord[0], coord[1])
            if cell_term_x and cell_term_y:
                if coord[0] == mouse_map_x and coord[
                        1] == mouse_map_y and game_map.fov[
                            coord[0], coord[1]] and not game_map.is_blocked(
                                coord[0], coord[1]):
                    terminal.color(terminal.color_from_argb(125, 0, 255, 0))
                elif get_blocking_entities_at_location(entities, coord[0],
                                                       coord[1]):
                    terminal.color(terminal.color_from_argb(125, 255, 0, 0))
                elif not game_map.fov[coord[0],
                                      coord[1]] or game_map.is_blocked(
                                          coord[0], coord[1]):
                    terminal.color(terminal.color_from_argb(125, 255, 0, 0))
                else:
                    terminal.color(terminal.color_from_argb(125, 255, 255, 0))
                terminal.put(x=cell_term_x, y=cell_term_y, c=0x3014)
            terminal.composition(terminal.TK_OFF)

        if targeting_item:
            function_kwargs = targeting_item.item.function_kwargs
            if function_kwargs:
                radius = function_kwargs.get("radius")

                if radius:
                    for cell_x, cell_y in disk(mouse_map_x, mouse_map_y,
                                               radius, game_map.width,
                                               game_map.height):
                        (cell_term_x, cell_term_y) = camera.map_to_term_coord(
                            cell_x, cell_y)
                        if cell_term_x and cell_term_y:  # Omit cells outside of the terminal window
                            if get_blocking_entities_at_location(
                                    entities, cell_x,
                                    cell_y) and game_map.fov[cell_x, cell_y]:
                                terminal.color(
                                    terminal.color_from_argb(125, 0, 255, 0))
                            else:
                                terminal.color(
                                    terminal.color_from_argb(125, 139, 0, 0))
                            terminal.put(x=cell_term_x,
                                         y=cell_term_y,
                                         c=0x3014)

    terminal.color(terminal.color_from_name("white"))

    terminal.layer(RenderLayer.HUD_BACKGROUND.value)

    hud_background_menu(9)

    terminal.layer(RenderLayer.HUD.value)

    # HP bar
    render_bar(1, panel_y + 7, bar_width, 'HP', player.fighter.current_hp,
               player.fighter.max_hp, "red", "darker red")

    terminal.printf(1, panel_y + 8, f"Dungeon Level: {game_map.dungeon_level}")

    entity_names = get_names_under_mouse(coordinates, camera, entities,
                                         game_map)

    terminal.printf(1, panel_y - 1, f"[color=white]{entity_names.title()}")

    line_y = panel_y + 1

    for message in message_log.messages:
        terminal.color(terminal.color_from_name(message.color))
        print_shadowed_text(message_log.x, line_y, message.text)
        line_y += 1

    terminal.color(terminal.color_from_name("white"))

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            title = "INVENTORY – press key next to item to use it"
        elif game_state == GameStates.DROP_INVENTORY:
            title = "INVENTORY – press key next to item to drop it"
        inventory_menu(title, player.inventory, 90,
                       terminal.state(terminal.TK_WIDTH),
                       terminal.state(terminal.TK_HEIGHT))

    if game_state in (GameStates.SHOW_EQUIPMENT, GameStates.DROP_EQUIPMENT):
        if game_state == GameStates.SHOW_EQUIPMENT:
            title = "EQUIPMENT – press key next to equipment to equip it"
        elif game_state == GameStates.DROP_EQUIPMENT:
            title = "EQUIPMENT – press key next to equipment to drop it"
        equipment_menu(title, player.inventory, player.equipment, 90,
                       terminal.state(terminal.TK_WIDTH),
                       terminal.state(terminal.TK_HEIGHT))

    if game_state == GameStates.CHARACTER_SCREEN:
        menu("Homo", ["Paskaa"], 40, terminal.state(terminal.TK_WIDTH),
             terminal.state(terminal.TK_HEIGHT))


def print_shadowed_text(
        x,
        y,
        text,
        shadow_offset=1,
        shadow_color="black",
        align=[terminal.TK_ALIGN_DEFAULT, terminal.TK_ALIGN_DEFAULT]):

    # Print text with colored shadow (default is black). Text alignment can also be set.

    vertical_align = align[0]
    horizontal_align = align[1]

    terminal.composition(terminal.TK_ON)

    terminal.puts(x,
                  y,
                  f"[color={shadow_color}][offset=0, {shadow_offset}]{text}",
                  align=vertical_align | horizontal_align)

    terminal.puts(
        x,
        y,
        f"[color={shadow_color}][offset={shadow_offset}, {shadow_offset}]{text}",
        align=vertical_align | horizontal_align)

    terminal.puts(x, y, text, align=vertical_align | horizontal_align)

    terminal.composition(terminal.TK_OFF)


def print_colored_shadowed_text(
        x,
        y,
        text,
        colored_text,
        shadow_offset=1,
        shadow_color="black",
        align=[terminal.TK_ALIGN_DEFAULT, terminal.TK_ALIGN_DEFAULT]):

    # Print colored text with colored shadow (default is black). Text alignment can also be set.

    vertical_align = align[0]
    horizontal_align = align[1]

    terminal.composition(terminal.TK_ON)

    terminal.puts(x,
                  y,
                  f"[color={shadow_color}][offset=0, {shadow_offset}]{text}",
                  align=vertical_align | horizontal_align)

    terminal.puts(
        x,
        y,
        f"[color={shadow_color}][offset={shadow_offset}, {shadow_offset}]{text}",
        align=vertical_align | horizontal_align)

    terminal.puts(x, y, colored_text, align=vertical_align | horizontal_align)

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
    # Clear the map layer.
    prev_layer = terminal.state(terminal.TK_LAYER)
    terminal.layer(RenderLayer.MAP.value)

    terminal.bkcolor('black')
    terminal.clear_area(0, 0, terminal.state(terminal.TK_WIDTH),
                        terminal.state(terminal.TK_HEIGHT))

    terminal.layer(prev_layer)


def clear_menu_layer():
    # Clear the menu and menu icon layers.
    prev_layer = terminal.state(terminal.TK_LAYER)
    terminal.layer(RenderLayer.MENU.value)
    terminal.clear_area(0, 0, terminal.state(terminal.TK_WIDTH),
                        terminal.state(terminal.TK_HEIGHT))

    terminal.layer(RenderLayer.MENU_ICON.value)
    terminal.clear_area(0, 0, terminal.state(terminal.TK_WIDTH),
                        terminal.state(terminal.TK_HEIGHT))

    terminal.layer(prev_layer)


def main_screen():
    """Create main menu."""
    terminal.layer(RenderLayer.HUD.value)
    terminal.color('white')

    screen_w = terminal.state(terminal.TK_WIDTH)
    screen_h = terminal.state(terminal.TK_HEIGHT)

    # Draw background image
    terminal.put(0, 0, 0x4000)
    title = ""
    center = (screen_w - len(title)) // 2
    terminal.printf(center, screen_h // 2 - 4, title)

    center = (screen_w - len(title)) // 2
    terminal.printf(center, screen_h - 2, title)