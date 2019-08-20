from components.inventory import Inventory
from components.item import Item
from item_functions import cast_fireball, cast_chaos_bolt, cast_confuse, ranged_attack
from components.fighter import Fighter
from components.equipment import Equipment
from components.ammunition import Ammunition
from equipment_slots import EquipmentSlots
from components.equippable import Equippable
from components.level import Level
from components.attributes import roll_character_attributes
from components.armors import generate_random_armor
from components.weapons import generate_random_weapon
from components.status_effects import DoubleDamageToOrcs
from entity import Entity
from render_order import RenderOrder
from game_messages import MessageLog, Message
from map_objects.game_map import GameMap
from random import randint
from game import GameStates


def get_constants():
    window_title: str = "Voidstone"
    fps = 60

    screen_width: int = 224
    screen_height: int = 59

    map_width: int = 80
    map_height: int = 60

    room_max_size: int = 10
    room_min_size: int = 4
    max_rooms: int = 70

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
    fighter_component = Fighter(
        roll_character_attributes(),
        current_hp=30,
        base_armor_class=5,
        base_dodge=5,
        base_armor=0,
        base_melee_cth_modifier=100,
        base_ranged_cth_modifier=0,
        base_speed=150,
        base_melee_attack_energy_bonus=0,
        base_ranged_attack_energy_bonus=50,
        base_movement_energy_bonus=0,
        base_natural_hp_regeneration_speed=50,
        base_melee_damage_dice={
            "physical": [[1, 6]],
            "fire": [],
            "ice": [],
            "lightning": [],
            "holy": [],
            "chaos": [],
            "arcane": [],
            "poison": [],
        },
        base_ranged_damage_dice={
            "physical": [[3, 6]],
            "fire": [],
            "ice": [],
            "lightning": [],
            "holy": [],
            "chaos": [],
            "arcane": [],
            "poison": [],
        },
    )
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

    for _i in range(2):
        armor = generate_random_armor()
        player.inventory.add_item(armor)

    player.fighter.actions = 1

    item_component = Item(
        use_function=cast_fireball,
        targeting=True,
        targeting_message=Message(
            'Left-click a target tile for the fireball, or right-click to cancel.',
            "light cyan"),
        damage={"fire": 25},
        radius=2)

    item = Entity(0,
                  0,
                  0x1007,
                  'Scroll of Fireball',
                  render_order=RenderOrder.ITEM,
                  item=item_component)

    player.inventory.add_item(item)

    item_component = Item(
        use_function=ranged_attack,
        targeting=True,
        quantity=10,
        targeting_message=Message(
            'Left-click to shoot your ranged weapon, or right-click to cancel.',
            "light cyan"),
    )

    ammo_component = Ammunition(rarity={
        "rarity": "normal",
        "rarity_color": "white"
    },
                                ammunition_name="arrow",
                                material="iron",
                                quality="normal")

    equippable_component = Equippable(
        equippable_type=ammo_component,
        slot=EquipmentSlots.RANGED_WEAPON_AMMUNITION)

    item = Entity(0,
                  0,
                  0x1000,
                  ammo_component.identified_name.title(),
                  render_order=RenderOrder.ITEM,
                  item=item_component,
                  equippable=equippable_component)

    player.inventory.add_item(item)

    player.fighter.apply_effect(DoubleDamageToOrcs)

    weapon = generate_random_weapon()

    player.inventory.add_item(weapon)

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