import tcod
from random import randint
from game_messages import Message
from entity import get_blocking_entities_at_location


class BasicMonster:
    def __init__(self, extra_movements=0, extra_attacks=0):
        self.owner = None
        self.extra_movements = extra_movements
        self.extra_attacks = extra_attacks

    def take_turn(self, target, game_map, entities):
        results = []
        extra_move_count = self.extra_movements
        extra_attack_count = self.extra_attacks
        monster = self.owner

        if game_map.fov[monster.x][monster.y]:

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