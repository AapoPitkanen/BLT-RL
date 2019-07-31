from typing import List
import math
from bearlibterminal import terminal
import tcod
from copy import deepcopy
from render_order import RenderOrder, RenderLayer


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    # def __init__(self, x, y, char, color):
    def __init__(self,
                 x: int,
                 y: int,
                 char,
                 color,
                 name: str,
                 blocks: bool = False,
                 render_order=RenderOrder.CORPSE,
                 fighter=None,
                 ai=None,
                 item=None,
                 inventory=None,
                 equippable=None):
        self.x: int = x
        self.y: int = y
        self.char = char
        self.color = color
        self.name: str = name
        self.blocks: bool = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.equippable = equippable

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.equippable:
            self.equippable.owner = self

    def draw(self, camera, game_map):
        # Draw the entity to the terminal
        terminal.color(terminal.color_from_name("white"))

        if game_map.fov[self.x, self.y]:
            (x, y) = camera.to_camera_coordinates(self.x, self.y)
            if x is not None:
                terminal.put(x=x * 2, y=y, c=self.char)

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy)
                and not get_blocking_entities_at_location(
                    entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx**2 + dy**2)

    def move_astar(
            self,
            target,
            game_map,
            entities,
    ):
        map_copy = deepcopy(game_map)

        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                map_copy.walkable[entity.x][entity.y] = False

        astar = tcod.path.AStar(map_copy.walkable)
        new_path = astar.get_path(self.x, self.y, target.x, target.y)
        if new_path and len(new_path) < 25:
            x, y = new_path[0]
            if x or y:
                self.x = x
                self.y = y
        else:
            self.move_towards(target.x, target.y, game_map, entities)

        tcod.path_delete(new_path)


def get_blocking_entities_at_location(entities: List[Entity],
                                      destination_x: int,
                                      destination_y: int) -> [Entity, None]:
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
