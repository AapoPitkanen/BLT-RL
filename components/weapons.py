import tcod as libtcod
from components.equippable import Equippable
from components.equipment_attributes import qualities, quality_weights, rarities, weapon_metal_material_names, weapon_metal_material_weights, weapon_wood_material_names, weapon_wood_material_weights, weapon_prefixes, weapon_prefix_weights, weapon_suffixes, weapon_suffix_weights
from equipment_slots import EquipmentSlots
from entity import Entity
from random import random, randint, choices, sample


class Weapon:
    def __init__(self,
                 rarity=None,
                 material=None,
                 slot_type=None,
                 weapon_type=None,
                 weapon_name=None,
                 weapon_physical_damage_type=None,
                 weapon_physical_damage_status_chance=None,
                 unidentified_name=None,
                 identified_name=None,
                 prefix=None,
                 suffix=None,
                 quality=None,
                 two_handed=False,
                 ammunition=None):
        self.rarity = rarity
        self.material = material
        self.slot_type = slot_type
        self.weapon_type = weapon_type
        self.weapon_name = weapon_name
        self.weapon_physical_damage_type = weapon_physical_damage_type
        self.weapon_physical_damage_status_chance = weapon_physical_damage_status_chance
        self.unidentified_name = unidentified_name
        self.identified_name = identified_name
        self.prefix = prefix
        self.suffix = suffix
        self.quality = quality
        self.two_handed = two_handed
        self.ammunition = ammunition


def generate_weapon_rarity_modifiers():
    weapon_rarity_modifiers = {
        "common": [{
            "armor_modifier": randint(1, 1)
        }, {
            "armor_class_modifier": randint(1, 1)
        }, {
            "max_hp_modifier": randint(1, 3)
        }, {
            "melee_chance_to_hit_modifier": randint(1, 2)
        }, {
            "ranged_chance_to_hit_modifier": randint(1, 2)
        }, {
            "speed_modifier": randint(1, 3)
        }, {
            "movement_energy_bonus_modifier": randint(1, 2)
        }, {
            "melee_attack_energy_bonus_modifier": randint(1, 2)
        }],
        "uncommon": [{
            "armor_modifier": randint(1, 1)
        }, {
            "armor_class_modifier": randint(1, 2)
        }, {
            "max_hp_modifier": randint(1, 4)
        }, {
            "melee_chance_to_hit_modifier": randint(1, 3)
        }, {
            "ranged_chance_to_hit_modifier": randint(1, 3)
        }, {
            "speed_modifier": randint(1, 4)
        }, {
            "movement_energy_bonus_modifier": randint(1, 3)
        }, {
            "melee_attack_energy_bonus_modifier": randint(1, 3)
        }, {
            "resistances": {
                "physical": randint(1, 3) / 100
            }
        }],
        "rare": [{
            "armor_modifier": randint(1, 1)
        }, {
            "armor_class_modifier": randint(1, 3)
        }, {
            "max_hp_modifier": randint(1, 5)
        }, {
            "melee_chance_to_hit_modifier": randint(1, 4)
        }, {
            "ranged_chance_to_hit_modifier": randint(1, 4)
        }, {
            "critical_hit_chance_modifier": randint(1, 2) / 100
        }, {
            "critical_hit_damage_multiplier_modifier": 5 / 100
        }, {
            "speed_modifier": randint(1, 5)
        }, {
            "movement_energy_bonus_modifier": randint(1, 4)
        }, {
            "melee_attack_energy_bonus_modifier": randint(1, 4)
        }, {
            "resistances": {
                "physical": randint(1, 4) / 100
            }
        }, {
            "resistances": {
                "fire": randint(1, 4) / 100
            }
        }, {
            "resistances": {
                "ice": randint(1, 4) / 100
            }
        }, {
            "resistances": {
                "lightning": randint(1, 4) / 100
            }
        }],
        "epic": [{
            "armor_modifier": randint(1, 3)
        }, {
            "armor_class_modifier": randint(2, 4)
        }, {
            "max_hp_modifier": randint(2, 6)
        }, {
            "melee_chance_to_hit_modifier": randint(2, 5)
        }, {
            "ranged_chance_to_hit_modifier": randint(2, 5)
        }, {
            "critical_hit_chance_modifier": randint(1, 3) / 100
        }, {
            "critical_hit_damage_multiplier_modifier": 5 / 100
        }, {
            "speed_modifier": randint(1, 5)
        }, {
            "movement_energy_bonus_modifier": randint(2, 5)
        }, {
            "melee_attack_energy_bonus_modifier": randint(2, 5)
        }, {
            "resistances": {
                "physical": randint(1, 5) / 100
            }
        }, {
            "resistances": {
                "fire": randint(1, 5) / 100
            }
        }, {
            "resistances": {
                "ice": randint(1, 5) / 100
            }
        }, {
            "resistances": {
                "lightning": randint(1, 5) / 100
            }
        }, {
            "resistances": {
                "holy": randint(1, 5) / 100
            }
        }, {
            "resistances": {
                "chaos": randint(1, 5) / 100
            }
        }, {
            "resistances": {
                "arcane": randint(1, 5) / 100
            }
        }, {
            "resistances": {
                "poison": randint(1, 5) / 100
            }
        }],
        "mythical": [{
            "armor_modifier": randint(2, 4)
        }, {
            "armor_class_modifier": randint(3, 6)
        }, {
            "max_hp_modifier": randint(3, 8)
        }, {
            "melee_chance_to_hit_modifier": randint(3, 6)
        }, {
            "ranged_chance_to_hit_modifier": randint(3, 6)
        }, {
            "critical_hit_chance_modifier": randint(2, 4) / 100
        }, {
            "critical_hit_damage_multiplier_modifier": 10 / 100
        }, {
            "speed_modifier": randint(2, 6)
        }, {
            "movement_energy_bonus_modifier": randint(2, 6)
        }, {
            "melee_attack_energy_bonus_modifier": randint(2, 6)
        }, {
            "life_steal_modifier": randint(3, 8) / 100
        }, {
            "damage_reflection_modifier": randint(3, 8) / 100
        }, {
            "strength_modifier": 1
        }, {
            "perception_modifier": 1
        }, {
            "dexterity_modifier": 1
        }, {
            "constitution_modifier": 1
        }, {
            "intelligence_modifier": 1
        }, {
            "wisdom_modifier": 1
        }, {
            "charisma_modifier": 1
        }, {
            "luck_modifier": 1
        }, {
            "resistances": {
                "physical": randint(1, 6) / 100
            }
        }, {
            "resistances": {
                "fire": randint(1, 6) / 100
            }
        }, {
            "resistances": {
                "ice": randint(1, 6) / 100
            }
        }, {
            "resistances": {
                "lightning": randint(1, 6) / 100
            }
        }, {
            "resistances": {
                "holy": randint(1, 6) / 100
            }
        }, {
            "resistances": {
                "chaos": randint(1, 6) / 100
            }
        }, {
            "resistances": {
                "arcane": randint(1, 6) / 100
            }
        }, {
            "resistances": {
                "poison": randint(1, 6) / 100
            }
        }, {
            "dodge_modifier": randint(1, 2)
        }]
    }
    return weapon_rarity_modifiers


def generate_melee_quality_modifiers():
    melee_quality_modifiers = {
        "abysmal": {
            "melee_chance_to_hit_modifier": randint(-4, -1),
            "melee_damage_modifiers": {
                "physical": randint(-4, -1)
            }
        },
        "awful": {
            "melee_chance_to_hit_modifier": randint(-4, 0),
            "melee_damage_modifiers": {
                "physical": randint(-3, -1)
            }
        },
        "bad": {
            "melee_chance_to_hit_modifier": randint(-3, 0),
            "melee_damage_modifiers": {
                "physical": randint(-2, -1)
            }
        },
        "poor": {
            "melee_chance_to_hit_modifier": randint(-2, 0),
            "melee_damage_modifiers": {
                "physical": randint(-2, 0)
            }
        },
        "fair": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": randint(-1, 0)
            }
        },
        "normal": {
            "melee_chance_to_hit_modifier": randint(0, 1),
        },
        "fine": {
            "melee_chance_to_hit_modifier": randint(0, 1),
            "melee_damage_modifiers": {
                "physical": randint(0, 1)
            }
        },
        "good": {
            "melee_chance_to_hit_modifier": randint(0, 2),
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "superior": {
            "melee_chance_to_hit_modifier": randint(1, 2),
            "melee_damage_modifiers": {
                "physical": randint(1, 2)
            }
        },
        "excellent": {
            "melee_chance_to_hit_modifier": 2,
            "melee_damage_modifiers": {
                "physical": randint(1, 2)
            }
        },
        "exceptional": {
            "melee_chance_to_hit_modifier": randint(2, 3),
            "melee_damage_modifiers": {
                "physical": randint(1, 2)
            }
        },
        "exquisite": {
            "melee_chance_to_hit_modifier": randint(2, 3),
            "melee_attack_energy_bonus_modifier": randint(1, 2),
            "melee_damage_modifiers": {
                "physical": randint(1, 2)
            },
        },
        "flawless": {
            "melee_chance_to_hit_modifier": randint(2, 4),
            "melee_attack_energy_bonus_modifier": randint(1, 3),
            "critical_hit_chance_modifier": randint(1, 2) / 100,
            "melee_damage_modifiers": {
                "physical": randint(1, 3)
            }
        }
    }
    return melee_quality_modifiers


def generate_ranged_quality_modifiers():
    ranged_quality_modifiers = {
        "abysmal": {
            "ranged_chance_to_hit_modifier": randint(-4, -1),
            "ranged_damage_modifiers": {
                "physical": randint(-4, -1)
            }
        },
        "awful": {
            "ranged_chance_to_hit_modifier": randint(-4, 0),
            "ranged_damage_modifiers": {
                "physical": randint(-3, -1)
            }
        },
        "bad": {
            "ranged_chance_to_hit_modifier": randint(-3, 0),
            "ranged_damage_modifiers": {
                "physical": randint(-2, -1)
            }
        },
        "poor": {
            "ranged_chance_to_hit_modifier": randint(-2, 0),
            "ranged_damage_modifiers": {
                "physical": randint(-2, 0)
            }
        },
        "fair": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(-1, 0)
            }
        },
        "normal": {
            "ranged_chance_to_hit_modifier": randint(0, 1),
        },
        "fine": {
            "ranged_chance_to_hit_modifier": randint(0, 1),
            "ranged_damage_modifiers": {
                "physical": randint(0, 1)
            }
        },
        "good": {
            "ranged_chance_to_hit_modifier": randint(0, 2),
            "ranged_damage_modifiers": {
                "physical": 1
            }
        },
        "superior": {
            "ranged_chance_to_hit_modifier": randint(1, 2),
            "ranged_damage_modifiers": {
                "physical": randint(1, 2)
            }
        },
        "excellent": {
            "ranged_chance_to_hit_modifier": 2,
            "ranged_damage_modifiers": {
                "physical": randint(1, 2)
            }
        },
        "exceptional": {
            "ranged_chance_to_hit_modifier": randint(2, 3),
            "ranged_damage_modifiers": {
                "physical": randint(1, 2)
            }
        },
        "exquisite": {
            "ranged_chance_to_hit_modifier": randint(2, 3),
            "melee_attack_energy_bonus_modifier": randint(1, 2),
            "ranged_damage_modifiers": {
                "physical": randint(1, 2)
            },
        },
        "flawless": {
            "ranged_chance_to_hit_modifier": randint(2, 4),
            "melee_attack_energy_bonus_modifier": randint(1, 3),
            "critical_hit_chance_modifier": randint(1, 2) / 100,
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        }
    }
    return ranged_quality_modifiers


def generate_melee_weapon_material_modifiers():
    melee_weapon_material_modifiers = {
        "copper": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "bronze": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "iron": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "steel": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "truesteel": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "darksteel": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "orichalcum": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "mithril": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "voidstone": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "brimstone": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "cold iron": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "thunderstone": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "pearlstone": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "electrum": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "adamantine": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
        "meteoric iron": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": 0,
            }
        },
    }
    return melee_weapon_material_modifiers


def generate_pistol_and_rifle_material_modifiers():
    pistol_and_rifle_material_modifiers = {
        "copper": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "bronze": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "iron": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "steel": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "truesteel": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "darksteel": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "orichalcum": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "mithril": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "voidstone": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "brimstone": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "cold iron": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "thunderstone": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "pearlstone": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "electrum": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "adamantine": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "meteoric iron": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
    }
    return pistol_and_rifle_material_modifiers


def generate_bow_and_crossbow_material_modifiers():
    bow_and_crossbow_material_modifiers = {
        "maple": {
            "ranged_chance_to_hit_modifier": randint(-1, 1)
        },
        "ash": {
            "ranged_chance_to_hit_modifier": randint(-1, 1)
        },
        "elm": {
            "ranged_chance_to_hit_modifier": randint(-1, 1)
        },
        "oak": {
            "ranged_chance_to_hit_modifier": randint(-1, 1)
        },
        "hickory": {
            "ranged_chance_to_hit_modifier": randint(-1, 1)
        },
        "walnut": {
            "ranged_chance_to_hit_modifier": randint(-1, 1)
        },
        "ironwood": {
            "ranged_chance_to_hit_modifier": randint(-1, 1)
        },
        "rosewood": {
            "ranged_chance_to_hit_modifier": randint(-1, 1)
        },
        "juniper": {
            "ranged_chance_to_hit_modifier": randint(-1, 1)
        },
        "yew": {
            "ranged_chance_to_hit_modifier": randint(-1, 1)
        },
    }
    return bow_and_crossbow_material_modifiers


weapon_types = {
    "types": [
        "sword",
        "axe",
        "dagger",
        "mace",
        "hammer",
        "polearm",
        "spear",
        "twohanded",
        "pistol",
        "rifle",
        "bow",
        "crossbow",
    ],
    "weights": [
        0.10,
        0.10,
        0.10,
        0.10,
        0.10,
        0.10,
        0.10,
        0.05,
        0.04,
        0.03,
        0.10,
        0.08,
    ]
}

weapon_names = {
    "sword": {
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
        "weights": [
            0.18,
            0.15,
            0.125,
            0.075,
            0.06,
            0.06,
            0.05,
            0.1,
            0.05,
            0.05,
            0.05,
            0.05,
        ],
    },
    "axe": {
        "names": [
            "hand axe",
            "axe",
            "double axe",
            "war axe",
            "military pick",
            "war pick",
            "battleaxe",
            "broadaxe",
            "hatchet",
            "cleaver",
            "bearded axe",
        ],
        "weights": [
            0.18,
            0.15,
            0.125,
            0.075,
            0.07,
            0.07,
            0.06,
            0.1,
            0.06,
            0.06,
            0.05,
        ]
    },
    "dagger": {
        "names": [
            "knife",
            "long knife",
            "dagger",
            "dirk",
            "kris",
            "rondel dagger",
            "hunting dagger",
            "blade",
            "stiletto",
        ],
        "weights": [
            0.19,
            0.17,
            0.125,
            0.075,
            0.08,
            0.08,
            0.1,
            0.1,
            0.08,
        ]
    },
    "mace": {
        "names": [
            "light mace",
            "mace",
            "ball mace",
            "heavy mace",
            "morning star",
            "light flail",
            "flail",
            "flanged mace",
            "bladed mace",
            "mallet",
        ],
        "weights": [
            0.15,
            0.12,
            0.125,
            0.075,
            0.08,
            0.08,
            0.1,
            0.1,
            0.08,
            0.07,
        ]
    },
    "hammer": {
        "names": [
            "club",
            "cudgel",
            "bludgeon",
            "truncheon",
            "war club",
            "heavy cudgel",
            "light hammer",
            "hammer",
            "war hammer",
            "battle hammer",
            "large hammer",
        ],
        "weights": [
            0.18,
            0.15,
            0.125,
            0.075,
            0.07,
            0.07,
            0.06,
            0.1,
            0.06,
            0.06,
            0.05,
        ]
    },
    "polearm": {
        "names": [
            "short staff",
            "staff",
            "long staff",
            "quarterstaff",
            "battle staff",
            "war staff",
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
        "weights": [
            0.10,
            0.09,
            0.08,
            0.07,
            0.06,
            0.05,
            0.10,
            0.09,
            0.08,
            0.07,
            0.06,
            0.05,
            0.04,
            0.03,
            0.02,
            0.01,
        ]
    },
    "spear": {
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
        "weights": [
            0.20,
            0.18,
            0.15,
            0.13,
            0.10,
            0.09,
            0.08,
            0.06,
        ]
    },
    "twohanded": {
        "names": [
            "greatsword",
            "greataxe",
            "claymore",
            "zweihänder",
            "flamberge",
            "warsword",
            "maul",
            "heavy maul",
            "two-handed hammer",
            "two-handed war hammer",
            "heavy flail",
        ],
        "weights": [
            0.15,
            0.15,
            0.10,
            0.08,
            0.06,
            0.06,
            0.08,
            0.08,
            0.08,
            0.08,
            0.08,
        ]
    },
    "pistol": {
        "names": [
            "flintlock pistol",
            "revolver",
            "repeater",
            "howdah",
            "hand cannon",
            "derringer",
        ],
        "weights": [
            0.25,
            0.2,
            0.175,
            0.15,
            0.125,
            0.1,
        ]
    },
    "rifle": {
        "names": [
            "flintlock rifle",
            "musket",
            "rifle",
            "repeater carbine",
            "blunderbuss",
            "bolt-action rifle",
            "repeating rifle",
            "carbine",
            "assault carbine",
            "revolver rifle",
        ],
        "weights": [
            0.150,
            0.140,
            0.130,
            0.120,
            0.110,
            0.090,
            0.080,
            0.070,
            0.060,
            0.050,
        ]
    },
    "bow": {
        "names": [
            "shortbow",
            "bow",
            "hunting bow",
            "composite bow",
            "longbow",
            "recurve bow",
            "war bow",
            "siege bow",
        ],
        "weights": [
            0.2,
            0.18,
            0.16,
            0.14,
            0.12,
            0.1,
            0.05,
            0.05,
        ]
    },
    "crossbow": {
        "names": [
            "light crossbow",
            "crossbow",
            "heavy crossbow",
            "repeating crossbow",
            "arbalest",
            "heavy arbalest",
            "siege crossbow",
            "hand ballista",
        ],
        "weights": [
            0.2,
            0.18,
            0.16,
            0.14,
            0.12,
            0.1,
            0.05,
            0.05,
        ]
    },
}

weapon_physical_damage_types = {
    "short sword": "slashing",
    "broadsword": "slashing",
    "longsword": "slashing",
    "bastard sword": "slashing",
    "scimitar": "slashing",
    "falchion": "slashing",
    "gladius": "slashing",
    "arming sword": "slashing",
    "sabre": "slashing",
    "estoc": "piercing",
    "rapier": "piercing",
    "fencing sword": "piercing",
    "hand axe": "slashing",
    "axe": "slashing",
    "double axe": "slashing",
    "war axe": "piercing",
    "military pick": "piercing",
    "war pick": "piercing",
    "battleaxe": "slashing",
    "broadaxe": "slashing",
    "hatchet": "slashing",
    "cleaver": "slashing",
    "bearded axe": "slashing",
    "knife": "slashing",
    "dagger": "piercing",
    "dirk": "piercing",
    "kris": "piercing",
    "rondel dagger": "slashing",
    "hunting dagger": "slashing",
    "blade": "slashing",
    "stiletto": "piercing",
    "light mace": "bludgeoning",
    "mace": "bludgeoning",
    "ball mace": "bludgeoning",
    "heavy mace": "bludgeoning",
    "morning star": "piercing",
    "light flail": "bludgeoning",
    "flail": "bludgeoning",
    "flanged mace": "bludgeoning",
    "bladed mace": "slashing",
    "mallet": "bludgeoning",
    "club": "bludgeoning",
    "cudgel": "bludgeoning",
    "bludgeon": "bludgeoning",
    "truncheon": "bludgeoning",
    "war club": "bludgeoning",
    "heavy cudgel": "bludgeoning",
    "light hammer": "bludgeoning",
    "hammer": "bludgeoning",
    "war hammer": "bludgeoning",
    "battle hammer": "bludgeoning",
    "large hammer": "bludgeoning",
    "short staff": "bludgeoning",
    "staff": "bludgeoning",
    "long staff": "bludgeoning",
    "quarterstaff": "bludgeoning",
    "battle staff": "bludgeoning",
    "war staff": "bludgeoning",
    "halberd": "slashing",
    "bardiche": "slashing",
    "voulge": "slashing",
    "poleaxe": "slashing",
    "fauchard": "slashing",
    "guisarme": "piercing",
    "glaive": "slashing",
    "partisan": "slashing",
    "lochaber axe": "slashing",
    "war scythe": "slashing",
    "shortspear": "piercing",
    "spear": "piercing",
    "longspear": "piercing",
    "pike": "piercing",
    "lance": "piercing",
    "war spear": "piercing",
    "spetum": "piercing",
    "brandistock": "piercing",
    "greatsword": "slashing",
    "greataxe": "slashing",
    "claymore": "slashing",
    "zweihänder": "slashing",
    "flamberge": "slashing",
    "warsword": "slashing",
    "maul": "bludgeoning",
    "heavy maul": "bludgeoning",
    "two-handed hammer": "bludgeoning",
    "two-handed war hammer": "bludgeoning",
    "heavy flail": "bludgeoning",
    "revolver": "piercing",
    "repeater": "piercing",
    "flintlock pistol": "piercing",
    "howdah": "piercing",
    "hand cannon": "piercing",
    "derringer": "piercing",
    "rifle": "piercing",
    "repeater carbine": "piercing",
    "flintlock rifle": "piercing",
    "musket": "piercing",
    "blunderbuss": "piercing",
    "bolt-action rifle": "piercing",
    "repeating rifle": "piercing",
    "carbine": "piercing",
    "assault carbine": "piercing",
    "revolver rifle": "piercing",
    "shortbow": "piercing",
    "bow": "piercing",
    "hunting bow": "piercing",
    "composite bow": "piercing",
    "longbow": "piercing",
    "recurve bow": "piercing",
    "war bow": "piercing",
    "siege bow": "piercing",
    "light crossbow": "piercing",
    "crossbow": "piercing",
    "heavy crossbow": "piercing",
    "repeating crossbow": "piercing",
    "arbalest": "piercing",
    "heavy arbalest": "piercing",
    "siege crossbow": "piercing",
    "hand ballista": "piercing",
}

weapon_physical_damage_status_chances = {
    "short sword": 0.05,
    "broadsword": 0.06,
    "longsword": 0.07,
    "bastard sword": 0.08,
    "scimitar": 0.08,
    "falchion": 0.08,
    "gladius": 0.08,
    "arming sword": 0.09,
    "sabre": 0.1,
    "estoc": 0.8,
    "rapier": 0.9,
    "fencing sword": 0.1,
    "hand axe": 0.05,
    "axe": 0.06,
    "double axe": 0.07,
    "war axe": 0.08,
    "military pick": 0.9,
    "war pick": 0.1,
    "battleaxe": 0.1,
    "broadaxe": 0.09,
    "hatchet": 0.08,
    "cleaver": 0.13,
    "bearded axe": 0.15,
    "knife": 0.05,
    "dagger": 0.06,
    "dirk": 0.07,
    "kris": 0.1,
    "rondel dagger": 0.11,
    "hunting dagger": 0.08,
    "blade": 0.1,
    "stiletto": 0.1,
    "light mace": 0.03,
    "mace": 0.04,
    "ball mace": 0.05,
    "heavy mace": 0.06,
    "morning star": 0.07,
    "light flail": 0.08,
    "flail": 0.09,
    "flanged mace": 0.1,
    "bladed mace": 0.11,
    "mallet": 0.05,
    "club": 0.06,
    "cudgel": 0.07,
    "bludgeon": 0.08,
    "truncheon": 0.09,
    "war club": 0.1,
    "heavy cudgel": 0.08,
    "light hammer": 0.1,
    "hammer": 0.11,
    "war hammer": 0.12,
    "battle hammer": 0.13,
    "large hammer": 0.14,
    "short staff": 0.03,
    "staff": 0.04,
    "long staff": 0.05,
    "quarterstaff": 0.06,
    "battle staff": 0.07,
    "war staff": 0.08,
    "halberd": 0.05,
    "bardiche": 0.06,
    "voulge": 0.07,
    "poleaxe": 0.08,
    "fauchard": 0.09,
    "guisarme": 0.1,
    "glaive": 0.11,
    "partisan": 0.12,
    "lochaber axe": 0.13,
    "war scythe": 0.18,
    "shortspear": 0.08,
    "spear": 0.09,
    "longspear": 0.1,
    "pike": 0.11,
    "lance": 0.12,
    "war spear": 0.13,
    "spetum": 0.14,
    "brandistock": 0.15,
    "greatsword": 0.15,
    "greataxe": 0.15,
    "claymore": 0.18,
    "zweihänder": 0.2,
    "flamberge": 0.2,
    "warsword": 0.22,
    "maul": 0.15,
    "heavy maul": 0.16,
    "two-handed hammer": 0.17,
    "two-handed war hammer": 0.18,
    "heavy flail": 0.19,
    "revolver": 0.1,
    "repeater pistol": 0.11,
    "flintlock pistol": 0.12,
    "howdah": 0.13,
    "hand cannon": 0.14,
    "derringer": 0.1,
    "rifle": 0.09,
    "repeater carbine": 0.1,
    "flintlock rifle": 0.11,
    "musket": 0.12,
    "blunderbuss": 0.13,
    "bolt-action rifle": 0.14,
    "repeating rifle": 0.15,
    "carbine": 0.16,
    "assault carbine": 0.17,
    "revolver rifle": 0.18,
    "shortbow": 0.05,
    "bow": 0.06,
    "hunting bow": 0.07,
    "composite bow": 0.08,
    "longbow": 0.09,
    "recurve bow": 0.1,
    "war bow": 0.11,
    "siege bow": 0.12,
    "light crossbow": 0.1,
    "crossbow": 0.11,
    "heavy crossbow": 0.12,
    "repeating crossbow": 0.13,
    "arbalest": 0.14,
    "heavy arbalest": 0.15,
    "siege crossbow": 0.16,
    "hand ballista": 0.17,
}

def generate_weapon_name_modifiers():

    weapon_name_modifiers = {
        "short sword": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "broadsword": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "longsword": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "bastard sword": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "scimitar": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "falchion": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "gladius": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "arming sword": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "sabre": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "estoc": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "rapier": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "fencing sword": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "hand axe": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "axe": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "double axe": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "war axe": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "military pick": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "war pick": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "battleaxe": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "broadaxe": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "hatchet": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "cleaver": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "bearded axe": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "knife": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "dagger": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "dirk": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "kris": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "rondel dagger": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "hunting dagger": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "blade": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "stiletto": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "light mace": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "mace": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "ball mace": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "heavy mace": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "morning star": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "light flail": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "flail": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "flanged mace": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "bladed mace": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "mallet": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "club": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "cudgel": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "bludgeon": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "truncheon": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "war club": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "heavy cudgel": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "light hammer": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "hammer": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "war hammer": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "battle hammer": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "large hammer": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "short staff": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "staff": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "long staff": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "quarterstaff": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "battle staff": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "war staff": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "halberd": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "bardiche": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "voulge": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "poleaxe": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "fauchard": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "guisarme": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "glaive": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "partisan": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "lochaber axe": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "war scythe": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "shortspear": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "spear": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "longspear": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "pike": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "lance": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "war spear": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "spetum": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "brandistock": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "greatsword": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "greataxe": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "claymore": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "zweihänder": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "flamberge": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "warsword": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "maul": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "heavy maul": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "two-handed hammer": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "two-handed war hammer": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "heavy flail": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "revolver": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "repeater": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "flintlock pistol": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "howdah": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "hand cannon": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "derringer": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "rifle": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "repeater carbine": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "flintlock rifle": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "musket": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "blunderbuss": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "bolt-action rifle": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "repeating rifle": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "carbine": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "assault carbine": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "revolver rifle": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "shortbow": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "bow": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "hunting bow": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "composite bow": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "longbow": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "recurve bow": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "war bow": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "siege bow": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "light crossbow": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "crossbow": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "heavy crossbow": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "repeating crossbow": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "arbalest": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "heavy arbalest": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "siege crossbow": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
        "hand ballista": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            }
        },
    }
    return weapon_name_modifiers

def generate_melee_weapon_prefix_modifiers():
    melee_weapon_prefix_modifiers = {
        "Deadly": {},
        "Blazing": {},
        "Searing": {},
        "Freezing": {},
        "Chilled": {},
        "Frostborn": {},
        "Fireborn": {},
        "Shocking": {},
        "Charged": {},
        "Thunderstruck": {},
        "Sanctified": {},
        "Abyssal": {},
        "Esoteric": {},
        "Venomous": {},
        "Relentless": {},
        "Murderous": {},
        "Masterwork": {},
        "Swift": {},
        "Quick": {},
        "Vampiric": {},
        "Dastardly": {},
        "Brutal": {},
        "Barbaric": {},
        "Bloodthirsty": {},
        "Demonic": {},
        "Infernal": {},
        "Enchanted": {},
        "Eldritch": {},
        "Wretched": {},
        "Sinister": {},
        "Stoneforged": {},
        "Skyforged": {},
    }
    return melee_weapon_prefix_modifiers


def generate_ranged_weapon_prefix_modifiers():
    ranged_weapon_prefix_modifiers = {
        "Deadly": {},
        "Blazing": {},
        "Searing": {},
        "Freezing": {},
        "Chilled": {},
        "Frostborn": {},
        "Fireborn": {},
        "Shocking": {},
        "Charged": {},
        "Thunderstruck": {},
        "Sanctified": {},
        "Abyssal": {},
        "Esoteric": {},
        "Venomous": {},
        "Relentless": {},
        "Murderous": {},
        "Masterwork": {},
        "Swift": {},
        "Quick": {},
        "Vampiric": {},
        "Dastardly": {},
        "Brutal": {},
        "Barbaric": {},
        "Bloodthirsty": {},
        "Demonic": {},
        "Infernal": {},
        "Enchanted": {},
        "Eldritch": {},
        "Wretched": {},
        "Sinister": {},
        "Stoneforged": {},
        "Skyforged": {},
    }
    return ranged_weapon_prefix_modifiers


def generate_melee_weapon_suffix_modifiers():
    melee_weapon_suffix_modifiers = {
        "of Alacrity": {},
        "of Celerity": {},
        "of Defense": {},
        "of Protection": {},
        "of Strength": {},
        "of the Juggernaut": {},
        "of the Hawk": {},
        "of the Eagle": {},
        "of the Cat": {},
        "of the Fox": {},
        "of Endurance": {},
        "of Toughness": {},
        "of the Magi": {},
        "of the Wizard": {},
        "of Wisdom": {},
        "of Piety": {},
        "of Charisma": {},
        "of the Silver Tongue": {},
        "of Fate": {},
        "of Fortune": {},
        "of Longevity": {},
        "of Health": {},
        "of Life": {},
        "of Flames": {},
        "of the Glacier": {},
        "of Thunder": {},
        "of the Heavens": {},
        "of the Void": {},
        "of the Arcane": {},
        "of Toxins": {},
        "of Evasion": {},
        "of Ruin": {},
        "of Scorching": {},
        "of Frostbite": {},
        "of Thunder": {},
        "of Decay": {},
        "of Death": {},
        "of Conflagaration": {},
        "of Insanity": {},
        "of Sanctification": {},
        "of the Slayer": {},
        "of the Excecutioner": {},
        "of Fervor": {},
        "of Voracity": {},
        "of Cruelty": {},
        "of Ruthlessness": {},
        "of Fury": {},
        "of Slaughter": {},
        "of Ferocity": {},
        "of Onslaught": {},
        "of Wildfire": {},
        "of Blight": {},
        "of Destruction": {},
        "of Devastation": {
            "melee_damage_dice_modifiers": {
                "physical": [[4, 0]]
            }
        },
        "of Decimation": {},
        "of Annihilation": {},
        "of Disintegration": {},
        "of Obliteration": {
        },
        "of the Elements": {},
        "of the Flamecaller": {},
        "of Shattering": {},
        "of Torment": {},
        "of Celestial Wrath": {},
        "of Mortality": {},
    }
    return melee_weapon_suffix_modifiers


def generate_ranged_weapon_suffix_modifiers():
    ranged_weapon_suffix_modifiers = {
        "of Alacrity": {},
        "of Celerity": {},
        "of Defense": {},
        "of Protection": {},
        "of Strength": {},
        "of the Juggernaut": {},
        "of the Hawk": {},
        "of the Eagle": {},
        "of the Cat": {},
        "of the Fox": {},
        "of Endurance": {},
        "of Toughness": {},
        "of the Magi": {},
        "of the Wizard": {},
        "of Wisdom": {},
        "of Piety": {},
        "of Charisma": {},
        "of the Silver Tongue": {},
        "of Fate": {},
        "of Fortune": {},
        "of Longevity": {},
        "of Health": {},
        "of Life": {},
        "of Flames": {},
        "of the Glacier": {},
        "of Thunder": {},
        "of the Heavens": {},
        "of the Void": {},
        "of the Arcane": {},
        "of Toxins": {},
        "of Evasion": {},
        "of Ruin": {},
        "of Scorching": {},
        "of Frostbite": {},
        "of Thunder": {},
        "of Decay": {},
        "of Death": {},
        "of Conflagaration": {},
        "of Insanity": {},
        "of Sanctification": {},
        "of the Slayer": {},
        "of the Excecutioner": {},
        "of Fervor": {},
        "of Voracity": {},
        "of Cruelty": {},
        "of Ruthlessness": {},
        "of Fury": {},
        "of Slaughter": {},
        "of Ferocity": {},
        "of Onslaught": {},
        "of Wildfire": {},
        "of Blight": {},
        "of Destruction": {},
        "of Devastation": {},
        "of Decimation": {},
        "of Annihilation": {},
        "of Disintegration": {},
        "of Obliteration": {},
        "of the Elements": {},
        "of the Flamecaller": {},
        "of Shattering": {},
        "of Torment": {},
        "of Celestial Wrath": {},
        "of Mortality": {},
    }
    return ranged_weapon_suffix_modifiers


def generate_random_weapon():
    rarity_level = ''.join(
        choices(rarities["rarity_levels"], rarities["rarity_weights"], k=1))
    quality = ''.join(choices(qualities, quality_weights, k=1))

    prefix = None
    prefix_seed = random()
    suffix = None
    suffix_seed = random()

    if prefix_seed <= 0.25:
        prefix = ''.join(choices(weapon_prefixes, weapon_prefix_weights, k=1))

    if suffix_seed <= 0.25:
        suffix = ''.join(choices(weapon_suffixes, weapon_suffix_weights, k=1))

    suffix = "of Devastation"

    rarity = {
        "rarity_level": rarity_level,
        "rarity_color": rarities["rarity_colors"][rarity_level]
    }

    weapon_type = "".join(
        choices(weapon_types["types"], weapon_types["weights"]))

    weapon_type = "bow"

    if weapon_type in ["pistol", "rifle", "bow", "crossbow"]:
        slot = EquipmentSlots.RANGED_WEAPON
        weapon_quality_modifiers = generate_ranged_quality_modifiers()[quality]
        if prefix:
            prefix_modifiers = generate_ranged_weapon_prefix_modifiers()[prefix]
        if suffix:
            suffix_modifiers = generate_ranged_weapon_suffix_modifiers()[suffix]
    else:
        slot = EquipmentSlots.MAIN_HAND
        weapon_quality_modifiers = generate_melee_quality_modifiers()[quality]
        if prefix:
            prefix_modifiers = generate_melee_weapon_prefix_modifiers()[prefix]
        if suffix:
            suffix_modifiers = generate_melee_weapon_suffix_modifiers()[suffix]

    weapon_name = "".join(
        choices(weapon_names[weapon_type]["names"],
                weapon_names[weapon_type]["weights"]))

    if weapon_type in ["bow", "crossbow"]:
        material = "".join(
            choices(weapon_wood_material_names, weapon_wood_material_weights))
    else:
        material = "".join(
            choices(weapon_metal_material_names,
                    weapon_metal_material_weights))

    if weapon_type in ["bow", "crossbow"]:
        material_modifiers = generate_bow_and_crossbow_material_modifiers(
        )[material]
    elif weapon_type in ["pistol", "rifle"]:
        material_modifiers = generate_pistol_and_rifle_material_modifiers(
        )[material]
    else:
        material_modifiers = generate_melee_weapon_material_modifiers(
        )[material]

    if weapon_type == "bow":
        ammunition = "arrow"
    elif weapon_type == "crossbow":
        ammunition = "bolt"
    elif weapon_type in ["pistol", "rifle"]:
        ammunition = "bullet"
    else:
        ammunition = None

    two_handed = True if weapon_type == "twohanded" else False

    weapon_name_modifiers = generate_weapon_name_modifiers()[weapon_name]

    weapon_physical_damage_type = weapon_physical_damage_types[weapon_name]
    weapon_physical_damage_status_chance = weapon_physical_damage_status_chances[
        weapon_name]

    total_modifiers = [
        material_modifiers, weapon_name_modifiers, weapon_quality_modifiers
    ]

    if prefix:
        total_modifiers.append(prefix_modifiers)

    if suffix:
        total_modifiers.append(suffix_modifiers)

    if rarity_level != "normal":
        possible_rarity_modifiers = generate_weapon_rarity_modifiers(
        )[rarity_level]
        modifier_count = rarities["rarity_modifier_counts"][rarity_level]
        rarity_modifier_sample = sample(possible_rarity_modifiers,
                                        modifier_count)
        rarity_modifiers = {}
        for modifier in rarity_modifier_sample:
            for modifier_name in modifier.keys():
                rarity_modifiers.update(
                    {modifier_name: modifier[modifier_name]})
        total_modifiers.append(rarity_modifiers)

    unidentified_name = f"{material.title()} {weapon_name.title()}"
    identified_name = f"{rarity_level.title() + ' ' if rarity_level != 'normal' else ''}{prefix + ' ' if prefix else ''}{material.title()} {weapon_name.title()}{' ' + suffix if suffix else ''}{' (' + quality + ')' if quality != 'normal' else ''}"

    random_weapon = Weapon(
        rarity=rarity,
        material=material,
        slot_type=slot,
        weapon_type=weapon_type,
        weapon_name=weapon_name,
        weapon_physical_damage_type=weapon_physical_damage_type,
        weapon_physical_damage_status_chance=
        weapon_physical_damage_status_chance,
        unidentified_name=unidentified_name,
        identified_name=identified_name,
        prefix=prefix,
        suffix=suffix,
        quality=quality,
        two_handed=two_handed,
        ammunition=ammunition)

    combined_modifiers = {
        "melee_chance_to_hit_modifier": 0,
        "ranged_chance_to_hit_modifier": 0,
        "armor_modifier": 0,
        "armor_class_modifier": 0,
        "dodge_modifier": 0,
        "shield_armor_class": 0,
        "max_hp_modifier": 0,
        "speed_modifier": 0,
        "movement_energy_bonus_modifier": 0,
        "melee_attack_energy_bonus_modifier": 0,
        "critical_hit_chance_modifier": 0,
        "critical_hit_damage_multiplier_modifier": 0,
        "strength_modifier": 0,
        "perception_modifier": 0,
        "dexterity_modifier": 0,
        "constitution_modifier": 0,
        "intelligence_modifier": 0,
        "wisdom_modifier": 0,
        "charisma_modifier": 0,
        "luck_modifier": 0,
        "life_steal_modifier": 0,
        "damage_reflection_modifier": 0,
        "natural_hp_regeneration_speed_modifier": 0,
        "melee_damage_modifiers": {
            "physical": 0,
            "fire": 0,
            "ice": 0,
            "lightning": 0,
            "holy": 0,
            "chaos": 0,
            "arcane": 0,
            "poison": 0,
        },
        "ranged_damage_modifiers": {
            "physical": 0,
            "fire": 0,
            "ice": 0,
            "lightning": 0,
            "holy": 0,
            "chaos": 0,
            "arcane": 0,
            "poison": 0,
        },
        "melee_damage_dice": {
            "physical": [],
            "fire": [],
            "ice": [],
            "lightning": [],
            "holy": [],
            "chaos": [],
            "arcane": [],
            "poison": [],
        },
        "ranged_damage_dice": {
            "physical": [],
            "fire": [],
            "ice": [],
            "lightning": [],
            "holy": [],
            "chaos": [],
            "arcane": [],
            "poison": [],
        },
        "resistances": {
            "physical": 0,
            "fire": 0,
            "ice": 0,
            "lightning": 0,
            "holy": 0,
            "chaos": 0,
            "arcane": 0,
            "poison": 0,
        }
    }

    for modifiers in total_modifiers:
        for modifier_name, modifier_value in modifiers.items():
            if modifier_name in modifiers:
                if type(modifier_value) is dict:
                    if modifier_name in ["melee_damage_dice", "ranged_damage_dice"]:
                        for damage_type in modifiers[modifier_name]:
                            new_value = modifiers[modifier_name][damage_type]
                            combined_modifiers[modifier_name][
                                damage_type].extend(new_value)
                    elif modifier_name == "melee_damage_dice_modifiers":
                        for damage_type in modifiers[modifier_name]:
                            for dice_count, dice_sides in modifiers[
                                    modifier_name][damage_type]:
                                if combined_modifiers["melee_damage_dice"][
                                        damage_type]:
                                    combined_modifiers["melee_damage_dice"][
                                        damage_type][0][0] += dice_count
                                    combined_modifiers["melee_damage_dice"][
                                        damage_type][0][1] += dice_sides
                                else:
                                    combined_modifiers["melee_damage_dice"][
                                        damage_type].append(
                                            [dice_count, dice_sides])
                    elif modifier_name == "ranged_damage_dice_modifiers":
                        for damage_type in modifiers[modifier_name]:
                            for dice_count, dice_sides in modifiers[
                                    modifier_name][damage_type]:
                                if combined_modifiers["ranged_damage_dice"][
                                        damage_type]:
                                    combined_modifiers["ranged_damage_dice"][
                                        damage_type][0][0] += dice_count
                                    combined_modifiers["ranged_damage_dice"][
                                        damage_type][0][1] += dice_sides
                                else:
                                    combined_modifiers["ranged_damage_dice"][
                                        damage_type].append(
                                            [dice_count, dice_sides])
                    else:
                        modifier_dict = modifiers[modifier_name]
                        combined_dict = combined_modifiers[modifier_name]
                        new_value = {
                            key: modifier_dict.get(key, 0) +
                            combined_dict.get(key, 0)
                            for key in set(modifier_dict)
                            | set(combined_dict)
                        }
                        combined_modifiers[modifier_name] = new_value
                else:
                    new_value = modifiers[modifier_name] + combined_modifiers[
                        modifier_name]
                    combined_modifiers[modifier_name] = new_value

    equippable_component = Equippable(random_weapon, slot)

    for modifier_name, modifier_value in combined_modifiers.items():
        setattr(equippable_component, modifier_name, modifier_value)

    new_weapon = Entity(0,
                        0,
                        "(",
                        random_weapon.unidentified_name,
                        equippable=equippable_component)

    return new_weapon


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
                                      melee_damage_dice={
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
                        starter_weapon.identified_name,
                        equippable=equippable_component)

    return new_entity
