from typing import TYPE_CHECKING, List
from game_states import GameStates
from components.status_effects import resolve_effects
from turn_processing import player_turn, process_player_turn_results, process_player_effect_results, process_enemy_turn
from random import randint

if TYPE_CHECKING:
    from entity import Entity


class Game:
    def __init__(self, player, entities, game_map, message_log, state,
                 previous_state, fov_recompute, constants, camera,
                 mouse_coordinates, targeting_item):
        self.player = player
        self.entities = entities
        self.fighter_entities = [
            entity.fighter for entity in self.entities if entity.fighter
        ]
        self.monster_fighter_entities = [
            entity.fighter for entity in self.entities if entity.ai
        ]
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

    def refresh_entities(self) -> None:
        self.fighter_entities = [
            entity.fighter for entity in self.entities if entity.fighter
        ]
        self.monster_fighter_entities = [
            entity.fighter for entity in self.entities if entity.ai
        ]

    def tick(self) -> None:
        player_turn_results = player_turn(self.player, self.entities,
                                          self.camera, self.game_map,
                                          self.state, self.previous_state,
                                          self.targeting_item)
        if not player_turn_results:
            return

        if player_turn_results:
            process_player_turn_results(player_turn_results, self)

        if self.state == GameStates.ENEMY_TURN:
            self.game_map.update_scent_tiles(self.player)
            player_effect_results = resolve_effects(self.player.fighter)
            process_player_effect_results(player_effect_results, self)
            if self.player.fighter.actions > 0:
                self.state = GameStates.PLAYERS_TURN
                return

            for fighter in self.fighter_entities:
                fighter.energy += fighter.speed
                if fighter.owner.ai:
                    fighter.energy += randint(-5, 10)
            for fighter in self.fighter_entities:
                fighter.actions += int(fighter.energy /
                                       self.constants["speed_action_divisor"])
                fighter.energy -= fighter.actions * self.constants[
                    "speed_action_divisor"]

            for monster in self.monster_fighter_entities:
                while (monster.actions > 0):
                    process_enemy_turn(self, monster.owner)
                    monster.actions -= 1

            self.state = GameStates.PLAYERS_TURN