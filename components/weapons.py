import tcod as libtcod
from components.equippable import Equippable
from equipment_slots import EquipmentSlots
from entity import Entity

material_names = [
    "copper", "bronze", "iron", "steel", "truesteel", "orichalcum", "mithril",
    "voidstone", "brimstone", "cold iron", "thunderstone", "pearlstone",
    "electrum", "adamantine", "meteoric iron"
]


class Weapon:
    def __init__(
            self,
            rarity=None,
            material=None,
            weapon_type=None,
            weapon_name=None,
            unidentified_name=None,
            identified_name=None,
            prefix=None,
            suffix=None,
            quality=None,
            two_handed=False,
            bonus_attribute=None,
    ):
        self.rarity = rarity
        self.material = material
        self.weapon_type = weapon_type
        self.weapon_name = weapon_name
        self.unidentified_name = unidentified_name
        self.identified_name = identified_name
        self.prefix = prefix
        self.suffix = suffix
        self.quality = quality
        self.two_handed = two_handed
        self.bonus_attribute = bonus_attribute


def generate_starter_weapon():
    rarity = {
        "rarity_level": "normal",
        "rarity_color": libtcod.white,
        "rarity_color_name": "white"
    }

    material = "iron"

    weapon_type = "sword"

    weapon_name = "short sword"

    unidentified_name = f"{material.title()} {weapon_name.title()}"

    quality = "normal"

    starter_weapon = Weapon(rarity,
                            material,
                            weapon_type,
                            weapon_name,
                            unidentified_name,
                            unidentified_name,
                            bonus_attribute="Strength",
                            two_handed=False)

    equippable_component = Equippable(starter_weapon,
                                      EquipmentSlots.MAIN_HAND,
                                      damage_dice={
                                          "physical": [[1, 6]],
                                          "fire": [],
                                          "ice": [],
                                          "lightning": [],
                                          "holy": [],
                                          "chaos": [],
                                          "arcane": [],
                                          "poison": [],
                                      })
    new_entity = Entity(0,
                        0,
                        "(",
                        starter_weapon.rarity["rarity_color"],
                        starter_weapon.unidentified_name,
                        equippable=equippable_component)

    return new_entity
