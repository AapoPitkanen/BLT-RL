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

    @property
    def fighter_entities(self):
        return [entity.fighter for entity in self.entities if entity.fighter]

    @property
    def monster_fighter_entities(self):
        return [entity.fighter for entity in self.entities if entity.ai]

    def tick(self) -> None:

        # Get a list of dicts where the results are specified e.g. {"move": True}
        player_turn_results = player_turn(self.player, self.entities,
                                          self.camera, self.game_map,
                                          self.state, self.previous_state,
                                          self.targeting_item)

        # Wait for player input during player's turn, the list will be empty if the player didn't do anything
        if self.state == GameStates.PLAYERS_TURN and not player_turn_results:
            return

        # After getting input the results will be processed
        if player_turn_results:
            process_player_turn_results(player_turn_results, self)

        # Enemy turns are processed only after all animations have been processed and rendered
        # The gfx_effects list will be empty after all effects have been rendered.
        if len(self.game_map.gfx_effects) > 0:
            return

        if self.state == GameStates.ENEMY_TURN:
            self.game_map.update_scent_tiles(self.player)
            # Resolve and process all status effects
            player_effect_results = resolve_effects(self.player.fighter)
            process_player_effect_results(player_effect_results, self)

            # If the player has actions remaining after his turn, switch back to player
            if self.player.fighter.actions > 0:
                self.state = GameStates.PLAYERS_TURN
                return

            # Run enemy turns until the player gets enough energy to act
            while self.player.fighter.actions <= 0:
                for fighter in self.fighter_entities:
                    if fighter.speed > 0:
                        fighter.energy += fighter.speed
                        if fighter.owner.ai:
                            fighter.energy += randint(-5, 10)

                for fighter in self.fighter_entities:
                    fighter.actions += int(
                        fighter.energy /
                        self.constants["speed_action_divisor"])
                    if fighter.actions > 0:
                        fighter.energy -= fighter.actions * self.constants[
                            "speed_action_divisor"]

                for monster in self.monster_fighter_entities:
                    turns_taken = 0
                    while (monster.actions > 0):
                        turns_taken += 1
                        process_enemy_turn(self, monster.owner)
                        monster.actions -= 1

            if self.state != GameStates.PLAYER_DEAD:
                self.state = GameStates.PLAYERS_TURN