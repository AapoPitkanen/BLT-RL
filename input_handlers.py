from bearlibterminal import terminal


def handle_keys(key: int):
    if key == terminal.TK_UP or key == terminal.TK_KP_8:
        return {'movement': (0, -1)}
    elif key == terminal.TK_DOWN or key == terminal.TK_KP_2:
        return {'movement': (0, 1)}
    elif key == terminal.TK_LEFT or key == terminal.TK_KP_4:
        return {'movement': (-1, 0)}
    elif key == terminal.TK_RIGHT or key == terminal.TK_KP_6:
        return {'movement': (1, 0)}
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
    elif key == terminal.TK_ESCAPE:
        return {'escape': True}

    return {}


def handle_mouse(key):
    #Handle mouse input and return screen coordinates.

    (mouse_x, mouse_y) = (terminal.state(terminal.TK_MOUSE_X),
                          terminal.state(terminal.TK_MOUSE_Y))

    if key == terminal.TK_MOUSE_LEFT:
        return {'left_click': (mouse_x, mouse_y)}
    elif key == terminal.TK_MOUSE_RIGHT:
        return {'right_click': (mouse_x, mouse_y)}

    return {}