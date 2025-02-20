from random import random, randint, choices, sample
from components.equippable import Equippable
from entity import Entity
from equipment_slots import equipment_slot_armor_list
import collections
import tcod as libtcod

material_names = [
    "hide", "leather", "boiled leather", "studded leather",
    "reinforced leather", "shadowed leather", "copper", "bronze", "iron",
    "steel", "truesteel", "darksteel", "orichalcum", "mithril", "voidstone",
    "brimstone", "cold iron", "thunderstone", "pearlstone", "electrum",
    "adamantine", "meteoric iron"
]

material_weights = [
    0.1, 0.11, 0.09, 0.08, 0.06, 0.05, 0.12, 0.11, 0.1, 0.08, 0.01, 0.02, 0.02,
    0.02, 0.0045, 0.0045, 0.0045, 0.0045, 0.0045, 0.0045, 0.0005, 0.0025
]

qualities = [
    "abysmal", "awful", "bad", "poor", "fair", "normal", "fine", "good",
    "superior", "excellent", "exceptional", "exquisite", "flawless"
]

quality_weights = [
    0.0075, 0.0125, 0.025, 0.05, 0.1, 0.5, 0.15, 0.0825, 0.04, 0.0225, 0.01,
    0.00375, 0.001875
]


def generate_quality_modifiers():
    quality_modifiers = {
        "abysmal": {
            "armor_modifier": randint(-5, 0),
            "armor_class_modifier": randint(-5, 0)
        },
        "awful": {
            "armor_modifier": randint(-4, 0),
            "armor_class_modifier": randint(-4, 0)
        },
        "bad": {
            "armor_modifier": randint(-3, 0),
            "armor_class_modifier": randint(-3, 0)
        },
        "poor": {
            "armor_modifier": randint(-2, 1),
            "armor_class_modifier": randint(-2, 1)
        },
        "fair": {
            "armor_modifier": randint(-1, 1),
            "armor_class_modifier": randint(-1, 1)
        },
        "normal": {
            "armor_class_modifier": randint(0, 1)
        },
        "fine": {
            "armor_modifier": randint(0, 1),
            "armor_class_modifier": randint(0, 1)
        },
        "good": {
            "armor_modifier": randint(0, 1),
            "armor_class_modifier": randint(0, 2)
        },
        "superior": {
            "armor_modifier": randint(0, 1),
            "armor_class_modifier": randint(1, 2)
        },
        "excellent": {
            "armor_modifier": randint(1, 2),
            "armor_class_modifier": randint(1, 3)
        },
        "exceptional": {
            "armor_modifier": randint(1, 2),
            "armor_class_modifier": randint(2, 3)
        },
        "exquisite": {
            "armor_modifier": randint(1, 2),
            "armor_class_modifier": randint(2, 4)
        },
        "flawless": {
            "armor_modifier": randint(1, 3),
            "armor_class_modifier": randint(2, 5),
            "resistances": {
                "physical": randint(1, 3) / 100
            }
        }
    }
    return quality_modifiers


def generate_material_weights_from_dungeon_floor(dungeon_floor):
    common_material_weights = material_weights[:10]
    rare_material_weights = material_weights[10:]
    new_common_material_weights = [
        weight - ((weight / 100) * (dungeon_floor - 1))
        for weight in common_material_weights
    ]
    removed_weight = sum(common_material_weights) - sum(
        new_common_material_weights)
    weight_fraction = removed_weight / len(rare_material_weights)
    new_rare_material_weights = [
        weight + weight_fraction for weight in rare_material_weights
    ]
    return new_common_material_weights + new_rare_material_weights


armor_rarities = {
    "rarity_levels":
    ["normal", "common", "uncommon", "rare", "epic", "mythical"],
    "rarity_weights": [0.535, 0.255, 0.125, 0.055, 0.029, 0.001],
    "rarity_colors": {
        "normal": libtcod.white,
        "common": libtcod.green,
        "uncommon": libtcod.blue,
        "rare": libtcod.gold,
        "epic": libtcod.purple,
        "mythical": libtcod.red
    },
    "rarity_color_names": {
        "normal": "white",
        "common": "green",
        "uncommon": "blue",
        "rare": "yellow",
        "epic": "purple",
        "mythical": "red"
    }
}

armor_prefixes = [
    "Tempered", "Hardened", "Unbreakable", "Indestructible", "Healing",
    "Vampiric", "Swift", "Quick", "Targeting", "Lucky", "Light", "Impervious",
    "Deadly", "Vigilant", "Blazing", "Freezing", "Shocking", "Sanctified",
    "Abyssal", "Esoteric", "Venomous", "Agile", "Stalwart", "Robust", "Astute",
    "Enlightened", "Appealing"
]

armor_prefix_weights = [
    0.12, 0.06, 0.03, 0.015, 0.08, 0.05, 0.08, 0.04, 0.08, 0.06, 0.06, 0.03,
    0.025, 0.05, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.025, 0.025, 0.025,
    0.025, 0.025, 0.025
]


def generate_armor_prefix_modifiers():
    armor_prefix_modifiers = {
        "Tempered": {
            "armor_modifier": randint(1, 2)
        },
        "Hardened": {
            "armor_modifier": randint(2, 3)
        },
        "Unbreakable": {
            "armor_modifier": randint(2, 4)
        },
        "Indestructible": {
            "armor_modifier": randint(3, 5)
        },
        "Healing": {
            "natural_hp_regeneration_speed_modifier": -5
        },
        "Vampiric": {
            "life_steal_modifier": randint(2, 5)
        },
        "Swift": {
            "speed_modifier": randint(1, 3)
        },
        "Quick": {
            "speed_modifier": randint(2, 5)
        },
        "Targeting": {
            "chance_to_hit_modifier": randint(2, 4)
        },
        "Lucky": {
            "luck_modifier": 1
        },
        "Light": {
            "movement_cost_modifier": randint(-10, -5)
        },
        "Impervious": {
            "armor_class_modifier": randint(2, 4),
            "armor_modifier": randint(1, 3)
        },
        "Deadly": {
            "critical_hit_chance_modifier": randint(1, 3)
        },
        "Vigilant": {
            "armor_class_modifier": randint(1, 3),
            "perception_modifier": 1
        },
        "Blazing": {
            "damage_dice": {
                "fire": [[1, 4]]
            }
        },
        "Freezing": {
            "damage_dice": {
                "ice": [[1, 4]],
            }
        },
        "Shocking": {
            "damage_dice": {
                "lightning": [[1, 4]]
            },
        },
        "Sanctified": {
            "damage_dice": {
                "holy": [[1, 4]]
            },
        },
        "Abyssal": {
            "damage_dice": {
                "chaos": [[1, 4]]
            },
        },
        "Esoteric": {
            "damage_dice": {
                "arcane": [[1, 4]]
            },
        },
        "Venomous": {
            "damage_dice": {
                "poison": [[1, 4]]
            },
        },
        "Agile": {
            "dexterity_modifier": 1
        },
        "Stalwart": {
            "constitution_modifier": 1
        },
        "Robust": {
            "strength_modifier": 1
        },
        "Astute": {
            "intelligence_modifier": 1
        },
        "Enlightened": {
            "wisdom_modifier": 1
        },
        "Appealing": {
            "charisma_modifier": 1
        },
    }
    return armor_prefix_modifiers


armor_suffixes = [
    "of Spikes",
    "of Thorns",
    "of Retaliation",
    "of Strength",
    "of the Juggernaut",
    "of the Hawk",
    "of the Eagle",
    "of the Cat",
    "of the Fox",
    "of Endurance",
    "of Toughness",
    "of the Magi",
    "of the Wizard",
    "of Wisdom",
    "of Piety",
    "of Charisma",
    "of the Silver Tongue",
    "of Fate",
    "of Fortune",
    "of Defense",
    "of the Rampart",
    "of Protection",
    "of the Fortress",
    "of Longevity",
    "of Health",
    "of Life",
    "of Flames",
    "of the Glacier",
    "of Thunder",
    "of the Heavens",
    "of the Void",
    "of the Arcane",
    "of Toxins",
    "of Alacrity",
]

armor_suffix_weights = [
    0.05,
    0.025,
    0.0125,
    0.025,
    0.0125,
    0.025,
    0.0125,
    0.025,
    0.0125,
    0.025,
    0.0125,
    0.025,
    0.0125,
    0.025,
    0.0125,
    0.025,
    0.0125,
    0.025,
    0.0125,
    0.09,
    0.04,
    0.09,
    0.04,
    0.075,
    0.0525,
    0.025,
    0.025,
    0.025,
    0.025,
    0.025,
    0.025,
    0.025,
    0.025,
    0.025,
]


def generate_armor_suffix_modifiers():
    armor_suffix_modifiers = {
        "of Spikes": {
            "damage_reflection_modifier": randint(5, 10)
        },
        "of Thorns": {
            "damage_reflection_modifier": randint(10, 15)
        },
        "of Retaliation": {
            "damage_reflection_modifier": randint(15, 20)
        },
        "of Strength": {
            "strength_modifier": randint(1, 2)
        },
        "of the Juggernaut": {
            "strength_modifier": randint(2, 4)
        },
        "of the Hawk": {
            "perception_modifier": randint(1, 2)
        },
        "of the Eagle": {
            "perception_modifier": randint(2, 4)
        },
        "of the Cat": {
            "dexterity_modifier": randint(1, 2)
        },
        "of the Fox": {
            "dexterity_modifier": randint(2, 4)
        },
        "of Endurance": {
            "constitution_modifier": randint(1, 2)
        },
        "of Toughness": {
            "constitution_modifier": randint(2, 4)
        },
        "of the Magi": {
            "intelligence_modifier": randint(1, 2)
        },
        "of the Wizard": {
            "intelligence_modifier": randint(2, 4)
        },
        "of Wisdom": {
            "wisdom_modifier": randint(1, 2)
        },
        "of Piety": {
            "wisdom_modifier": randint(2, 4)
        },
        "of Charisma": {
            "charisma_modifier": randint(1, 2)
        },
        "of the Silver Tongue": {
            "charisma_modifier": randint(2, 4)
        },
        "of Fate": {
            "luck_modifier": randint(1, 2)
        },
        "of Fortune": {
            "luck_modifier": randint(2, 4)
        },
        "of Defense": {
            "armor_class_modifier": randint(2, 4)
        },
        "of the Rampart": {
            "armor_class_modifier": randint(3, 6)
        },
        "of Protection": {
            "armor_modifier": randint(1, 2)
        },
        "of the Fortress": {
            "armor_modifier": randint(2, 4)
        },
        "of Longevity": {
            "max_hp_modifier": randint(5, 15)
        },
        "of Health": {
            "max_hp_modifier": randint(10, 25)
        },
        "of Life": {
            "max_hp_modifier": randint(15, 30)
        },
        "of Flames": {
            "resistances": {
                "fire": randint(15, 25) / 100
            },
            "damage_modifiers": {
                "fire": randint(2, 5)
            }
        },
        "of the Glacier": {
            "resistances": {
                "ice": randint(15, 25) / 100
            },
            "damage_modifiers": {
                "ice": randint(2, 5)
            },
        },
        "of Thunder": {
            "resistances": {
                "lightning": randint(15, 25) / 100
            },
            "damage_modifiers": {
                "lightning": randint(2, 5)
            }
        },
        "of the Heavens": {
            "resistances": {
                "holy": randint(15, 25) / 100
            },
            "damage_modifiers": {
                "holy": randint(2, 5)
            }
        },
        "of the Void": {
            "resistances": {
                "chaos": randint(15, 25) / 100
            },
            "damage_modifiers": {
                "chaos": randint(2, 5)
            }
        },
        "of the Arcane": {
            "resistances": {
                "arcane": randint(15, 25) / 100
            },
            "damage_modifiers": {
                "arcane": randint(2, 5)
            }
        },
        "of Toxins": {
            "resistances": {
                "poison": randint(15, 25) / 100
            },
            "damage_modifiers": {
                "poison": randint(2, 5)
            }
        },
        "of Alacrity": {
            "speed_modifier": randint(3, 6)
        },
    }
    return armor_suffix_modifiers


def generate_armor_rarity_modifiers():
    armor_rarity_modifiers = {
        "common": [{
            "armor_modifier": randint(0, 1)
        }, {
            "armor_class_modifier": randint(1, 2)
        }, {
            "max_hp_modifier": randint(1, 5)
        }, {
            "chance_to_hit_modifier": randint(1, 2)
        }, {
            "speed_modifier": randint(1, 3)
        }],
        "uncommon": [{
            "armor_modifier": randint(0, 2)
        }, {
            "armor_class_modifier": randint(1, 3)
        }, {
            "max_hp_modifier": randint(1, 6)
        }, {
            "chance_to_hit_modifier": randint(1, 3)
        }, {
            "speed_modifier": randint(1, 4)
        }, {
            "damage_modifiers": {
                "physical": randint(1, 2)
            }
        }],
        "rare": [{
            "armor_modifier": randint(0, 3)
        }, {
            "armor_class_modifier": randint(1, 4)
        }, {
            "max_hp_modifier": randint(2, 8)
        }, {
            "chance_to_hit_modifier": randint(2, 4)
        }, {
            "speed_modifier": randint(2, 5)
        }, {
            "damage_modifiers": {
                "physical": randint(1, 3)
            }
        }],
        "epic": [{
            "armor_modifier": randint(1, 5)
        }, {
            "armor_class_modifier": randint(2, 6)
        }, {
            "max_hp_modifier": randint(4, 10)
        }, {
            "chance_to_hit_modifier": randint(3, 6)
        }, {
            "speed_modifier": randint(3, 6)
        }, {
            "damage_modifiers": {
                "physical": randint(2, 5)
            }
        }],
        "mythical": [{
            "armor_modifier": randint(2, 6)
        }, {
            "armor_class_modifier": randint(3, 8)
        }, {
            "max_hp_modifier": randint(6, 12)
        }, {
            "chance_to_hit_modifier": randint(4, 8)
        }, {
            "speed_modifier": randint(4, 8)
        }, {
            "damage_modifiers": {
                "physical": randint(3, 6)
            }
        }]
    }
    return armor_rarity_modifiers


def generate_armor_material_modifiers():
    armor_material_modifiers = {
        "hide": {
            "armor_class_modifier": randint(0, 1),
            "movement_cost_modifier": randint(-5, -1)
        },
        "leather": {
            "armor_class_modifier": randint(0, 2),
            "movement_cost_modifier": randint(-4, -1)
        },
        "boiled leather": {
            "armor_class_modifier": randint(1, 2),
            "movement_cost_modifier": randint(-3, -1)
        },
        "studded leather": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(0, 2),
            "movement_cost_modifier": randint(-2, -1)
        },
        "reinforced leather": {
            "armor_class_modifier": randint(1, 4),
            "armor_modifier": randint(1, 2),
            "movement_cost_modifier": randint(-1, 0)
        },
        "shadowed leather": {
            "armor_class_modifier": randint(2, 4),
            "armor_modifier": randint(1, 3),
            "movement_cost_modifier": randint(-3, 0),
            "resistances": {
                "physical": randint(1, 3) / 100
            }
        },
        "copper": {
            "armor_class_modifier": randint(0, 1),
            "armor_modifier": randint(0, 1),
            "movement_cost_modifier": randint(0, 2),
            "resistances": {
                "physical": randint(1, 2) / 100
            },
            "speed_modifier": randint(-1, 0)
        },
        "bronze": {
            "armor_class_modifier": randint(-1, 1),
            "armor_modifier": randint(0, 2),
            "movement_cost_modifier": randint(0, 3),
            "resistances": {
                "physical": randint(1, 3) / 100
            },
            "speed_modifier": randint(-3, -1)
        },
        "iron": {
            "armor_class_modifier": randint(-2, -1),
            "armor_modifier": randint(0, 3),
            "movement_cost_modifier": randint(1, 4),
            "resistances": {
                "physical": randint(1, 4) / 100
            },
            "speed_modifier": randint(-4, -1)
        },
        "steel": {
            "armor_class_modifier": randint(-4, -1),
            "armor_modifier": randint(1, 4),
            "movement_cost_modifier": randint(2, 5),
            "resistances": {
                "physical": randint(1, 6) / 100
            },
            "speed_modifier": randint(-5, -2)
        },
        "truesteel": {
            "armor_class_modifier": randint(-2, -1),
            "armor_modifier": randint(2, 5),
            "movement_cost_modifier": randint(0, 3),
            "critical_hit_chance_modifier": randint(1, 5),
            "critical_hit_multiplier_modifier": randint(1, 5),
            "resistances": {
                "holy": randint(3, 8) / 100
            },
            "speed_modifier": randint(-4, -2)
        },
        "darksteel": {
            "armor_class_modifier": randint(-6, -2),
            "armor_modifier": randint(4, 9),
            "movement_cost_modifier": randint(6, 12),
            "resistances": {
                "physical": randint(5, 10) / 100
            },
            "speed_modifier": randint(-8, -4)
        },
        "orichalcum": {
            "armor_class_modifier": randint(-4, -1),
            "armor_modifier": randint(2, 5),
            "movement_cost_modifier": randint(1, 4),
            "resistances": {
                "physical": randint(4, 8) / 100
            },
            "speed_modifier": randint(-6, -2)
        },
        "mithril": {
            "armor_class_modifier": randint(0, 3),
            "armor_modifier": randint(2, 4),
            "movement_cost_modifier": randint(-2, 2),
            "resistances": {
                "physical": randint(3, 6) / 100,
                "holy": randint(2, 4) / 100
            },
            "speed_modifier": randint(-3, -1)
        },
        "voidstone": {
            "armor_class_modifier": randint(-4, -1),
            "armor_modifier": randint(3, 6),
            "movement_cost_modifier": randint(4, 8),
            "resistances": {
                "arcane": randint(5, 10) / 100,
                "chaos": randint(10, 20) / 100
            },
            "speed_modifier": randint(-8, -4),
            "luck_modifier": randint(0, 2)
        },
        "brimstone": {
            "armor_class_modifier": randint(-4, -1),
            "armor_modifier": randint(3, 6),
            "movement_cost_modifier": randint(4, 8),
            "resistances": {
                "arcane": randint(5, 10) / 100,
                "fire": randint(10, 20) / 100
            },
            "speed_modifier": randint(-8, -4),
            "strength_modifier": randint(0, 2)
        },
        "cold iron": {
            "armor_class_modifier": randint(-4, -1),
            "armor_modifier": randint(2, 8),
            "movement_cost_modifier": randint(4, 8),
            "resistances": {
                "arcane": randint(5, 10) / 100,
                "ice": randint(10, 20) / 100
            },
            "speed_modifier": randint(-8, -4),
            "dexterity_modifier": randint(0, 2)
        },
        "thunderstone": {
            "armor_class_modifier": randint(-5, -3),
            "armor_modifier": randint(3, 6),
            "movement_cost_modifier": randint(4, 8),
            "resistances": {
                "arcane": randint(5, 10) / 100,
                "lightning": randint(10, 20) / 100
            },
            "speed_modifier": randint(-4, -1),
            "constitution_modifier": randint(0, 2)
        },
        "pearlstone": {
            "armor_class_modifier": randint(-2, -1),
            "armor_modifier": randint(1, 3),
            "movement_cost_modifier": randint(1, 4),
            "resistances": {
                "arcane": randint(5, 10) / 100,
                "holy": randint(10, 20) / 100
            },
            "speed_modifier": randint(-4, -1),
            "wisdom_modifier": randint(0, 2)
        },
        "electrum": {
            "armor_class_modifier": randint(-3, -1),
            "armor_modifier": randint(2, 5),
            "movement_cost_modifier": randint(3, 6),
            "resistances": {
                "arcane": randint(10, 20) / 100,
            },
            "speed_modifier": randint(-5, -1),
            "intelligence_modifier": randint(0, 2)
        },
        "adamantine": {
            "armor_class_modifier": randint(0, 2),
            "armor_modifier": randint(5, 9),
            "movement_cost_modifier": randint(3, 9),
            "resistances": {
                "physical": randint(1, 5) / 100,
                "fire": randint(1, 5) / 100,
                "ice": randint(1, 5) / 100,
                "lightning": randint(1, 5) / 100,
                "holy": randint(1, 5) / 100,
                "chaos": randint(1, 5) / 100,
                "arcane": randint(1, 5) / 100,
                "poison": randint(1, 5) / 100,
            },
            "speed_modifier": randint(-5, 0)
        },
        "meteoric iron": {
            "armor_class_modifier": randint(-4, 0),
            "armor_modifier": randint(3, 5),
            "movement_cost_modifier": randint(-4, -1),
            "resistances": {
                "physical": randint(5, 10) / 100,
                "fire": randint(5, 10) / 100,
                "ice": randint(5, 10) / 100,
                "lightning": randint(5, 10) / 100,
            },
            "speed_modifier": randint(2, 6)
        },
    }
    return armor_material_modifiers


def generate_armor_name_modifiers():
    armor_name_modifiers = {
        # Headgear
        "cap": {
            "armor_class_modifier": randint(0, 1)
        },
        "helmet": {
            "armor_class_modifier": randint(1, 2)
        },
        "hood": {
            "armor_class_modifier": randint(0, 2),
            "speed_modifier": randint(0, 1)
        },
        "mask": {
            "armor_class_modifier": randint(0, 2),
            "speed_modifier": randint(0, 1),
            "resistances": {
                "poison": randint(1, 3) / 100
            }
        },
        "helm": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        "cervelliere": {
            "armor_class_modifier": randint(0, 3),
            "armor_modifier": randint(0, 1)
        },
        "nasal helmet": {
            "armor_class_modifier": randint(0, 3),
            "armor_modifier": randint(0, 2)
        },
        "mail coif": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(0, 2)
        },
        "circlet": {
            "armor_class_modifier": randint(0, 1),
            "armor_modifier": randint(0, 1),
            "resistances": {
                "fire": randint(0, 1) / 100,
                "ice": randint(0, 1) / 100,
                "lightning": randint(0, 1) / 100,
                "holy": randint(0, 1) / 100,
                "chaos": randint(0, 1) / 100,
                "arcane": randint(0, 1) / 100,
                "poison": randint(0, 1) / 100,
            }
        },
        "burgonet": {
            "armor_class_modifier": randint(0, 3),
            "armor_modifier": randint(1, 2),
        },
        "barbute": {
            "armor_class_modifier": randint(-1, 4),
            "armor_modifier": randint(1, 2),
        },
        "sallet": {
            "armor_class_modifier": randint(-1, 3),
            "armor_modifier": randint(1, 3),
            "perception_modifier": randint(-1, 0)
        },
        "enclosed helmet": {
            "armor_class_modifier": randint(0, 1),
            "armor_modifier": randint(1, 3),
            "perception_modifier": randint(-1, 0)
        },
        "great helm": {
            "armor_class_modifier": randint(0, 2),
            "armor_modifier": randint(2, 3),
            "perception_modifier": randint(-1, 0),
            "resistances": {
                "physical": randint(1, 2) / 100
            }
        },
        "bassinet": {
            "armor_class_modifier": randint(0, 2),
            "armor_modifier": randint(2, 3),
            "perception_modifier": randint(-1, 0),
            "resistances": {
                "physical": randint(1, 3) / 100
            }
        },
        "closed helmet": {
            "armor_class_modifier": randint(0, 2),
            "armor_modifier": randint(1, 4),
            "perception_modifier": randint(-2, 0),
            "resistances": {
                "physical": randint(2, 4) / 100
            }
        },
        "armet": {
            "armor_class_modifier": randint(-1, 1),
            "armor_modifier": randint(2, 4),
            "perception_modifier": randint(-2, -1),
            "resistances": {
                "physical": randint(2, 5) / 100
            }
        },
        # Shoulder armor
        "couters": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        "spaulders": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        "pauldrons": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        "gardbraces": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        "shoulderguards": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        "mantle": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        "epaulets": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        "shoulderpads": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        "shoulderplates": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        # Body armor
        "armor": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        "brigandine": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(0, 2)
        },
        "cuirass": {
            "armor_class_modifier": randint(0, 3),
            "armor_modifier": randint(0, 3),
            "speed_modifier": randint(-3, -1),
        },
        "ring mail": {
            "armor_class_modifier": randint(-1, 1),
            "armor_modifier": randint(1, 3),
            "speed_modifier": randint(-2, 0),
            "movement_cost_modifier": randint(2, 3)
        },
        "hauberk": {
            "armor_class_modifier": randint(-2, 0),
            "armor_modifier": randint(1, 4),
            "speed_modifier": randint(-2, 0),
            "movement_cost_modifier": randint(2, 5)
        },
        "light plate": {
            "armor_class_modifier": randint(-2, 0),
            "armor_modifier": randint(2, 5),
            "speed_modifier": randint(-3, 0),
            "movement_cost_modifier": randint(2, 6)
        },
        "mail": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(2, 6),
            "speed_modifier": randint(-3, 0),
            "movement_cost_modifier": randint(3, 6)
        },
        "plate": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(2, 6),
            "speed_modifier": randint(-4, -1),
            "movement_cost_modifier": randint(3, 7)
        },
        "splint mail": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(3, 6),
            "speed_modifier": randint(-5, -1),
            "movement_cost_modifier": randint(4, 7)
        },
        "plate mail": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(3, 7),
            "speed_modifier": randint(-5, -2),
            "movement_cost_modifier": randint(4, 8)
        },
        "breastplate": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(3, 8),
            "speed_modifier": randint(-6, -2),
            "movement_cost_modifier": randint(4, 9)
        },
        "faulds": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(4, 9),
            "speed_modifier": randint(-6, -3),
            "movement_cost_modifier": randint(5, 9)
        },
        "culet": {
            "armor_class_modifier": randint(-7, -3),
            "armor_modifier": randint(4, 10),
            "speed_modifier": randint(-6, -3),
            "movement_cost_modifier": randint(5, 10)
        },
        "plackart": {
            "armor_class_modifier": randint(-7, -4),
            "armor_modifier": randint(4, 11),
            "speed_modifier": randint(-7, -3),
            "movement_cost_modifier": randint(5, 11)
        },
        "full plate mail": {
            "armor_class_modifier": randint(-8, -4),
            "armor_modifier": randint(5, 12),
            "speed_modifier": randint(-8, -4),
            "movement_cost_modifier": randint(6, 12)
        },
        # Leg armor
        "greaves": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1),
            "speed_modifier": randint(-1, 1),
            "movement_cost_modifier": randint(-3, 0)
        },
        "tassets": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(0, 1),
            "speed_modifier": randint(-2, 2),
            "movement_cost_modifier": randint(-4, 0)
        },
        "leg guards": {
            "armor_class_modifier": randint(1, 4),
            "armor_modifier": randint(0, 2),
            "speed_modifier": randint(-3, 3),
            "movement_cost_modifier": randint(-5, 2)
        },
        "chausses": {
            "armor_class_modifier": randint(1, 4),
            "armor_modifier": randint(1, 2),
            "speed_modifier": randint(-4, 3),
            "movement_cost_modifier": randint(-3, 3)
        },
        "cuisses": {
            "armor_class_modifier": randint(1, 5),
            "armor_modifier": randint(1, 3),
            "speed_modifier": randint(-5, 2),
            "movement_cost_modifier": randint(-2, 4)
        },
        "poleyns": {
            "armor_class_modifier": randint(2, 5),
            "armor_modifier": randint(2, 4),
            "speed_modifier": randint(-6, 1),
            "movement_cost_modifier": randint(-1, 5)
        },
        # Wrist armor
        "bracers": {
            "armor_class_modifier": randint(0, 1),
            "armor_modifier": randint(0, 1),
            "attack_cost_modifier": randint(-5, 0)
        },
        "rerebraces": {
            "armor_class_modifier": randint(0, 2),
            "armor_modifier": randint(0, 1),
            "attack_cost_modifier": randint(-6, 0)
        },
        "bracers": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(1, 2),
            "attack_cost_modifier": randint(-7, 0)
        },
        "vambraces": {
            "armor_class_modifier": randint(1, 4),
            "armor_modifier": randint(1, 3),
            "attack_cost_modifier": randint(-8, 0)
        },
        # Hand armor
        "gloves": {
            "armor_class_modifier": randint(0, 2),
            "armor_modifier": randint(0, 1),
            "attack_cost_modifier": randint(-2, 0)
        },
        "grips": {
            "armor_class_modifier": randint(0, 1),
            "armor_modifier": randint(0, 1),
            "attack_cost_modifier": randint(-3, 0)
        },
        "handguards": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(0, 2),
            "attack_cost_modifier": randint(-4, 0)
        },
        "gauntlets": {
            "armor_class_modifier": randint(1, 4),
            "armor_modifier": randint(1, 3),
            "attack_cost_modifier": randint(-5, 0)
        },
        # Boots
        "footwear": {
            "armor_class_modifier": randint(1, 4),
            "armor_modifier": randint(0, 1),
            "movement_cost_modifier": randint(-2, 0)
        },
        "boots": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(0, 1),
            "movement_cost_modifier": randint(-3, 0)
        },
        "footpads": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(0, 1),
            "movement_cost_modifier": randint(-4, 0)
        },
        "sandals": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1),
            "movement_cost_modifier": randint(-5, 0)
        },
        "sabatons": {
            "armor_class_modifier": randint(2, 3),
            "armor_modifier": randint(1, 3),
            "movement_cost_modifier": randint(-4, 0)
        },
        "treads": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(2, 4),
            "movement_cost_modifier": randint(-3, 0)
        },
        "warboots": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(2, 5),
            "movement_cost_modifier": randint(-2, 0)
        },
        # Shields
        "guige": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        "buckler": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(0, 1)
        },
        "small shield": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(0, 2)
        },
        "shield": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(1, 2)
        },
        "round shield": {
            "armor_class_modifier": randint(1, 4),
            "armor_modifier": randint(1, 2)
        },
        "large shield": {
            "armor_class_modifier": randint(1, 5),
            "armor_modifier": randint(1, 3)
        },
        "war shield": {
            "armor_class_modifier": randint(1, 6),
            "armor_modifier": randint(2, 3)
        },
        "bulwark": {
            "armor_class_modifier": randint(1, 7),
            "armor_modifier": randint(1, 4)
        },
        "enarmes": {
            "armor_class_modifier": randint(1, 8),
            "armor_modifier": randint(2, 4),
            "resistances": {
                "physical": randint(1, 3) / 100
            }
        },
        "heater shield": {
            "armor_class_modifier": randint(1, 9),
            "armor_modifier": randint(1, 5),
            "resistances": {
                "physical": randint(1, 4) / 100
            }
        },
        "kite shield": {
            "armor_class_modifier": randint(1, 10),
            "armor_modifier": randint(2, 5),
            "resistances": {
                "physical": randint(1, 5) / 100
            }
        },
        "rondache": {
            "armor_class_modifier": randint(1, 11),
            "armor_modifier": randint(2, 6),
            "resistances": {
                "physical": randint(1, 6) / 100
            }
        },
        "targe": {
            "armor_class_modifier": randint(1, 12),
            "armor_modifier": randint(3, 6),
            "resistances": {
                "physical": randint(1, 7) / 100
            }
        },
        "tower shield": {
            "armor_class_modifier": randint(1, 13),
            "armor_modifier": randint(3, 7),
            "resistances": {
                "physical": randint(1, 8) / 100
            }
        },
    }
    return armor_name_modifiers


armor_names = {
    "HEAD": {
        "leather": ["cap", "helmet", "hood", "mask"],
        "leather_weights": [0.33, 0.33, 0.17, 0.17],
        "metal": [
            "helm", "cervelliere", "nasal helmet", "helmet", "mail coif",
            "circlet", "burgonet", "barbute", "sallet", "enclosed helmet",
            "great helm", "bassinet", "closed helmet", "armet"
        ],
        "metal_weights": [
            0.17, 0.15, 0.12, 0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03,
            0.02, 0.015, 0.005
        ]
    },
    "SHOULDERS": {
        "leather": [
            "couters", "spaulders", "pauldrons", "gardbraces",
            "shoulderguards", "mantle", "epaulets", "shoulderpads"
        ],
        "leather_weights": [0.2, 0.17, 0.16, 0.135, 0.11, 0.095, 0.07, 0.06],
        "metal": [
            "couters", "spaulders", "pauldrons", "gardbraces",
            "shoulderguards", "mantle", "epaulets", "shoulderpads",
            "shoulderplates"
        ],
        "metal_weights":
        [0.18, 0.16, 0.14, 0.125, 0.1, 0.095, 0.08, 0.07, 0.05],
    },
    "TORSO": {
        "leather": ["armor", "brigandine", "cuirass"],
        "leather_weights": [0.5, 0.375, 0.125],
        "metal": [
            "ring mail", "hauberk", "light plate", "mail", "plate",
            "splint mail", "plate mail", "breastplate", "faulds", "culet",
            "plackart", "cuirass", "full plate mail"
        ],
        "metal_weights": [
            0.14, 0.13, 0.12, 0.11, 0.1, 0.09, 0.08, 0.07, 0.06, 0.04, 0.03,
            0.02, 0.01
        ]
    },
    "LEGS": {
        "leather": ["greaves", "tassets", "leg guards"],
        "leather_weights": [0.5, 0.375, 0.125],
        "metal":
        ["chausses", "greaves", "cuisses", "tassets", "poleyns", "leg guards"],
        "metal_weights": [0.35, 0.27, 0.125, 0.1, 0.09, 0.065]
    },
    "WRISTS": {
        "leather": ["bracers"],
        "leather_weights": [1],
        "metal": ["rerebraces", "bracers", "vambraces"],
        "metal_weights": [0.5, 0.375, 0.125]
    },
    "GLOVES": {
        "leather": ["gloves", "grips", "handguards"],
        "leather_weights": [0.5, 0.375, 0.125],
        "metal": ["gauntlets", "handguards"],
        "metal_weights": [0.5, 0.5]
    },
    "BOOTS": {
        "leather": ["footwear", "boots", "footpads", "sandals"],
        "leather_weights": [0.33, 0.175, 0.295, 0.2],
        "metal": ["boots", "sabatons", "treads", "warboots"],
        "metal_weights": [0.33, 0.175, 0.295, 0.2]
    },
    "OFF_HAND": {
        "leather": ["shield", "small shield"],
        "leather_weights": [0.5, 0.5],
        "metal": [
            "guige",
            "buckler",
            "small shield",
            "shield",
            "round shield",
            "large shield",
            "war shield",
            "bulwark",
            "enarmes",
            "heater shield",
            "kite shield",
            "rondache",
            "targe",
            "tower shield",
        ],
        "metal_weights": [
            0.13, 0.12, 0.115, 0.105, 0.1, 0.095, 0.09, 0.075, 0.05, 0.04,
            0.035, 0.02, 0.015, 0.01
        ]
    }
}

armor_characters = {
    "HEAD": "^",
    "SHOULDERS": "´",
    "TORSO": "[",
    "LEGS": "}",
    "WRISTS": "~",
    "GLOVES": "{",
    "BOOTS": "-",
    "OFF_HAND": "]"
}


# equippable type is built as a class with the following properties:
# equipment_type: e.g. "weapon", "torso", "ring" etc.
# weapons and armor also have additional properties in equipment_type, such as weapon type and such
# unidentified_name: generic name for the equipment
# identified_name : full name of the equipment, including material, quality, prefixes and suffixes
# material: material of the equipment, giving specific bonuses
# quality: quality of the equipment, giving specific bonuses
class Armor:
    def __init__(self,
                 rarity=None,
                 material=None,
                 slot_type=None,
                 armor_name=None,
                 unidentified_name=None,
                 identified_name=None,
                 prefix=None,
                 suffix=None,
                 quality=None):
        self.rarity = rarity
        self.material = material
        self.slot_type = slot_type
        self.armor_name = armor_name
        self.unidentified_name = unidentified_name
        self.identified_name = identified_name
        self.prefix = prefix
        self.suffix = suffix
        self.quality = quality


def generate_random_armor():
    material = ''.join(choices(material_names, material_weights, k=1))
    rarity_level = ''.join(
        choices(armor_rarities["rarity_levels"],
                armor_rarities["rarity_weights"],
                k=1))
    quality = ''.join(choices(qualities, quality_weights, k=1))

    prefix = None
    prefix_seed = random()
    suffix = None
    suffix_seed = random()

    if prefix_seed <= 0.25:
        prefix = ''.join(choices(armor_prefixes, armor_prefix_weights, k=1))

    if suffix_seed <= 0.25:
        suffix = ''.join(choices(armor_suffixes, armor_suffix_weights, k=1))

    rarity = {
        "rarity_level": rarity_level,
        "rarity_color": armor_rarities["rarity_colors"][rarity_level],
        "rarity_color_name": armor_rarities["rarity_color_names"][rarity_level]
    }

    armor_material = material

    equipment_slot_index = randint(0, len(equipment_slot_armor_list) - 1)
    slot = equipment_slot_armor_list[equipment_slot_index]

    if "leather" in material or "hide" in material:
        armor_name = ''.join(
            choices(armor_names[slot._name_]["leather"],
                    armor_names[slot._name_]["leather_weights"],
                    k=1))
    else:
        armor_name = ''.join(
            choices(armor_names[slot._name_]["metal"],
                    armor_names[slot._name_]["metal_weights"],
                    k=1))

    material_modifiers = generate_armor_material_modifiers()[material]
    armor_name_modifiers = generate_armor_name_modifiers()[armor_name]
    armor_quality_modifiers = generate_quality_modifiers()[quality]

    total_modifiers = [
        material_modifiers, armor_name_modifiers, armor_quality_modifiers
    ]

    if prefix:
        prefix_modifiers = generate_armor_prefix_modifiers()[prefix]
        total_modifiers.append(prefix_modifiers)

    if suffix:
        suffix_modifiers = generate_armor_suffix_modifiers()[suffix]
        total_modifiers.append(suffix_modifiers)

    if rarity_level != "normal":
        possible_rarity_modifiers = generate_armor_rarity_modifiers(
        )[rarity_level]
        rarity_seed = randint(1, len(possible_rarity_modifiers) - 1)
        rarity_modifiers = possible_rarity_modifiers[rarity_seed]
        total_modifiers.append(rarity_modifiers)

    unidentified_name = f"{armor_material.title()} {armor_name.title()}"
    identified_name = f"{rarity_level.title() + ' ' if rarity_level != 'normal' else ''}{prefix + ' ' if prefix else ''}{armor_material.title()} {armor_name.title()}{' ' + suffix if suffix else ''}{' (' + quality + ')' if quality != 'normal' else ''}"

    random_armor = Armor(rarity,
                         armor_material,
                         slot,
                         armor_name,
                         unidentified_name,
                         identified_name,
                         prefix,
                         suffix,
                         quality=quality)

    combined_modifiers = {
        "chance_to_hit_modifier": 0,
        "armor_modifier": 0,
        "armor_class_modifier": 0,
        "max_hp_modifier": 0,
        "speed_modifier": 0,
        "movement_cost_modifier": 0,
        "attack_cost_modifier": 0,
        "critical_hit_chance_modifier": 0,
        "critical_hit_multiplier_modifier": 0,
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
        "damage_modifiers": {
            "physical": 0,
            "fire": 0,
            "ice": 0,
            "lightning": 0,
            "holy": 0,
            "chaos": 0,
            "arcane": 0,
            "poison": 0,
        },
        "damage_dice": {
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
                    if modifier_name == "damage_dice":
                        for damage_type in modifiers[modifier_name]:
                            new_value = modifiers[modifier_name][damage_type]
                            combined_modifiers[modifier_name][
                                damage_type].extend(new_value)
                    elif modifier_name == "damage_dice_modifiers":
                        for damage_type in modifiers[modifier_name]:
                            for dice_count, dice_sides in modifiers[modifier_name][damage_type]:
                                if combined_modifiers["damage_dice"][damage_type]:
                                    combined_modifiers["damage_dice"][damage_type][0][0] += dice_count
                                    combined_modifiers["damage_dice"][damage_type][
                                        0][1] += dice_sides
                                else:
                                    combined_modifiers["damage_dice"][damage_type].append([dice_count, dice_sides])

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

    chance_to_hit_modifier = combined_modifiers["chance_to_hit_modifier"]
    armor_modifier = combined_modifiers["armor_modifier"]
    armor_class_modifier = combined_modifiers["armor_class_modifier"]
    max_hp_modifier = combined_modifiers["max_hp_modifier"]
    speed_modifier = combined_modifiers["speed_modifier"]
    movement_cost_modifier = combined_modifiers["movement_cost_modifier"]
    attack_cost_modifier = combined_modifiers["attack_cost_modifier"]
    critical_hit_chance_modifier = combined_modifiers[
        "critical_hit_chance_modifier"]
    critical_hit_multiplier_modifier = combined_modifiers[
        "critical_hit_multiplier_modifier"]
    strength_modifier = combined_modifiers["strength_modifier"]
    perception_modifier = combined_modifiers["perception_modifier"]
    dexterity_modifier = combined_modifiers["dexterity_modifier"]
    constitution_modifier = combined_modifiers["constitution_modifier"]
    intelligence_modifier = combined_modifiers["intelligence_modifier"]
    wisdom_modifier = combined_modifiers["wisdom_modifier"]
    charisma_modifier = combined_modifiers["charisma_modifier"]
    luck_modifier = combined_modifiers["luck_modifier"]
    life_steal_modifier = combined_modifiers["life_steal_modifier"]
    damage_reflection_modifier = combined_modifiers[
        "damage_reflection_modifier"]
    natural_hp_regeneration_speed_modifier = combined_modifiers[
        "natural_hp_regeneration_speed_modifier"]
    damage_modifiers = combined_modifiers["damage_modifiers"]
    damage_dice = combined_modifiers["damage_dice"]
    resistances = combined_modifiers["resistances"]

    equippable_component = Equippable(
        random_armor, slot, chance_to_hit_modifier, armor_modifier,
        armor_class_modifier, max_hp_modifier, speed_modifier,
        movement_cost_modifier, attack_cost_modifier,
        critical_hit_chance_modifier, critical_hit_multiplier_modifier,
        strength_modifier, perception_modifier, dexterity_modifier,
        constitution_modifier, intelligence_modifier, wisdom_modifier,
        charisma_modifier, luck_modifier, life_steal_modifier,
        damage_reflection_modifier, natural_hp_regeneration_speed_modifier,
        damage_modifiers, damage_dice, resistances)

    new_armor = Entity(0,
                        0,
                        armor_characters[slot._name_],
                        random_armor.rarity["rarity_color"],
                        random_armor.identified_name,
                        equippable=equippable_component)

    return new_armor
