from typing import List, Optional, Any, TYPE_CHECKING
import math
from bearlibterminal import terminal
from components.item import Item
import tcod
from copy import deepcopy
from render_order import RenderOrder, RenderLayer

if TYPE_CHECKING:
    from map_objects.game_map import GameMap
    from camera import Camera


class Entity:
    # A generic class to represent objects in the game world
    def __init__(self,
                 x: int,
                 y: int,
                 char: int,
                 name: str,
                 blocks: bool = False,
                 render_order: RenderOrder = RenderOrder.CORPSE,
                 fighter=None,
                 ai=None,
                 item=None,
                 inventory=None,
                 stairs=None,
                 level=None,
                 equipment=None,
                 equippable=None,
                 path=None):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.blocks = blocks
        self.render_order: RenderOrder = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.equipment = equipment
        self.equippable = equippable
        self.path = path

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

        if self.equipment:
            self.equipment.owner = self

        if self.equippable:
            self.equippable.owner = self

            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

        if self.fighter and self.equipment:
            self.fighter.recalculate_hp()

    def draw(self, camera: "Camera", game_map: "GameMap") -> None:

        terminal.color(terminal.color_from_name("white"))
        """ if game_map.fov[self.x, self.y] or (self.stairs and
                                            game_map.explored[self.x, self.y]):
            (x, y) = camera.to_camera_coordinates(self.x, self.y)
            if x is not None:
                terminal.put(x=x * 4, y=y * 2, c=self.char) """
        (x, y) = camera.to_camera_coordinates(self.x, self.y)
        if x is not None:
            terminal.put(x=x * 4, y=y * 2, c=self.char)

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x: int, target_y: int, game_map: "GameMap",
                     entities: List["Entity"]) -> None:
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        if not (game_map.is_blocked(self.x + dx, self.y + dy)
                ) and not get_blocking_entities_at_location(
                    entities, self.x + dx, self.y + dy):
            self.move(dx, dy)

    def distance(self, x: int, y: int) -> float:
        return math.sqrt((x - self.x)**2 + (y - self.y)**2)

    def distance_to(self, other) -> float:
        dx: int = other.x - self.x
        dy: int = other.y - self.y
        return math.sqrt(dx**2 + dy**2)

    def move_astar(
            self,
            target: "Entity",
            game_map: "GameMap",
            entities: List["Entity"],
    ) -> None:
        '''
        Calculate the A* path toward a target Entity and save it to the Entity
        '''
        if not self.path:
            # Create a numpy array of the map for tcod astar path calculation (the recommended way)
            map_array = game_map.game_map_to_numpy_array()

            # Scan all the objects to see if there are objects that must be navigated around
            # Check also that the object isn't self or the target (so that the start and the end points are free)
            for entity in entities:
                if entity.blocks and entity is not self and entity is not target:
                    map_array[entity.x][entity.y] = 0

            # Allocate a A* path, store it to the entity if there isn't one
            astar = tcod.path.AStar(map_array)
            path = astar.get_path(self.x, self.y, target.x, target.y)

            if path and len(path) < 25:
                self.path = path
        # Check the stored path and move to the first path coordinates
        if self.path:
            x, y = self.path[0]
            dx = x - self.x
            dy = y - self.y
            if not get_blocking_entities_at_location(entities, x, y):
                self.move(dx, dy)
            else:
                # Reset the path so a new one will be calculated on the next turn
                self.path = None
                return
            # Remove the coordinates from the list so the next coordinates on the path are available
            self.path.pop(0)
        # Fallback if the path doesn't exist so the entity can still move
        else:
            self.move_towards(target.x, target.y, game_map, entities)


def get_blocking_entities_at_location(entities: List[Entity],
                                      destination_x: int,
                                      destination_y: int) -> Optional[Entity]:
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
