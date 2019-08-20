from bearlibterminal import terminal
from typing import Tuple, Iterable, Union, TYPE_CHECKING


class Camera:
    def __init__(self):
        self.width: int = int(terminal.state(terminal.TK_WIDTH) / 4)
        self.height: int = int((terminal.state(terminal.TK_HEIGHT) - 10) / 2)
        self.camera_x: int = 0
        self.camera_y: int = 0

    def move_camera(self, target_x: int, target_y: int, game_map):

        x = int(round(target_x - self.width / 2))
        y = int(round(target_y - self.height / 2))

        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > game_map.width - self.width:
            x = (game_map.width - self.width)
        if y > game_map.height - self.height:
            y = game_map.height - self.height

        if x == self.camera_x and y == self.camera_y:
            return False  # Camera didn't move

        self.camera_x, self.camera_y = x, y

        return True  # Camera did move

    def to_camera_coordinates(self, x: int, y: int):

        (x, y) = (x - self.camera_x, y - self.camera_y)

        if (x < 0 or y < 0 or x >= self.width or y >= self.height):
            return (None, None)
        return (x, y)

    def map_to_cam_coord(self, map_x: int, map_y: int):
        # Convert game map coordinates to camera shooting range coordinates.
        cam_x: int = (map_x - self.camera_x)
        cam_y: int = (map_y - self.camera_y)

        if 0 <= cam_x < self.width and 0 <= cam_y < self.height:
            return (cam_x, cam_y)

        return (None, None)  # if it's outside the camera, return nothing

    def map_to_term_coord(self, map_x: int, map_y: int):
        # Convert game map coordinates to terminal screen coordinates.
        (cam_x, cam_y) = self.map_to_cam_coord(map_x, map_y)

        if cam_x is not None:
            return (cam_x * 4, cam_y * 2)

        return (None, None
                )  # if outside of the camera (or screen), return nothing