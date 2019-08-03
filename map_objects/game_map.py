from random import randint
from components.item import Item
from bearlibterminal import terminal
import numpy
from tcod.map import Map
from render_order import RenderOrder
from enum import Enum, auto
from components.fighter import Fighter
from components.ai import BasicMonster
from components.stairs import Stairs
from components.equipment import Equipment
from components.inventory import Inventory
from components.attributes import generate_attributes
from entity import Entity
from game_messages import Message
from item_functions import heal, cast_chaos_bolt, cast_fireball, cast_confuse
from random_utils import from_dungeon_level,random_choice_from_dict

WALL_NORTH = 0x3000
WALL_SOUTH = 0x3001
WALL_WEST = 0x3002
WALL_EAST = 0x3003
IN_CORNER_TOP_LEFT = 0x3004
IN_CORNER_TOP_RIGHT = 0x3005
IN_CORNER_BOTTOM_RIGHT = 0x3006
IN_CORNER_BOTTOM_LEFT = 0x3007
OUT_CORNER_TOP_LEFT = 0x3008
OUT_CORNER_TOP_RIGHT = 0x3009
OUT_CORNER_BOTTOM_LEFT = 0x300a
OUT_CORNER_BOTTOM_RIGHT = 0x300b
WALL_HORIZONTAL_BOTH_SIDES = 0x3015
WALL_VERTICAL_BOTH_SIDES = 0x301a
WALL_END_EAST = 0x3016
WALL_END_WEST = 0x3017
WALL_END_NORTH = 0x3018
WALL_END_SOUTH = 0x3019

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1
                and self.y1 <= other.y2 and self.y2 >= other.y1)


class GameMap(Map):
    def __init__(self, width, height, dungeon_level=1):
        super().__init__(width=width, height=height, order='F')

        self.explored = numpy.zeros((width, height), dtype=bool, order='F')
        self.transparent[:] = False
        self.walkable[:] = False
        self.floor_seed = [[None for y in range(height)] for x in range(width)]
        for map_y in range(height):
            for map_x in range(width):
                floor_tile = randint(1, 8)
                self.floor_seed[map_x][map_y] = floor_tile

        self.dungeon_level = dungeon_level
        self.effects = []

    def create_h_tunnel(self, x1, x2, y):
        min_x: int = min(x1, x2)
        max_x: int = max(x1, x2) + 1

        self.walkable[min_x:max_x, y] = True
        self.transparent[min_x:max_x, y] = True

    def create_room(self, room):
        self.walkable[room.x1 + 1:room.x2, room.y1 + 1:room.y2] = True
        self.transparent[room.x1 + 1:room.x2, room.y1 + 1:room.y2] = True

    def create_v_tunnel(self, y1, y2, x):
        min_y: int = min(y1, y2)
        max_y: int = max(y1, y2) + 1

        self.walkable[x, min_y:max_y] = True
        self.transparent[x, min_y:max_y] = True

    def is_blocked(self, x, y):
        return not self.walkable[x, y]

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width,
                 map_height, player, entities):

        self.explored = numpy.zeros((self.width, self.height), dtype=bool, order='F')
        self.transparent[:] = False
        self.walkable[:] = False
        self.floor_seed = [[None for y in range(self.height)] for x in range(self.width)]
        for map_y in range(self.height):
            for map_x in range(self.width):
                floor_tile = randint(1, 8)
                self.floor_seed[map_x][map_y] = floor_tile

        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, 0x1001, "white", "Stairs", render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    def place_entities(self, room, entities):
        # Get a random number of monsters

        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)

        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        monster_chances = {
            'orc':
            80,
            'troll':
            from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
        }
        item_chances = {
            'potion_of_healing': 35,
            'scroll_of_chaos_bolt': from_dungeon_level([[25, 4]],
                                                   self.dungeon_level),
            'scroll_of_fireball': from_dungeon_level([[25, 6]],
                                                  self.dungeon_level),
            'scroll_of_confusion': from_dungeon_level([[10, 2]],
                                                   self.dungeon_level)
        }

        for _i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([
                    entity
                    for entity in entities if entity.x == x and entity.y == y
            ]):
                monster_choice = random_choice_from_dict(monster_chances)
                equipment_component = Equipment()
                inventory_component = Inventory(26)

                if monster_choice == "orc":
                    inventory_seed = randint(1, 20)
                    fighter_component = Fighter(
                        generate_attributes(16, 13, 12, 16, 7, 11, 10, 10),
                        current_hp=25,
                        base_armor_class=12,
                        base_armor=0,
                        base_cth_modifier=0,
                        base_speed=95,
                        base_attack_cost=100,
                        base_movement_cost=100,
                        base_natural_hp_regeneration_speed=25,
                        xp_reward=35,
                        base_damage_modifiers={
                            "physical": 2,
                            "fire": 1
                        },
                        base_damage_dice={
                            "physical": [[1, 6]],
                            "fire": [[1, 1]],
                            "ice": [],
                            "lightning": [],
                            "holy": [],
                            "chaos": [],
                            "arcane": [],
                            "poison": [],
                        })
                    ai_component = BasicMonster()
                    monster = Entity(x=x,
                                     y=y,
                                     char=0x1002,
                                     color="white",
                                     name='Orc',
                                     blocks=True,
                                     render_order=RenderOrder.ACTOR,
                                     fighter=fighter_component,
                                     ai=ai_component,
                                     inventory=inventory_component,
                                     equipment=equipment_component)

                    item_component = Item(use_function=heal, amount=4)

                    item = Entity(x,
                                  y,
                                  0x1005,
                                  "violet",
                                  'Potion of Healing',
                                  render_order=RenderOrder.ITEM,
                                  item=item_component)

                    if inventory_seed >= 10:
                        monster.inventory.items.append(item)
                else:
                    fighter_component = Fighter(
                        generate_attributes(19, 14, 13, 20, 7, 9, 7, 14),
                        current_hp=30,
                        base_armor_class=9,
                        base_armor=2,
                        base_cth_modifier=5,
                        base_speed=80,
                        base_attack_cost=100,
                        base_movement_cost=100,
                        base_natural_hp_regeneration_speed=33,
                        base_damage_modifiers={
                            "physical": 10,
                            "fire": 2
                        },
                        base_damage_dice={
                            "physical": [[1, 10]],
                            "fire": [],
                            "ice": [],
                            "lightning": [],
                            "holy": [],
                            "chaos": [],
                            "arcane": [],
                            "poison": [],
                        },
                        xp_reward=100,
                    )
                    ai_component = BasicMonster()
                    monster = Entity(x=x,
                                     y=y,
                                     char=0x1003,
                                     color="white",
                                     name='Troll',
                                     blocks=True,
                                     render_order=RenderOrder.ACTOR,
                                     fighter=fighter_component,
                                     ai=ai_component,
                                     inventory=inventory_component,
                                     equipment=equipment_component)

                entities.append(monster)

        for _i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([
                    entity
                    for entity in entities if entity.x == x and entity.y == y
            ]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == "potion_of_healing":
                    item_component = Item(use_function=heal, amount=4)

                    item = Entity(x,
                                  y,
                                  0x1005,
                                  "violet",
                                  'Potion of Healing',
                                  render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == "scroll_of_fireball":
                    item_component = Item(
                        use_function=cast_fireball,
                        targeting=True,
                        targeting_message=Message(
                            'Left-click a target tile for the fireball, or right-click to cancel.',
                            "light cyan"),
                        damage=15,
                        radius=2)

                    item = Entity(x,
                                  y,
                                  0x1007,
                                  "red",
                                  'Scroll of Fireball',
                                  render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == "scroll_of_confusion":
                    item_component = Item(
                        use_function=cast_confuse,
                        targeting=True,
                        targeting_message=Message(
                            'Left-click an enemy to confuse it, or right-click to cancel.',
                            "light cyan"))
                    item = Entity(x,
                                  y,
                                  0x1007,
                                  "light pink",
                                  'Confusion Scroll',
                                  render_order=RenderOrder.ITEM,
                                  item=item_component)
                else:
                    chaos_bolt_damage = 0

                    for _i in range(5):
                        chaos_bolt_damage += randint(1, 6)

                    item_component = Item(use_function=cast_chaos_bolt,
                                          damage=chaos_bolt_damage,
                                          maximum_range=5)

                    item = Entity(x,
                                  y,
                                  0x1007,
                                  "crimson",
                                  'Scroll of Chaos Bolt',
                                  render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)

    def render_from_camera(self, camera):

        for y in range(camera.height):
            for x in range(camera.width):

                (map_x, map_y) = (camera.camera_x + x, camera.camera_y + y)

                wall = self.is_blocked(map_x, map_y)
                visible = self.fov[map_x, map_y]

                if visible:
                    terminal.color(terminal.color_from_name("white"))
                    if wall:
                        # Check for single-width walls first
                        if self.transparent[
                                map_x, min(self.height - 1, map_y -
                                           1)] and self.transparent[
                                               map_x,
                                               min(self.height - 1, map_y +
                                                   1)] and self.transparent[min(self.width - 1, map_x + 1), map_y]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=WALL_END_EAST)
                        elif self.transparent[
                                map_x, min(self.height - 1, map_y -
                                           1)] and self.transparent[
                                               map_x,
                                               min(self.height - 1, map_y + 1
                                                   )] and self.transparent[min(
                                                       self.width - 1, map_x -
                                                       1), map_y]:
                            terminal.put(x=x * 4, y=y * 2, c=WALL_END_WEST)
                        elif self.transparent[min(self.width - 1, map_x + 1),
                                              map_y] and self.transparent[min(
                                                  self.width - 1, map_x -
                                                  1), map_y] and self.transparent[map_x, min(self.height - 1, map_y - 1)]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=WALL_END_NORTH)
                        elif self.transparent[min(
                                self.width - 1, map_x + 1
                        ), map_y] and self.transparent[min(
                                self.width - 1, map_x - 1
                        ), map_y] and self.transparent[
                                map_x, min(self.height - 1, map_y + 1)]:
                            terminal.put(x=x * 4, y=y * 2, c=WALL_END_SOUTH)
                        elif self.transparent[
                                map_x, min(self.height - 1, map_y -
                                           1)] and self.transparent[
                                               map_x,
                                               min(self.height - 1, map_y +
                                                   1)]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=WALL_HORIZONTAL_BOTH_SIDES)
                        elif self.transparent[min(self.width - 1, map_x + 1),
                                              map_y] and self.transparent[min(
                                                  self.width - 1, map_x -
                                                  1), map_y]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=WALL_VERTICAL_BOTH_SIDES)
                        # Check for outward facing corners
                        elif self.transparent[min(
                                self.width - 1, map_x - 1
                        ), map_y] and self.transparent[
                                map_x, min(self.height - 1, map_y -
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x - 1),
                                               min(self.height - 1, map_y -
                                                   1)]:
                            terminal.put(x=x * 4, y=y * 2, c=OUT_CORNER_TOP_LEFT)
                        elif self.transparent[min(
                                self.width - 1, map_x + 1
                        ), map_y] and self.transparent[
                                map_x, min(self.height - 1, map_y -
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x + 1),
                                               min(self.height - 1, map_y -
                                                   1)]:
                            terminal.put(x=x * 4, y=y * 2, c=OUT_CORNER_TOP_RIGHT)
                        elif self.transparent[min(
                                self.width - 1, map_x - 1
                        ), map_y] and self.transparent[
                                map_x, min(self.height - 1, map_y +
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x - 1),
                                               min(self.height - 1, map_y -
                                                   1)]:
                            terminal.put(x=x * 4, y=y * 2, c=OUT_CORNER_BOTTOM_LEFT)
                        elif self.transparent[min(
                                self.width - 1, map_x + 1
                        ), map_y] and self.transparent[
                                map_x, min(self.height - 1, map_y +
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x + 1),
                                               min(self.height - 1, map_y -
                                                   1)]:
                            terminal.put(x=x * 4, y=y * 2, c=OUT_CORNER_BOTTOM_RIGHT)
                        # Check for edges
                        elif self.transparent[map_x,
                                              min(self.height - 1, map_y + 1)]:
                            terminal.put(x=x * 4, y=y * 2, c=WALL_NORTH)
                        elif self.transparent[map_x,
                                              min(self.height - 1, map_y - 1)]:
                            terminal.put(x=x * 4, y=y * 2, c=WALL_SOUTH)
                        elif self.transparent[min(self.width - 1, map_x +
                                                  1), map_y]:
                            terminal.put(x=x * 4, y=y * 2, c=WALL_WEST)
                        elif self.transparent[min(self.width - 1, map_x -
                                                  1), map_y]:
                            terminal.put(x=x * 4, y=y * 2, c=WALL_EAST)

                        # Check for inward facing corners
                        elif not self.transparent[min(
                                self.width - 1, map_x + 1
                        ), map_y] and not self.transparent[
                                map_x, min(self.height - 1, map_y +
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x + 1),
                                               min(self.height - 1, map_y +
                                                   1)]:
                            terminal.put(x=x * 4, y=y * 2, c=IN_CORNER_TOP_LEFT)
                        elif not self.transparent[min(
                                self.width - 1, map_x - 1
                        ), map_y] and not self.transparent[
                                map_x, min(self.height - 1, map_y +
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x - 1),
                                               min(self.height - 1, map_y +
                                                   1)]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=IN_CORNER_TOP_RIGHT)
                        elif not self.transparent[min(
                                self.width - 1, map_x - 1
                        ), map_y] and not self.transparent[
                                map_x, min(self.height - 1, map_y -
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x - 1),
                                               min(self.height - 1, map_y -
                                                   1)]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=IN_CORNER_BOTTOM_RIGHT)
                        elif not self.transparent[min(
                                self.width - 1, map_x + 1
                        ), map_y] and not self.transparent[
                                map_x, min(self.height - 1, map_y -
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x + 1),
                                               min(self.height - 1, map_y -
                                                   1)]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=IN_CORNER_BOTTOM_LEFT)


                    else:
                        tile_type = self.floor_seed[map_x][map_y]
                        terminal.put(x=x * 4,
                                     y=y * 2,
                                     c=0x3000 + 11 + tile_type)

                elif self.explored[map_x, map_y]:
                    terminal.color(terminal.color_from_name("grey"))
                    if wall:
                        # Check for single-width walls first
                        if self.transparent[
                                map_x, min(self.height - 1, map_y -
                                           1)] and self.transparent[
                                               map_x,
                                               min(self.height - 1, map_y + 1
                                                   )] and self.transparent[min(
                                                       self.width - 1, map_x +
                                                       1), map_y]:
                            terminal.put(x=x * 4, y=y * 2, c=WALL_END_EAST)
                        elif self.transparent[
                                map_x, min(self.height - 1, map_y -
                                           1)] and self.transparent[
                                               map_x,
                                               min(self.height - 1, map_y + 1
                                                   )] and self.transparent[min(
                                                       self.width - 1, map_x -
                                                       1), map_y]:
                            terminal.put(x=x * 4, y=y * 2, c=WALL_END_WEST)
                        elif self.transparent[min(
                                self.width - 1, map_x + 1
                        ), map_y] and self.transparent[min(
                                self.width - 1, map_x - 1
                        ), map_y] and self.transparent[
                                map_x, min(self.height - 1, map_y - 1)]:
                            terminal.put(x=x * 4, y=y * 2, c=WALL_END_NORTH)
                        elif self.transparent[min(
                                self.width - 1, map_x + 1
                        ), map_y] and self.transparent[min(
                                self.width - 1, map_x - 1
                        ), map_y] and self.transparent[
                                map_x, min(self.height - 1, map_y + 1)]:
                            terminal.put(x=x * 4, y=y * 2, c=WALL_END_SOUTH)
                        elif self.transparent[
                                map_x, min(self.height - 1, map_y -
                                           1)] and self.transparent[
                                               map_x,
                                               min(self.height - 1, map_y +
                                                   1)]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=WALL_HORIZONTAL_BOTH_SIDES)
                        elif self.transparent[min(self.width - 1, map_x + 1),
                                              map_y] and self.transparent[min(
                                                  self.width - 1, map_x -
                                                  1), map_y]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=WALL_VERTICAL_BOTH_SIDES)
                        # Check for outward facing corners
                        elif self.transparent[min(
                                self.width - 1, map_x - 1
                        ), map_y] and self.transparent[
                                map_x, min(self.height - 1, map_y -
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x - 1),
                                               min(self.height - 1, map_y -
                                                   1)]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=OUT_CORNER_TOP_LEFT)
                        elif self.transparent[min(
                                self.width - 1, map_x + 1
                        ), map_y] and self.transparent[
                                map_x, min(self.height - 1, map_y -
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x + 1),
                                               min(self.height - 1, map_y -
                                                   1)]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=OUT_CORNER_TOP_RIGHT)
                        elif self.transparent[min(
                                self.width - 1, map_x - 1
                        ), map_y] and self.transparent[
                                map_x, min(self.height - 1, map_y +
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x - 1),
                                               min(self.height - 1, map_y -
                                                   1)]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=OUT_CORNER_BOTTOM_LEFT)
                        elif self.transparent[min(
                                self.width - 1, map_x + 1
                        ), map_y] and self.transparent[
                                map_x, min(self.height - 1, map_y +
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x + 1),
                                               min(self.height - 1, map_y -
                                                   1)]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=OUT_CORNER_BOTTOM_RIGHT)
                        # Check for edges
                        elif self.transparent[map_x,
                                              min(self.height - 1, map_y + 1)]:
                            terminal.put(x=x * 4, y=y * 2, c=WALL_NORTH)
                        elif self.transparent[map_x,
                                              min(self.height - 1, map_y - 1)]:
                            terminal.put(x=x * 4, y=y * 2, c=WALL_SOUTH)
                        elif self.transparent[min(self.width - 1, map_x +
                                                  1), map_y]:
                            terminal.put(x=x * 4, y=y * 2, c=WALL_WEST)
                        elif self.transparent[min(self.width - 1, map_x -
                                                  1), map_y]:
                            terminal.put(x=x * 4, y=y * 2, c=WALL_EAST)

                        # Check for inward facing corners
                        elif not self.transparent[min(
                                self.width - 1, map_x + 1
                        ), map_y] and not self.transparent[
                                map_x, min(self.height - 1, map_y +
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x + 1),
                                               min(self.height - 1, map_y +
                                                   1)]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=IN_CORNER_TOP_LEFT)
                        elif not self.transparent[min(
                                self.width - 1, map_x - 1
                        ), map_y] and not self.transparent[
                                map_x, min(self.height - 1, map_y +
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x - 1),
                                               min(self.height - 1, map_y +
                                                   1)]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=IN_CORNER_TOP_RIGHT)
                        elif not self.transparent[min(
                                self.width - 1, map_x - 1
                        ), map_y] and not self.transparent[
                                map_x, min(self.height - 1, map_y -
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x - 1),
                                               min(self.height - 1, map_y -
                                                   1)]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=IN_CORNER_BOTTOM_RIGHT)
                        elif not self.transparent[min(
                                self.width - 1, map_x + 1
                        ), map_y] and not self.transparent[
                                map_x, min(self.height - 1, map_y -
                                           1)] and self.transparent[
                                               min(self.width - 1, map_x + 1),
                                               min(self.height - 1, map_y -
                                                   1)]:
                            terminal.put(x=x * 4,
                                         y=y * 2,
                                         c=IN_CORNER_BOTTOM_LEFT)

                    else:
                        tile_type = self.floor_seed[map_x][map_y]
                        terminal.put(x=x * 4,
                                     y=y * 2,
                                     c=0x3000 + 11 + tile_type)

        self.explored = self.explored | self.fov

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.make_map(constants["max_rooms"], constants["room_min_size"],
                          constants["room_max_size"], constants["map_width"],
                          constants["map_height"], player, entities)

        player.fighter.heal(player.fighter.max_hp // 4)

        message_log.add_message(
            Message('You take a moment to rest and recover your strength.',
                    "violet"))

        return entities