from game_states import GameStates
from components.status_effects import resolve_effects
from turn_processing import player_turn, process_player_turn_results, process_player_effect_results, process_enemy_turns
from collections import deque


class Game:
    def __init__(self, player, entities, game_map, message_log, state,
                 previous_state, fov_recompute, constants, camera,
                 mouse_coordinates, targeting_item):
        self.player = player
        self.entities = entities
        self.fighter_entities = [
            entity.fighter for entity in self.entities if entity.fighter
        ]
        self.entity_queue = deque(self.fighter_entities)
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
        self.current_actor = self.player

    def tick(self):

        player_turn_results = player_turn(self.player, self.entities,
                                          self.camera, self.game_map,
                                          self.state, self.previous_state,
                                          self.targeting_item)
        if not player_turn_results:
            return

        if player_turn_results:
            process_player_turn_results(player_turn_results, self)

        if self.state == GameStates.ENEMY_TURN:
            player_effect_results = resolve_effects(self.player.fighter)
            process_player_effect_results(player_effect_results, self)
            process_enemy_turns(self)