import tcod
from random import randint
from game_messages import Message
from entity import get_blocking_entities_at_location
import time


class GenericTarget:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class BasicMonster:
    def __init__(self, extra_movements=0, extra_attacks=0):
        self.owner = None
        self.extra_movements = extra_movements
        self.extra_attacks = extra_attacks
        self.last_player_position = None
        self.scent_tile = None

    def find_and_update_scent_tile(self, game_map):
        """
        Scan monster's surrounding tiles for player scent and find the coordinates
        where the scent value is highest. The monster will track the player
        by scent if it's not in the player's fov.
        """
        scent_coordinates = {}

        for x in range(-1, 2):
            for y in range(-1, 2):
                target_x = min(game_map.width - 1, self.owner.x + x)
                target_y = min(game_map.height - 1, self.owner.y + y)

                if (target_x, target_y) in game_map.scent_tiles:
                    scent_coordinates.update({
                        (target_x, target_y):
                        game_map.scent_tiles[(target_x, target_y)]
                    })

        if scent_coordinates:
            max_scent_tile = max(scent_coordinates, key=scent_coordinates.get)
            if scent_coordinates[(max_scent_tile)] > 15:
                x, y = max_scent_tile
                self.scent_tile = GenericTarget(x, y)

    def take_turn(self, target, game_map, entities):
        """
        The monster will work in the following sequence:
        1. If in player's fov, move towards player if the distance is above 2
        2. Attack player if in neighboring tile
        3. Move towards player's last location
        4. If no last location, move towards the highest scent tile
        5. Reset the scent tile if the distance to player is above 25
        """
        results = []
        extra_move_count = self.extra_movements
        extra_attack_count = self.extra_attacks
        monster = self.owner

        if self.owner.distance_to(target) < 25:
            self.find_and_update_scent_tile(game_map)
        elif self.scent_tile and self.owner.distance_to(target) > 25:
            self.scent_tile = None

        if game_map.fov[monster.x][monster.y]:

            self.last_player_position = GenericTarget(target.x, target.y)
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, game_map, entities)
                results.append({"move": True})
                while extra_move_count > 0:
                    if monster.distance_to(target) < 2:
                        break
                    monster.move_astar(target, game_map, entities)

            elif target.fighter.current_hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
                results.append({"attack": True})
                while extra_attack_count > 0:
                    attack_results = monster.fighter.attack(target)
                    results.extend(attack_results)
                    extra_attack_count -= 1

        elif self.last_player_position:
            monster.move_astar(self.last_player_position, game_map, entities)
            results.append({"move": True})
            while extra_move_count > 0:
                if self.owner.x == self.last_player_position.x and self.owner.y == self.last_player_position.y:
                    break
                monster.move_astar(self.last_player_position, game_map,
                                   entities)

            if self.owner.x == self.last_player_position.x and self.owner.y == self.last_player_position.y:
                self.last_player_position = None

        elif self.scent_tile:
            self.owner.x = self.scent_tile.x
            self.owner.y = self.scent_tile.y
            results.append({"move": True})
        else:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y and not get_blocking_entities_at_location(
                    entities, random_x, random_y):
                self.owner.move_towards(random_x, random_y, game_map, entities)
            results.append({"move": True})
        return results


class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns
        self.owner = None

    def take_turn(self, target, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y and not get_blocking_entities_at_location(
                    entities, random_x, random_y):
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1

        else:
            self.owner.ai = self.previous_ai
            results.append({
                "message":
                Message(f"The {self.owner.name} is no longer confused!", "red")
            })
        return results