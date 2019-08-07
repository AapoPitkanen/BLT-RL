from components.inventory import Inventory
from components.item import Item
from item_functions import cast_fireball, cast_chaos_bolt, cast_confuse
from components.fighter import Fighter
from components.equipment import Equipment
from components.level import Level
from components.attributes import roll_character_attributes
from components.armors import generate_random_armor
from entity import Entity
from render_order import RenderOrder
from game_messages import MessageLog, Message
from map_objects.game_map import GameMap
from random import randint
from game import GameStates


def get_constants():
    window_title: str = "Voidstone"
    fps = 30

    screen_width: int = 192
    screen_height: int = 54

    map_width: int = 80
    map_height: int = 60

    room_max_size: int = 12
    room_min_size: int = 5
    max_rooms: int = 60

    fov_algorithm: int = 0
    fov_light_walls: bool = True

    max_monsters_per_room: int = 3
    max_items_per_room: int = 2

    bar_width: int = 20
    panel_height: int = 9
    panel_y: int = (screen_height - panel_height - 1)

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    speed_action_divisor = 100

    constants = {
        "window_title": window_title,
        "fps": fps,
        "screen_width": screen_width,
        "screen_height": screen_height,
        "bar_width": bar_width,
        "panel_height": panel_height,
        "panel_y": panel_y,
        "message_x": message_x,
        "message_width": message_width,
        "message_height": message_height,
        "map_width": map_width,
        "map_height": map_height,
        "room_max_size": room_max_size,
        "room_min_size": room_min_size,
        "max_rooms": max_rooms,
        "fov_algorithm": fov_algorithm,
        "fov_light_walls": fov_light_walls,
        "max_monsters_per_room": max_monsters_per_room,
        "max_items_per_room": max_items_per_room,
        "speed_action_divisor": speed_action_divisor
    }

    return constants


def get_game_variables(constants):
    fighter_component = Fighter(roll_character_attributes(),
                                current_hp=30,
                                base_armor_class=10,
                                base_armor=2,
                                base_cth_modifier=3,
                                base_speed=100,
                                base_attack_energy_bonus=0,
                                base_movement_energy_bonus=0,
                                base_natural_hp_regeneration_speed=50,
                                base_damage_dice={
                                    "physical": [[1, 6]],
                                    "fire": [],
                                    "ice": [],
                                    "lightning": [],
                                    "holy": [],
                                    "chaos": [],
                                    "arcane": [],
                                    "poison": [],
                                })
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(0,
                    0,
                    0x1004,
                    "Player",
                    blocks=True,
                    render_order=RenderOrder.ACTOR,
                    fighter=fighter_component,
                    inventory=inventory_component,
                    equipment=equipment_component,
                    level=level_component)
    entities = [player]

    for _i in range(25):
        armor = generate_random_armor()
        player.inventory.add_item(armor)

    player.fighter.actions = 1

    message_log = MessageLog(constants["message_x"],
                             constants["message_width"],
                             constants["message_height"])

    game_map: GameMap = GameMap(width=constants["map_width"],
                                height=constants["map_height"])
    game_map.make_map(constants["max_rooms"], constants["room_min_size"],
                      constants["room_max_size"], constants["map_width"],
                      constants["map_height"], player, entities)

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state