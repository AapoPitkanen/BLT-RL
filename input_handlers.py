from bearlibterminal import terminal
from game_states import GameStates


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)

    return {}


def handle_player_turn_keys(key):
    if key == terminal.TK_UP or key == terminal.TK_KP_8:
        return {"movement": (0, -1)}
    elif key == terminal.TK_DOWN or key == terminal.TK_KP_2:
        return {"movement": (0, 1)}
    elif key == terminal.TK_LEFT or key == terminal.TK_KP_4:
        return {"movement": (-1, 0)}
    elif key == terminal.TK_RIGHT or key == terminal.TK_KP_6:
        return {"movement": (1, 0)}
    elif key == terminal.TK_KP_1:
        return {"movement": (-1, 1)}
    elif key == terminal.TK_KP_3:
        return {"movement": (1, 1)}
    elif key == terminal.TK_KP_7:
        return {"movement": (-1, -1)}
    elif key == terminal.TK_KP_9:
        return {"movement": (1, -1)}
    elif key == terminal.TK_KP_5:
        return {"pass_turn": True}
    elif key == terminal.TK_G:
        return {"pickup": True}
    elif key == terminal.TK_I:
        return {"show_inventory": True}
    elif key == terminal.TK_D:
        return {"drop_inventory": True}
    elif key == terminal.TK_ENTER:
        return {"take_stairs": True}
    elif key == terminal.TK_ESCAPE:
        return {"escape": True}

    return {}


def handle_targeting_keys(key):
    if key == terminal.TK_ESCAPE:
        return {"escape": True}

    return {}


def handle_player_dead_keys(key):

    if key == terminal.TK_I:
        return {"show_inventory": True}
    elif key == terminal.TK_ESCAPE:
        return {"escape": True}

    return {}


def handle_inventory_keys(key):

    index = terminal.state(terminal.TK_CHAR) - ord('a')

    if index >= 0:
        return {"inventory_index": index}

    if key == terminal.TK_ESCAPE:
        return {"escape": True}

    return {}


def handle_main_menu(key):
    if key == terminal.TK_A:
        return {"new_game": True}
    elif key == terminal.TK_B:
        return {"load_game": True}
    elif key == terminal.TK_C or key == terminal.TK_ESCAPE:
        return {"exit": True}

    return {}


def handle_mouse(key, camera):
    #Handle mouse input and return screen coordinate, accounting for cellsize 8x16.

    (mouse_x, mouse_y) = ((int(terminal.state(terminal.TK_MOUSE_X) / 4)),
                          (int(terminal.state(terminal.TK_MOUSE_Y) / 2)))

    (mouse_x, mouse_y) = (camera.camera_x + mouse_x, camera.camera_y + mouse_y)

    if key == terminal.TK_MOUSE_LEFT:
        return {"left_click": (mouse_x, mouse_y)}
    elif key == terminal.TK_MOUSE_RIGHT:
        return {"right_click": (mouse_x, mouse_y)}

    return {}