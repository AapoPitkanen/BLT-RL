from bearlibterminal import terminal


class GameView():
    def __init__(self, player, game_map):
        self.width = int(game_map.width / 2)
        self.height = int(game_map.height / 2)
        self.origin_x = player.x - (int(self.width / 2))
        self.origin_y = player.y - (int(self.height / 2))

    def recalculate_origin(self, player, game_map):

        terminal_width = terminal.state(terminal.TK_WIDTH)
        terminal_height = terminal.state(terminal.TK_HEIGHT)

        self.origin_x = player.x - (int(self.width / 2))
        self.origin_y = player.y - (int(self.height / 2))

        if self.origin_x < 0:
            self.origin_x = 0

        if self.origin_y < 0:
            self.origin_y = 0

        if self.origin_x + self.width > game_map.width:
            self.origin_x -= (self.origin_x + terminal_width - game_map.width)
            self.origin_y -= (self.origin_y + terminal_height -
                              game_map.height)
