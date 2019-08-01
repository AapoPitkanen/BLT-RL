from bearlibterminal import terminal
import tcod
from entity import Entity, get_blocking_entities_at_location
from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import save_game, load_game
from map_objects.game_map import GameMap
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from death_functions import kill_monster, kill_player
from game_messages import MessageLog, Message
from game_states import GameStates
from render_order import RenderOrder
from render_functions import render_all, clear_all_entities, clear_map_layer, clear_menu_layer, main_screen
from camera import Camera
from copy import deepcopy
from menu import Menu
import sys


def main():
    terminal.open()
    constants = get_constants()
    terminal.set(
        f'window: size={constants["screen_width"]}x{constants["screen_height"]}, cellsize=8x16, title="{constants["window_title"]}"'
    )
    terminal.set("font: clacon.ttf, size=8x16")
    terminal.set(
        "0x1000: test_tiles.png, size=32x32, resize-filter=nearest, align=top-left"
    )
    terminal.set(
        "0x2000: inventory-ui.png, size=32x32, resize-filter=nearest, align=top-left"
    )
    terminal.set(
        "0x3000: wall_tiles.png, size=32x32, resize-filter=nearest, align=top-left"
    )
    terminal.set(
        "0x4000: voidstone_background.png, size=1280x768, align=top-left")

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    in_main_menu: bool = True

    main_menu = Menu('Voidstone', 24,
                     ["New game", "Load saved game", "Quit game"])

    while in_main_menu:

        key = None
        if terminal.has_input():
            key: int = terminal.read()

        if show_main_menu:
            main_screen()
            main_menu.draw()

            if show_load_error_message:
                Menu("No save game to load", 60).draw()

            terminal.refresh()

            action = handle_main_menu(key)

            new_game = action.get("new_game")
            load_saved_game = action.get("load_game")
            exit_game = action.get("exit")

            if show_load_error_message and (new_game or load_saved_game
                                            or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state = get_game_variables(
                    constants)
                game_state = GameStates.PLAYERS_TURN
                show_main_menu = False
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state = load_game(
                    )
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break
        else:
            terminal.clear()

            play_game(player, entities, game_map, message_log, game_state,
                      constants)

            terminal.clear()
            show_main_menu = True


def play_game(player, entities, game_map, message_log, game_state, constants):

    fov_recompute: bool = True

    game_state: GameStates = GameStates.PLAYERS_TURN
    previous_game_state: GameStates = game_state

    camera = Camera()
    mouse_coordinates = (0, 0)

    targeting_item = None

    while True:
        if fov_recompute:
            game_map.compute_fov(x=player.x,
                                 y=player.y,
                                 radius=constants["fov_radius"],
                                 light_walls=constants["fov_light_walls"],
                                 algorithm=constants["fov_algorithm"])

        render_all(
            entities=entities,
            player=player,
            game_map=game_map,
            message_log=message_log,
            bar_width=constants["bar_width"],
            panel_y=constants["panel_y"],
            coordinates=mouse_coordinates,
            camera=camera,
            game_state=game_state,
        )

        fov_recompute = False

        terminal.refresh()
        clear_all_entities(entities, camera)

        if terminal.has_input():
            key: int = terminal.read()

            if key == terminal.TK_MOUSE_MOVE:
                mouse_coordinates = (terminal.state(terminal.TK_MOUSE_X),
                                     terminal.state(terminal.TK_MOUSE_Y))

            action = handle_keys(key, game_state)
            mouse_action = handle_mouse(key, camera)

            escape = action.get('escape')
            movement = action.get('movement')
            pickup = action.get("pickup")
            show_inventory = action.get("show_inventory")
            drop_inventory = action.get("drop_inventory")
            inventory_index = action.get("inventory_index")
            take_stairs = action.get("take_stairs")
            pass_turn = action.get("pass_turn")

            left_click = mouse_action.get("left_click")
            right_click = mouse_action.get('right_click')

            player_turn_results = []

            if movement and game_state == GameStates.PLAYERS_TURN:
                dx, dy = movement
                destination_x: int = player.x + dx
                destination_y: int = player.y + dy

                if not game_map.is_blocked(destination_x, destination_y):
                    target: Entity = get_blocking_entities_at_location(
                        entities, destination_x, destination_y)

                    if target:
                        attack_results = player.fighter.attack(target)
                        player_turn_results.extend(attack_results)

                    else:
                        player.move(dx, dy)
                        fov_recompute = True

                    game_state = GameStates.ENEMY_TURN

            if pass_turn:
                game_state = GameStates.ENEMY_TURN

            if pickup:
                for entity in entities:
                    if entity.item and entity.x == player.x and entity.y == player.y:
                        pickup_results = player.inventory.add_item(entity)
                        player_turn_results.extend(pickup_results)

                        break
                else:
                    message_log.add_message(
                        Message("There is nothing here to pick up.",
                                "light yellow"))

            if show_inventory:
                previus_game_state = game_state
                game_state = GameStates.SHOW_INVENTORY

            if drop_inventory:
                previous_game_state = game_state
                game_state = GameStates.DROP_INVENTORY

            if game_state in (GameStates.SHOW_INVENTORY,
                              GameStates.DROP_INVENTORY):
                if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                        player.inventory.items):

                    item = player.inventory.items[inventory_index]

                    if game_state == GameStates.SHOW_INVENTORY:
                        player_turn_results.extend(
                            player.inventory.use(item,
                                                 entities=entities,
                                                 game_map=game_map))

                    elif game_state == GameStates.DROP_INVENTORY:
                        player_turn_results.extend(
                            player.inventory.drop_item(item))

                    game_state = GameStates.ENEMY_TURN

            if take_stairs:
                for entity in entities:

                    if entity.stairs and entity.x == player.x and entity.y == player.y:
                        entities = game_map.next_floor(player, message_log,
                                                       constants)
                        fov_recompute = True
                        terminal.clear()

                        break
                else:
                    message_log.add_message(
                        Message('There are no stairs here.', "yellow"))

            if game_state == GameStates.TARGETING:
                if left_click:
                    target_x, target_y = left_click

                    item_use_results = player.inventory.use(targeting_item,
                                                            entities=entities,
                                                            game_map=game_map,
                                                            target_x=target_x,
                                                            target_y=target_y)
                    player_turn_results.extend(item_use_results)
                elif right_click:
                    player_turn_results.append({'targeting_cancelled': True})

            if escape:
                if game_state in (GameStates.SHOW_INVENTORY,
                                  GameStates.DROP_INVENTORY):
                    game_state = previus_game_state
                elif game_state == GameStates.TARGETING:
                    player_turn_results.append({'targeting_cancelled': True})
                else:
                    save_game(player, entities, game_map, message_log,
                              game_state)
                    return True

            for player_turn_result in player_turn_results:

                message = player_turn_result.get("message")
                dead_entity = player_turn_result.get("dead")
                item_added = player_turn_result.get("item_added")
                item_consumed = player_turn_result.get("consumed")
                item_dropped = player_turn_result.get("item_dropped")
                item_quantity_dropped = player_turn_result.get(
                    "item_quantity_dropped")
                targeting = player_turn_result.get("targeting")
                targeting_cancelled = player_turn_result.get(
                    "targeting_cancelled")

                if message:
                    message_log.add_message(message)

                if targeting_cancelled:
                    game_state = previous_game_state

                    message_log.add_message(Message('Targeting cancelled'))

                if dead_entity:
                    if dead_entity == player:
                        message, game_state = kill_player(dead_entity)
                    else:
                        message = kill_monster(dead_entity)

                    message_log.add_message(message)

                if item_added:
                    entities.remove(item_added)
                    game_state = GameStates.ENEMY_TURN

                if item_consumed:
                    game_state = GameStates.ENEMY_TURN

                if item_dropped:
                    entities.append(item_dropped)
                    game_state = GameStates.ENEMY_TURN

                if item_quantity_dropped:
                    item_copy = deepcopy(item_quantity_dropped)
                    item_copy.item.quantity = 1
                    entities.append(item_copy)
                    game_state = GameStates.ENEMY_TURN

                if targeting:
                    previous_game_state = GameStates.PLAYERS_TURN
                    game_state = GameStates.TARGETING

                    targeting_item = targeting

                    message_log.add_message(
                        targeting_item.item.targeting_message)

            if game_state == GameStates.ENEMY_TURN:
                for entity in entities:
                    if entity.ai:
                        enemy_turn_results = entity.ai.take_turn(
                            player, game_map, entities)

                        for enemy_turn_result in enemy_turn_results:
                            message = enemy_turn_result.get('message')
                            dead_entity = enemy_turn_result.get('dead')

                            if message:
                                message_log.add_message(message)

                            if dead_entity:
                                if dead_entity == player:
                                    message, game_state = kill_player(
                                        dead_entity)
                                else:
                                    message = kill_monster(dead_entity)

                                message_log.add_message(message)

                                if game_state == GameStates.PLAYER_DEAD:
                                    break

                        if game_state == GameStates.PLAYER_DEAD:
                            break
                else:
                    game_state = GameStates.PLAYERS_TURN

        terminal.clear()


if __name__ == '__main__':
    main()
