from typing import List, Dict, Any, Union, Tuple, TYPE_CHECKING
from components.status_effects import resolve_effects
from bearlibterminal import terminal
from death_functions import kill_monster, kill_player
from components.status_effects import resolve_effects
from entity import Entity, get_blocking_entities_at_location
from loader_functions.data_loaders import save_game
from game_messages import Message
from copy import deepcopy
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from game_states import GameStates

if TYPE_CHECKING:
    from camera import Camera
    from map_objects.game_map import GameMap


def player_turn(player, entities, camera, game_map, game_state,
                previous_game_state, targeting_item):
    player_turn_results = []
    if terminal.has_input():
        key: int = terminal.read()

        if key == terminal.TK_MOUSE_MOVE:
            mouse_coordinates = (terminal.state(terminal.TK_MOUSE_X),
                                 terminal.state(terminal.TK_MOUSE_Y))
            player_turn_results.append(
                {"mouse_coordinates": mouse_coordinates})

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

        if left_click:
            print(left_click)

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
                    player_turn_results.append(
                        {"game_state": GameStates.ENEMY_TURN})
                    player_turn_results.append({"action_consumed": True})

                else:
                    player_turn_results.append({"move": (dx, dy)})
                    player_turn_results.append(
                        {"game_state": GameStates.ENEMY_TURN})
                    player_turn_results.append({"action_consumed": True})

        if pass_turn:
            player_turn_results.append({"game_state": GameStates.ENEMY_TURN})
            player_turn_results.append({"action_consumed": True})

        if pickup:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
                    player_turn_results.append(
                        {"game_state": GameStates.ENEMY_TURN})
                    player_turn_results.append({"action_consumed": True})
                    break
            else:
                player_turn_results.append({
                    "message":
                    Message("There is nothing here to pick up.",
                            "light yellow")
                })

        if show_inventory:
            player_turn_results.append({"previous_game_state": game_state})
            player_turn_results.append(
                {"game_state": GameStates.SHOW_INVENTORY})

        if drop_inventory:
            player_turn_results.append({"previous_game_state": game_state})
            player_turn_results.append(
                {"game_state": GameStates.DROP_INVENTORY})

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

                player_turn_results.append({"action_consumed": True})

        if take_stairs:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    player_turn_results.append({"stairs_taken": True})
                    player_turn_results.append({"action_consumed": True})
                    break
            else:
                player_turn_results.append({
                    "message":
                    Message('There are no stairs here.', "yellow")
                })

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(targeting_item,
                                                        entities=entities,
                                                        game_map=game_map,
                                                        target_x=target_x,
                                                        target_y=target_y)
                player_turn_results.extend(item_use_results)
                player_turn_results.append({"action_consumed": True})
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if escape:
            if game_state in (GameStates.SHOW_INVENTORY,
                              GameStates.DROP_INVENTORY):
                player_turn_results.append({"game_state": previous_game_state})
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                player_turn_results.append({"game_saved": True})

    return player_turn_results


def process_player_turn_results(results, game):
    player = game.player
    fighter = game.player.fighter
    for player_turn_result in results:
        message = player_turn_result.get("message")
        dead_entity = player_turn_result.get("dead")
        item_added = player_turn_result.get("item_added")
        item_consumed = player_turn_result.get("consumed")
        item_dropped = player_turn_result.get("item_dropped")
        item_quantity_dropped = player_turn_result.get("item_quantity_dropped")
        targeting = player_turn_result.get("targeting")
        targeting_cancelled = player_turn_result.get("targeting_cancelled")
        xp = player_turn_result.get("xp")
        game_saved = player_turn_result.get("game_saved")
        stairs_taken = player_turn_result.get("stairs_taken")
        move = player_turn_result.get("move")
        pass_turn = player_turn_result.get("pass_turn")
        attack = player_turn_result.get("attack")
        new_game_state = player_turn_result.get("game_state")
        new_previous_game_state = player_turn_result.get("previous_game_state")
        new_mouse_coordinates = player_turn_result.get("mouse_coordinates")
        action_consumed = player_turn_result.get("action_consumed")

        if new_mouse_coordinates:
            game.mouse_coordinates = new_mouse_coordinates

        if new_game_state:
            game.state = new_game_state

        if new_previous_game_state:
            game.previous_state = new_previous_game_state

        if message:
            game.message_log.add_message(message)

        if targeting_cancelled:
            game.state = game.previous_state

            game.message_log.add_message(Message('Targeting cancelled'))

        if dead_entity:
            if dead_entity == player:
                message, game.state = kill_player(dead_entity, game)
            else:
                message = kill_monster(dead_entity, game)

            game.message_log.add_message(message)

        if item_added:
            game.entities.remove(item_added)

        if item_consumed:
            game.state = GameStates.ENEMY_TURN

        if item_dropped:
            game.entities.append(item_dropped)

        if item_quantity_dropped:
            item_copy = deepcopy(item_quantity_dropped)
            item_copy.item.quantity = 1
            game.entities.append(item_copy)

        if targeting:
            game.previous_state = GameStates.PLAYERS_TURN
            game.state = GameStates.TARGETING

            game.targeting_item = targeting

            game.message_log.add_message(
                game.targeting_item.item.targeting_message)

        if xp:
            leveled_up = game.player.level.add_xp(xp)
            game.message_log.add_message(
                Message(f"You gained {xp} experience points!"))

            if leveled_up:
                game.message_log.add_message(
                    Message(
                        f"Congratulations! You reached level {player.level.current_level}.",
                        "gold"))
                #previous_game_state = game_state
                #game_state = GameStates.LEVEL_UP

        if game_saved:
            save_game(player, game.entities, game.game_map, game.message_log,
                      game.state)
            game.exit = True

        if stairs_taken:
            game.entities = game.game_map.next_floor(player, game.message_log,
                                                     game.constants)
            game.fov_recompute = True
            terminal.clear()

        if move:
            if (player.x, player.y) not in game.game_map.scent_tiles:
                game.game_map.scent_tiles.update({(player.x, player.y): 150})
            else:
                game.game_map.scent_tiles[(player.x, player.y)] = 150
            player.move(move[0], move[1])
            game.fov_recompute = True
            fighter.energy += fighter.movement_energy_bonus

        if attack:
            fighter.energy += fighter.attack_energy_bonus

        if action_consumed:
            fighter.actions -= 1


def process_player_effect_results(results, game):
    for effect_result in results:
        message = effect_result.get("message")
        dead_entity = effect_result.get("dead")

        if message:
            game.message_log.add_message(message)

        if dead_entity:
            message, game.state = kill_player(dead_entity, game)
            game.message_log.add_message(message)
            break


def process_enemy_turn(game, monster_entity):
    enemy_turn_results = monster_entity.ai.take_turn(game.player,
                                                     game.game_map,
                                                     game.entities)

    for enemy_turn_result in enemy_turn_results:
        message = enemy_turn_result.get("message")
        dead_entity = enemy_turn_result.get("dead")
        attack = enemy_turn_result.get("attack")
        move = enemy_turn_result.get("move")

        if message:
            game.message_log.add_message(message)

        if dead_entity:
            if dead_entity == game.player:
                message, game.state = kill_player(dead_entity, game)
            else:
                message = kill_monster(dead_entity, game)

            game.message_log.add_message(message)

            if game.state == GameStates.PLAYER_DEAD:
                break

        if attack:
            monster_entity.fighter.energy += monster_entity.fighter.attack_energy_bonus

        if move:
            monster_entity.fighter.energy += monster_entity.fighter.movement_energy_bonus

    if game.state == GameStates.PLAYER_DEAD:
        return

    monster_effect_results = resolve_effects(monster_entity.fighter)

    for effect_result in monster_effect_results:

        message = effect_result.get("message")
        dead_entity = effect_result.get("dead")
        drop_loot = effect_result.get("drop_loot")

        if message:
            game.message_log.add_message(message)

        if dead_entity:
            if dead_entity == game.player:
                message, game.state = kill_player(dead_entity, game)
            else:
                message = kill_monster(dead_entity, game)

            game.message_log.add_message(message)

            if game.state == GameStates.PLAYER_DEAD:
                break

        if drop_loot:
            for item in drop_loot["items"]:
                item.x = drop_loot["x"]
                item.y = drop_loot["y"]
                game.entities.append(item)