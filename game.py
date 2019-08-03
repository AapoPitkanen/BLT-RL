class Game:
    def __init__(self, player, entities, game_map, message_log, state,
                 previous_state, fov_recompute, constants, camera,
                 mouse_coordinates, targeting_item):
        self.player = player
        self.entities = entities
        self.game_map = game_map
        self.message_log = message_log
        self.state = state
        self.previous_state = previous_state
        self.fov_recompute = fov_recompute
        self.constants = constants
        self.camera = camera
        self.mouse_coordinates = mouse_coordinates
        self.exit = False
        self.targeting_item = targeting_item
