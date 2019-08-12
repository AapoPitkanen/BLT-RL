import tcod as libtcod
from components.equippable import Equippable
from components.equipment_attributes import qualities, quality_weights, rarities, weapon_material_names, weapon_material_weights
from equipment_slots import EquipmentSlots
from entity import Entity


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


melee_weapon_names = {
    "swords": {
        "names": [
            "short sword",
            "broadsword",
            "longsword",
            "bastard sword",
            "scimitar",
            "falchion",
            "gladius",
            "arming sword",
            "estoc",
            "sabre",
            "rapier",
            "fencing sword",
        ],
        "weights": []
    },
    "axes": {
        "names": [
            "hand axe",
            "axe",
            "double axe",
            "war axe",
            "military pick",
            "battleaxe",
            "broadaxe",
            "hatchet",
            "cleaver",
            "bearded axe",
        ],
        "weights": []
    },
    "daggers": {
        "names": [
            "knife",
            "dagger",
            "dirk",
            "kris",
            "rondel dagger",
            "hunting dagger",
            "blade",
            "stiletto",
        ],
        "weights": []
    },
    "maces": {
        "names": [],
        "weights": []
    },
    "hammers": {
        "names": ["light hammer", "hammer", "warhammer"],
        "weights": []
    },
    "polearms": {
        "names": [
            "halberd",
            "bardiche",
            "voulge",
            "poleaxe",
            "fauchard",
            "guisarme",
            "glaive",
            "partisan",
            "lochaber axe",
            "war scythe",
        ],
        "weights": []
    },
    "spears": {
        "names": [
            "shortspear",
            "spear",
            "longspear",
            "pike",
            "lance",
            "war spear",
            "spetum",
            "brandistock",
        ],
        "weights": []
    },
    "twohanded": {
        "names": [
            "greatsword",
            "greataxe",
            "claymore",
            "zweihänder",
            "flamberge",
            "warsword",
        ],
        "weights": []
    }
}

ranged_weapon_names = {
    "pistols": {
        "names": [],
        "weights": []
    },
    "rifles": {
        "names": [],
        "weights": []
    },
    "bows": {
        "names": [],
        "weights": []
    },
    "crossbows": {
        "names": [],
        "weights": []
    },
}


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
