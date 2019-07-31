from bearlibterminal import terminal


class Camera:
    def __init__(self, margin=0):
        self.camera_width = terminal.state(terminal.TK_WIDTH)
        self.camera_height = terminal.state(terminal.TK_HEIGHT) - 6
        self.camera_x = 0
        self.camera_y = 0
        self.margin = margin

    def move_camera(self, target_x, target_y, game_map):

        x = int(round(target_x - self.camera_width / 2))
        y = int(round(target_y - self.camera_height / 2))

        if x < -self.margin:
            x = -self.margin
        if y < -self.margin:
            y = -self.margin
        if x > game_map.width - self.camera_width + self.margin:
            x = game_map.width - self.camera_width + self.margin
        if y > game_map.height - self.camera_height + self.margin:
            y = game_map.height - self.camera_height + self.margin

        if x == self.camera_x and y == self.camera_y:
            return False

        self.camera_x, self.camera_y = x, y

        return True  # camera moved

    def to_camera_coordinates(self, x, y):

        (x, y) = (x - self.camera_x, y - self.camera_y)

        if (x < 0 or y < 0 or x >= self.camera_width
                or y >= self.camera_height):
            return (None, None)
        return (x, y)
