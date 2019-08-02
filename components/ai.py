import tcod
from random import randint
from game_messages import Message
from entity import get_blocking_entities_at_location


class BasicMonster:
    def __init__(self):
        self.owner = None

    def take_turn(self, target, game_map, entities):
        results = []

        monster = self.owner

        if game_map.fov[monster.x][monster.y]:

            if monster.distance_to(target) >= 2:
                monster.move_astar(target, game_map, entities)

            elif target.fighter.current_hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
        self.owner.fighter.energy -= 100
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