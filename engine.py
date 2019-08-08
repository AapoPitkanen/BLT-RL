from typing import List, TYPE_CHECKING
from bearlibterminal import terminal
import tcod
import time
from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game
from map_objects.game_map import GameMap
from input_handlers import handle_main_menu
from game_messages import MessageLog
from render_order import RenderOrder
from render_functions import render_all, clear_map_layer, clear_menu_layer, main_screen
from camera import Camera
from copy import deepcopy
from menu import main_menu, message_box
from game_states import GameStates
from game import Game

if TYPE_CHECKING:
    from entity import Entity

import cProfile


def main() -> None:

    terminal.open()
    constants = get_constants()
    terminal.set(
        f'window: size={constants["screen_width"]}x{constants["screen_height"]}, cellsize=8x16, title="{constants["window_title"]}"'
    )
    terminal.set("font: clacon.ttf, size=8x16")
    terminal.set(
        "0x1000: test_tiles3.png, size=32x32, resize-filter=nearest, align=top-left"
    )
    terminal.set(
        "0x2000: inventory-ui.png, size=32x32, resize-filter=nearest, align=top-left"
    )
    terminal.set(
        "0x3000: wall_tiles2.png, size=32x32, resize-filter=nearest, align=top-left"
    )
    terminal.set(
        "0x4000: voidstone_background_1536x864.png, size=1536x864, resize=1792x1008,resize-filter=nearest, align=top-left"
    )

    player = None
    entities: List["Entity"] = []
    game_map = None
    message_log = None
    game_state = None
    game = None
    camera = None
    targeting_item = None
    fov_recompute: bool = True

    show_main_menu: bool = True
    show_load_error_message: bool = False

    in_main_menu: bool = True

    while in_main_menu:
        start_time = time.perf_counter()  # Set up fps limiter
        if show_main_menu:
            main_screen()
            main_menu(constants['screen_width'], constants['screen_height'])

            if show_load_error_message:
                message_box(header='No saved game to load.',
                            width=50,
                            screen_width=constants['screen_width'],
                            screen_height=constants['screen_height'])

            if terminal.has_input():
                key: int = terminal.read()

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
                    mouse_coordinates = (player.x, player.y)
                    game_state = GameStates.PLAYERS_TURN
                    camera = Camera()
                    show_main_menu = False
                    game = Game(player, entities, game_map, message_log,
                                game_state, game_state, fov_recompute,
                                constants, camera, mouse_coordinates,
                                targeting_item)
                elif load_saved_game:
                    try:
                        player, entities, game_map, message_log, game_state = load_game(
                        )
                        mouse_coordinates = (player.x, player.y)
                        camera = Camera()
                        show_main_menu = False
                        game = Game(player, entities, game_map, message_log,
                                    game_state, game_state, fov_recompute,
                                    constants, camera, mouse_coordinates,
                                    targeting_item)
                    except FileNotFoundError:
                        show_load_error_message = True
                elif exit_game:
                    break

            terminal.refresh()
        else:
            terminal.clear()

            if game:
                play_game(game)

            terminal.clear()
            show_main_menu = True

        delta_time = (time.perf_counter() - start_time) * 1000
        terminal.delay(max(int(1000.0 / constants['fps'] - delta_time), 0))


def play_game(game: Game) -> None:
    while True:
        start_time = time.perf_counter()
        if game.fov_recompute:
            game.game_map.compute_fov(
                x=game.player.x,
                y=game.player.y,
                radius=game.player.fighter.fov_radius,
                light_walls=game.constants["fov_light_walls"],
                algorithm=game.constants["fov_algorithm"])

        render_all(entities=game.entities,
                   player=game.player,
                   game_map=game.game_map,
                   message_log=game.message_log,
                   bar_width=game.constants["bar_width"],
                   panel_y=game.constants["panel_y"],
                   coordinates=game.mouse_coordinates,
                   camera=game.camera,
                   game_state=game.state,
                   targeting_item=game.targeting_item)

        game.fov_recompute = False

        terminal.refresh()

        game.tick()

        if game.exit:
            return

        terminal.clear()

        delta_time = (time.perf_counter() - start_time) * 1000
        terminal.delay(max(int(1000.0 / game.constants['fps'] - delta_time),
                           0))


if __name__ == '__main__':
    main()