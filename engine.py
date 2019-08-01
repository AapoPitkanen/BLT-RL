from bearlibterminal import terminal
import tcod
from entity import Entity, get_blocking_entities_at_location
from game_map import GameMap
from input_handlers import handle_keys, handle_mouse
from components.inventory import Inventory
from components.item import Item
from item_functions import cast_fireball
from components.fighter import Fighter
from components.equipment import Equipment
from death_functions import kill_monster, kill_player
from game_messages import MessageLog, Message
from game_states import GameStates
from render_order import RenderOrder
from render_functions import render_all, clear_all_entities, clear_map_layer, clear_menu_layer
from camera import Camera
from copy import deepcopy


def main():
    window_title: str = 'Bearlibterm/TCOD Roguelike'

    screen_width: int = 160
    screen_height: int = 48

    map_width: int = 80
    map_height: int = 80

    room_max_size: int = 10
    room_min_size: int = 6
    max_rooms: int = 50

    fov_algorithm: int = 0
    fov_light_walls: bool = True
    fov_radius: int = 10

    max_monsters_per_room: int = 3
    max_items_per_room: int = 2

    bar_width: int = 20
    panel_height: int = 8
    panel_y: int = (screen_height - panel_height)

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    mouse_coordinates = (0, 0)

    colors = {
        'dark_wall': terminal.color_from_argb(0, 38, 38, 38),
        'dark_ground': terminal.color_from_argb(0, 100, 100, 100),
        'light_wall': terminal.color_from_argb(255, 128, 128, 128),
        'light_ground': terminal.color_from_argb(0, 255, 255, 255)
    }

    game_running: bool = True

    fov_recompute: bool = True

    fighter_component = Fighter(hp=30, defense=2, power=15)

    inventory_component = Inventory(26)

    equipment_component = Equipment()

    player: Entity = Entity(x=0,
                            y=0,
                            char=0x1004,
                            color=terminal.color_from_argb(255, 255, 255, 255),
                            name='Player',
                            blocks=True,
                            render_order=RenderOrder.ACTOR,
                            fighter=fighter_component,
                            inventory=inventory_component,
                            equipment=equipment_component)

    item_component = Item(
        use_function=cast_fireball,
        targeting=True,
        targeting_message=Message(
            'Left-click a target tile for the fireball, or right-click to cancel.',
            "light cyan"),
        damage=15,
        radius=2)

    item = Entity(0,
                  0,
                  0x1007,
                  "red",
                  'Scroll of Fireball',
                  render_order=RenderOrder.ITEM,
                  item=item_component)

    player.inventory.add_item(item)

    entities = [player]

    message_log = MessageLog(message_x, message_width, message_height)

    game_map: GameMap = GameMap(width=map_width, height=map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width,
                      map_height, player, entities, max_monsters_per_room,
                      max_items_per_room)

    game_state: GameStates = GameStates.PLAYERS_TURN
    previous_game_state: GameStates = game_state

    targeting_item = None

    terminal.open()

    terminal.set(
        f'window: size={screen_width}x{screen_height}, cellsize=8x16, title="{window_title}"'
    )

    terminal.set("font: clacon.ttf, size=8x16")

    terminal.set(
        "0x1000: test_tiles.png, size=32x32, resize-filter=nearest, align=top-left"
    )

    terminal.set(
        "0x2000: inventory-ui.png, size=32x32, resize-filter=nearest, align=top-left"
    )

    camera = Camera()
    camera.move_camera(player.x, player.y, game_map)
    while game_running:
        if fov_recompute:
            game_map.compute_fov(x=player.x,
                                 y=player.y,
                                 radius=fov_radius,
                                 light_walls=fov_light_walls,
                                 algorithm=fov_algorithm)

        render_all(
            entities=entities,
            player=player,
            game_map=game_map,
            message_log=message_log,
            bar_width=bar_width,
            panel_y=panel_y,
            coordinates=mouse_coordinates,
            camera=camera,
            game_state=game_state,
            colors=colors,
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

            if game_state == GameStates.TARGETING:
                if left_click:
                    target_x, target_y = left_click
                    print(f"({target_x}, {target_y})")
                    print(f"({player.x}, {player.y})")
                    print(game_map.fov[target_x, target_y])
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
                    game_running = False

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

    terminal.close()


if __name__ == '__main__':
    main()
