from random import randint
from components.item import Item
from bearlibterminal import terminal
import numpy
from tcod.map import Map
from render_order import RenderOrder
from enum import Enum, auto
from components.fighter import Fighter
from components.ai import BasicMonster
from entity import Entity
from item_functions import heal, cast_chaos_bolt, cast_fireball, cast_confuse
from game_messages import Message


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
    def __init__(self, width, height):
        super().__init__(width=width, height=height, order='F')

        self.explored = numpy.zeros((width, height), dtype=bool, order='F')
        self.transparent[:] = False
        self.walkable[:] = False

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
                 map_height, player, entities, max_monsters_per_room,
                 max_items_per_room):
        rooms = []
        num_rooms = 0

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

                self.place_entities(new_room, entities, max_monsters_per_room,
                                    max_items_per_room)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

    def place_entities(self, room, entities, max_monsters_per_room,
                       max_items_per_room):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        for _i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([
                    entity
                    for entity in entities if entity.x == x and entity.y == y
            ]):
                if randint(0, 100) < 80:
                    fighter_component = Fighter(hp=10, defense=0, power=3)
                    ai_component = BasicMonster()
                    monster = Entity(x=x,
                                     y=y,
                                     char=0x1002,
                                     color="white",
                                     name='Orc',
                                     blocks=True,
                                     render_order=RenderOrder.ACTOR,
                                     fighter=fighter_component,
                                     ai=ai_component)
                else:
                    fighter_component = Fighter(hp=16, defense=1, power=4)
                    ai_component = BasicMonster()
                    monster = Entity(x=x,
                                     y=y,
                                     char=0x1003,
                                     color="white",
                                     name='Troll',
                                     blocks=True,
                                     render_order=RenderOrder.ACTOR,
                                     fighter=fighter_component,
                                     ai=ai_component)

                entities.append(monster)

        for _i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([
                    entity
                    for entity in entities if entity.x == x and entity.y == y
            ]):
                item_chance = randint(0, 100)

                if item_chance < 70:
                    item_component = Item(use_function=heal, amount=4)

                    item = Entity(x,
                                  y,
                                  0x1005,
                                  "violet",
                                  'Potion of Healing',
                                  render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_chance < 80:
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
                elif item_chance < 90:
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
                        terminal.put(x=x * 4, y=y * 2, c=0x1000)
                    else:
                        terminal.put(x=x * 4, y=y * 2, c=0x1001)

                elif self.explored[map_x, map_y]:
                    terminal.color(terminal.color_from_name("grey"))
                    if wall:
                        terminal.put(x=x * 4, y=y * 2, c=0x1000)
                    else:
                        terminal.put(x=x * 4, y=y * 2, c=0x1001)

        self.explored = self.explored | self.fov
