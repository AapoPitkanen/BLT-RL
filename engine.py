from bearlibterminal import terminal
import tcod
from entity import Entity, get_blocking_entities_at_location
from game_map import GameMap
from input_handlers import handle_keys, handle_mouse
from components.inventory import Inventory
from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from game_messages import MessageLog, Message
from game_states import GameStates
from render_order import RenderOrder
from render_functions import render_all


def main():
    window_title: str = 'Bearlibterm/TCOD Roguelike'

    screen_width: int = 120
    screen_height: int = 60
    map_width: int = 100
    map_height: int = 53

    room_max_size: int = 10
    room_min_size: int = 6
    max_rooms: int = 30

    fov_algorithm: int = 0
    fov_light_walls: bool = True
    fov_radius: int = 10

    max_monsters_per_room: int = 3
    max_items_per_room: int = 2

    bar_width: int = 20
    panel_height: int = 7
    panel_y: int = (screen_height - panel_height)

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    mouse_coordinates = (0, 0)
    cur_x, cur_y = 0, 0

    colors = {
        'dark_wall': terminal.color_from_argb(0, 38, 38, 38),
        'dark_ground': terminal.color_from_argb(0, 100, 100, 100),
        'light_wall': terminal.color_from_argb(255, 128, 128, 128),
        'light_ground': terminal.color_from_argb(0, 255, 255, 255)
    }

    game_running: bool = True

    fov_recompute: bool = True

    fighter_component = Fighter(hp=30, defense=2, power=5)

    inventory_component = Inventory(26)

    player: Entity = Entity(x=0,
                            y=0,
                            char='@',
                            color=terminal.color_from_argb(0, 255, 255, 255),
                            name='Player',
                            blocks=True,
                            render_order=RenderOrder.ACTOR,
                            fighter=fighter_component,
                            inventory=inventory_component)
    entities = [player]

    message_log = MessageLog(message_x, message_width, message_height)

    game_map: GameMap = GameMap(width=map_width, height=map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width,
                      map_height, player, entities, max_monsters_per_room,
                      max_items_per_room)

    game_state: GameStates = GameStates.PLAYERS_TURN

    terminal.open()
    terminal.set(
        f'window: size={screen_width}x{screen_height}, title="{window_title}";'
    )
    terminal.set("font: clacon.ttf, size=16x16;")

    while game_running:
        if fov_recompute:
            game_map.compute_fov(x=player.x,
                                 y=player.y,
                                 radius=fov_radius,
                                 light_walls=fov_light_walls,
                                 algorithm=fov_algorithm)

        render_all(entities=entities,
                   player=player,
                   game_map=game_map,
                   message_log=message_log,
                   bar_width=bar_width,
                   panel_y=panel_y,
                   mouse_coordinates=mouse_coordinates,
                   colors=colors)

        fov_recompute = False

        terminal.refresh()

        if terminal.has_input():
            terminal_input: int = terminal.read()

            if terminal_input == terminal.TK_MOUSE_MOVE:
                mouse_coordinates = (terminal.state(terminal.TK_MOUSE_X),
                                     terminal.state(terminal.TK_MOUSE_Y))

            action = handle_keys(terminal_input)
            mouse_action = handle_mouse(terminal_input)

            escape = action.get('escape')
            movement = action.get('movement')
            pickup = action.get("pickup")
            pass_turn = action.get("pass_turn")

            left_click = mouse_action.get("left_click")
            right_click = mouse_action.get('right_click')

            if left_click:
                print(left_click)

            if right_click:
                print(right_click)

            if escape:
                game_running = False

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

            for player_turn_result in player_turn_results:

                message = player_turn_result.get("message")
                dead_entity = player_turn_result.get("dead")
                item_added = player_turn_result.get("item_added")

                if message:
                    message_log.add_message(message)

                if dead_entity:
                    if dead_entity == player:
                        message, game_state = kill_player(dead_entity)
                    else:
                        message = kill_monster(dead_entity)

                    message_log.add_message(message)

                if item_added:
                    entities.remove(item_added)
                    game_state = GameStates.ENEMY_TURN

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
