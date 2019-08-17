from random import random, randint, choices, sample
from components.equippable import Equippable
from entity import Entity
from equipment_slots import equipment_slot_armor_list
from components.equipment_attributes import rarities, armor_material_names, armor_material_weights, qualities, quality_weights, armor_prefixes, armor_prefix_weights, armor_suffixes, armor_suffix_weights
import collections
import tcod as libtcod


def generate_quality_modifiers():
    quality_modifiers = {
        "abysmal": {
            "armor_modifier": randint(-4, 0),
            "armor_class_modifier": randint(-4, 0)
        },
        "awful": {
            "armor_modifier": randint(-3, 0),
            "armor_class_modifier": randint(-3, 0)
        },
        "bad": {
            "armor_modifier": randint(-2, 0),
            "armor_class_modifier": randint(-2, 0)
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
    common_material_weights = armor_material_weights[:10]
    rare_material_weights = armor_material_weights[10:]
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


def generate_armor_prefix_modifiers():
    armor_prefix_modifiers = {
        "Tempered": {
            "armor_modifier": 1
        },
        "Hardened": {
            "armor_modifier": randint(1, 2)
        },
        "Unbreakable": {
            "armor_modifier": randint(1, 3)
        },
        "Indestructible": {
            "armor_modifier": randint(2, 4)
        },
        "Healing": {
            "natural_hp_regeneration_speed_modifier": -5
        },
        "Vampiric": {
            "life_steal_modifier": randint(5, 10) / 100
        },
        "Swift": {
            "speed_modifier": randint(1, 3)
        },
        "Quick": {
            "speed_modifier": randint(2, 5)
        },
        "Targeting": {
            "melee_chance_to_hit_modifier": randint(2, 4),
            "ranged_chance_to_hit_modifier": randint(2, 4)
        },
        "Lucky": {
            "luck_modifier": 1
        },
        "Light": {
            "movement_energy_bonus_modifier": randint(5, 10)
        },
        "Impervious": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(1, 2)
        },
        "Deadly": {
            "critical_hit_chance_modifier": randint(2, 4) / 100
        },
        "Vigilant": {
            "armor_class_modifier": randint(1, 2),
            "perception_modifier": 1
        },
        "Blazing": {
            "melee_damage_dice": {
                "fire": [[1, 4]]
            },
            "ranged_damage_dice": {
                "fire": [[1, 4]]
            }
        },
        "Freezing": {
            "melee_damage_dice": {
                "ice": [[1, 4]],
            },
            "ranged_damage_dice": {
                "ice": [[1, 4]],
            }
        },
        "Shocking": {
            "melee_damage_dice": {
                "lightning": [[1, 4]]
            },
            "ranged_damage_dice": {
                "lightning": [[1, 4]]
            },
        },
        "Sanctified": {
            "melee_damage_dice": {
                "holy": [[1, 4]]
            },
            "ranged_damage_dice": {
                "holy": [[1, 4]]
            },
        },
        "Abyssal": {
            "melee_damage_dice": {
                "chaos": [[1, 4]]
            },
            "ranged_damage_dice": {
                "chaos": [[1, 4]]
            },
        },
        "Esoteric": {
            "melee_damage_dice": {
                "arcane": [[1, 4]]
            },
            "ranged_damage_dice": {
                "arcane": [[1, 4]]
            },
        },
        "Venomous": {
            "melee_damage_dice": {
                "poison": [[1, 4]]
            },
            "ranged_damage_dice": {
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


def generate_armor_suffix_modifiers():
    armor_suffix_modifiers = {
        "of Spikes": {
            "damage_reflection_modifier": randint(5, 10) / 100
        },
        "of Thorns": {
            "damage_reflection_modifier": randint(10, 15) / 100
        },
        "of Retaliation": {
            "damage_reflection_modifier": randint(15, 20) / 100
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
            "armor_class_modifier": randint(1, 2)
        },
        "of the Rampart": {
            "armor_class_modifier": randint(2, 3)
        },
        "of Protection": {
            "armor_modifier": randint(1, 2)
        },
        "of the Fortress": {
            "armor_modifier": randint(2, 3)
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
            "melee_damage_modifiers": {
                "fire": randint(2, 5)
            },
            "ranged_damage_modifiers": {
                "fire": randint(2, 5)
            }
        },
        "of the Glacier": {
            "resistances": {
                "ice": randint(15, 25) / 100
            },
            "melee_damage_modifiers": {
                "ice": randint(2, 5)
            },
            "ranged_damage_modifiers": {
                "ice": randint(2, 5)
            },
        },
        "of Thunder": {
            "resistances": {
                "lightning": randint(15, 25) / 100
            },
            "melee_damage_modifiers": {
                "lightning": randint(2, 5)
            },
            "ranged_damage_modifiers": {
                "ice": randint(2, 5)
            },
        },
        "of the Heavens": {
            "resistances": {
                "holy": randint(15, 25) / 100
            },
            "melee_damage_modifiers": {
                "holy": randint(2, 5)
            },
            "ranged_damage_modifiers": {
                "ice": randint(2, 5)
            },
        },
        "of the Void": {
            "resistances": {
                "chaos": randint(15, 25) / 100
            },
            "melee_damage_modifiers": {
                "chaos": randint(2, 5)
            },
            "ranged_damage_modifiers": {
                "ice": randint(2, 5)
            },
        },
        "of the Arcane": {
            "resistances": {
                "arcane": randint(15, 25) / 100
            },
            "melee_damage_modifiers": {
                "arcane": randint(2, 5)
            },
            "ranged_damage_modifiers": {
                "ice": randint(2, 5)
            },
        },
        "of Toxins": {
            "resistances": {
                "poison": randint(15, 25) / 100
            },
            "melee_damage_modifiers": {
                "poison": randint(2, 5)
            },
            "ranged_damage_modifiers": {
                "poison": randint(2, 5)
            }
        },
        "of Alacrity": {
            "speed_modifier": randint(4, 8)
        },
        "of Evasion": {
            "dodge_modifier": randint(2, 4)
        }
    }
    return armor_suffix_modifiers


def generate_armor_rarity_modifiers():
    armor_rarity_modifiers = {
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
            "attack_energy_bonus_modifier": randint(1, 2)
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
            "attack_energy_bonus_modifier": randint(1, 3)
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
            "attack_energy_bonus_modifier": randint(1, 4)
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
            "attack_energy_bonus_modifier": randint(2, 5)
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
            "attack_energy_bonus_modifier": randint(2, 6)
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
    return armor_rarity_modifiers


def generate_armor_material_modifiers():
    armor_material_modifiers = {
        "hide": {
            "armor_class_modifier": randint(0, 1),
            "movement_energy_bonus_modifier": randint(1, 5)
        },
        "leather": {
            "armor_class_modifier": randint(0, 2),
            "movement_energy_bonus_modifier": randint(1, 5)
        },
        "boiled leather": {
            "armor_class_modifier": randint(1, 2),
            "movement_energy_bonus_modifier": randint(1, 3)
        },
        "studded leather": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(0, 2),
            "movement_energy_bonus_modifier": randint(1, 2)
        },
        "reinforced leather": {
            "armor_class_modifier": randint(1, 4),
            "armor_modifier": randint(1, 2),
            "movement_energy_bonus_modifier": randint(0, 1)
        },
        "shadowed leather": {
            "armor_class_modifier": randint(2, 4),
            "armor_modifier": randint(1, 3),
            "movement_energy_bonus_modifier": randint(0, 3),
            "resistances": {
                "physical": randint(1, 3) / 100
            }
        },
        "copper": {
            "armor_class_modifier": randint(0, 1),
            "armor_modifier": randint(0, 1),
            "movement_energy_bonus_modifier": randint(-2, 0),
            "resistances": {
                "physical": randint(1, 2) / 100
            },
            "speed_modifier": randint(-1, 0)
        },
        "bronze": {
            "armor_class_modifier": randint(-1, 1),
            "armor_modifier": randint(0, 2),
            "movement_energy_bonus_modifier": randint(-3, 0),
            "resistances": {
                "physical": randint(1, 3) / 100
            },
            "speed_modifier": randint(-3, -1)
        },
        "iron": {
            "armor_class_modifier": randint(-2, -1),
            "armor_modifier": randint(0, 3),
            "movement_energy_bonus_modifier": randint(-4, -1),
            "resistances": {
                "physical": randint(1, 4) / 100
            },
            "speed_modifier": randint(-4, -1)
        },
        "steel": {
            "armor_class_modifier": randint(-4, -1),
            "armor_modifier": randint(1, 4),
            "movement_energy_bonus_modifier": randint(-5, -2),
            "resistances": {
                "physical": randint(1, 6) / 100
            },
            "speed_modifier": randint(-5, -2)
        },
        "truesteel": {
            "armor_class_modifier": randint(-2, -1),
            "armor_modifier": randint(2, 5),
            "movement_energy_bonus_modifier": randint(-3, 0),
            "critical_hit_chance_modifier": randint(1, 5) / 100,
            "critical_hit_damage_multiplier_modifier": randint(1, 5) / 100,
            "resistances": {
                "holy": randint(3, 8) / 100
            },
            "speed_modifier": randint(-4, -2)
        },
        "darksteel": {
            "armor_class_modifier": randint(-8, -3),
            "armor_modifier": randint(4, 9),
            "movement_energy_bonus_modifier": randint(-12, -6),
            "resistances": {
                "physical": randint(5, 10) / 100
            },
            "speed_modifier": randint(-8, -4)
        },
        "orichalcum": {
            "armor_class_modifier": randint(-4, -1),
            "armor_modifier": randint(2, 5),
            "movement_energy_bonus_modifier": randint(-4, -1),
            "resistances": {
                "physical": randint(4, 8) / 100
            },
            "speed_modifier": randint(-6, -2)
        },
        "mithril": {
            "armor_class_modifier": randint(0, 3),
            "armor_modifier": randint(2, 4),
            "movement_energy_bonus_modifier": randint(-3, 2),
            "resistances": {
                "physical": randint(3, 6) / 100,
                "holy": randint(2, 4) / 100
            },
            "speed_modifier": randint(-3, -1)
        },
        "voidstone": {
            "armor_class_modifier": randint(-4, -1),
            "armor_modifier": randint(3, 6),
            "movement_energy_bonus_modifier": randint(-8, -4),
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
            "movement_energy_bonus_modifier": randint(-8, -4),
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
            "movement_energy_bonus_modifier": randint(-8, -4),
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
            "movement_energy_bonus_modifier": randint(-8, -4),
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
            "movement_energy_bonus_modifier": randint(-4, -1),
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
            "movement_energy_bonus_modifier": randint(-6, -3),
            "resistances": {
                "arcane": randint(10, 20) / 100,
            },
            "speed_modifier": randint(-5, -1),
            "intelligence_modifier": randint(0, 2)
        },
        "adamantine": {
            "armor_class_modifier": randint(0, 2),
            "armor_modifier": randint(5, 9),
            "movement_energy_bonus_modifier": randint(-9, -3),
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
            "movement_energy_bonus_modifier": randint(1, 4),
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
            "armor_class_modifier": 1,
            "armor_modifier": randint(0, 1)
        },
        "spaulders": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        "pauldrons": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": 1
        },
        "gardbraces": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": 1
        },
        "shoulderguards": {
            "armor_class_modifier": randint(2, 3),
            "armor_modifier": 1
        },
        "mantle": {
            "armor_class_modifier": randint(2, 3),
            "armor_modifier": randint(1, 2)
        },
        "epaulets": {
            "armor_class_modifier": randint(2, 4),
            "armor_modifier": randint(1, 2)
        },
        "shoulderpads": {
            "armor_class_modifier": randint(1, 5),
            "armor_modifier": randint(1, 2)
        },
        "shoulderplates": {
            "armor_class_modifier": randint(1, 5),
            "armor_modifier": randint(1, 3)
        },
        # Body armor
        "armor": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        "brigandine": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": 1
        },
        "cuirass": {
            "armor_class_modifier": randint(0, 3),
            "armor_modifier": randint(1, 2),
            "speed_modifier": randint(-3, -1),
        },
        "ring mail": {
            "armor_class_modifier": randint(-1, 1),
            "armor_modifier": 2,
            "speed_modifier": randint(-2, 0),
            "movement_energy_bonus_modifier": randint(-3, -2)
        },
        "hauberk": {
            "armor_class_modifier": randint(-2, 0),
            "armor_modifier": randint(2, 3),
            "speed_modifier": randint(-2, 0),
            "movement_energy_bonus_modifier": randint(-5, -2)
        },
        "light plate": {
            "armor_class_modifier": randint(-2, 1),
            "armor_modifier": randint(2, 3),
            "speed_modifier": randint(-3, 0),
            "movement_energy_bonus_modifier": randint(-6, -2)
        },
        "mail": {
            "armor_class_modifier": randint(0, 2),
            "armor_modifier": randint(2, 4),
            "speed_modifier": randint(-3, 0),
            "movement_energy_bonus_modifier": randint(-6, -3)
        },
        "plate": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": 3,
            "speed_modifier": randint(-4, -1),
            "movement_energy_bonus_modifier": randint(-7, -3)
        },
        "splint mail": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(3, 4),
            "speed_modifier": randint(-5, -1),
            "movement_energy_bonus_modifier": randint(-7, -4)
        },
        "plate mail": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(3, 5),
            "speed_modifier": randint(-5, -2),
            "movement_energy_bonus_modifier": randint(-8, -4)
        },
        "breastplate": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": 4,
            "speed_modifier": randint(-6, -2),
            "movement_energy_bonus_modifier": randint(-9, -4)
        },
        "faulds": {
            "armor_class_modifier": randint(-1, 2),
            "armor_modifier": randint(4, 5),
            "speed_modifier": randint(-6, -3),
            "movement_energy_bonus_modifier": randint(-9, -5)
        },
        "culet": {
            "armor_class_modifier": randint(-5, -2),
            "armor_modifier": randint(4, 6),
            "speed_modifier": randint(-6, -3),
            "movement_energy_bonus_modifier": randint(-10, -5)
        },
        "plackart": {
            "armor_class_modifier": randint(-7, -4),
            "armor_modifier": randint(4, 7),
            "speed_modifier": randint(-7, -3),
            "movement_energy_bonus_modifier": randint(-11, -5)
        },
        "full plate mail": {
            "armor_class_modifier": randint(-8, -4),
            "armor_modifier": randint(5, 8),
            "speed_modifier": randint(-8, -4),
            "movement_energy_bonus_modifier": randint(-12, -6)
        },
        # Leg armor
        "greaves": {
            "armor_class_modifier": randint(0, 1),
            "armor_modifier": randint(0, 1),
            "speed_modifier": randint(-1, 1),
            "movement_energy_bonus_modifier": randint(0, 3)
        },
        "tassets": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": randint(0, 1),
            "speed_modifier": randint(-2, 2),
            "movement_energy_bonus_modifier": 2
        },
        "leg guards": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": 1,
            "speed_modifier": randint(-3, 3),
            "movement_energy_bonus_modifier": randint(2, 5)
        },
        "chausses": {
            "armor_class_modifier": randint(1, 4),
            "armor_modifier": randint(1, 2),
            "speed_modifier": randint(-4, 3),
            "movement_energy_bonus_modifier": randint(-3, 3)
        },
        "cuisses": {
            "armor_class_modifier": randint(1, 4),
            "armor_modifier": 2,
            "speed_modifier": randint(-5, 2),
            "movement_energy_bonus_modifier": randint(-4, 2)
        },
        "poleyns": {
            "armor_class_modifier": randint(2, 4),
            "armor_modifier": randint(2, 3),
            "speed_modifier": randint(-6, 1),
            "movement_energy_bonus_modifier": randint(-5, 1)
        },
        # Wrist armor
        "bracers": {
            "armor_class_modifier": randint(0, 1),
            "armor_modifier": randint(0, 1),
            "attack_energy_bonus_modifier": randint(-5, 0)
        },
        "rerebraces": {
            "armor_class_modifier": randint(0, 2),
            "armor_modifier": randint(0, 1),
            "attack_energy_bonus_modifier": randint(-6, 0)
        },
        "bracers": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": 1,
            "attack_energy_bonus_modifier": randint(-7, 0)
        },
        "vambraces": {
            "armor_class_modifier": randint(2, 3),
            "armor_modifier": randint(1, 2),
            "attack_energy_bonus_modifier": randint(-8, 0)
        },
        # Hand armor
        "gloves": {
            "armor_class_modifier": randint(0, 1),
            "attack_energy_bonus_modifier": randint(1, 2)
        },
        "grips": {
            "armor_class_modifier": randint(0, 1),
            "armor_modifier": randint(0, 1),
            "attack_energy_bonus_modifier": randint(0, 3)
        },
        "handguards": {
            "armor_class_modifier": randint(1, 2),
            "armor_modifier": 1,
            "attack_energy_bonus_modifier": randint(1, 4)
        },
        "gauntlets": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(1, 2),
            "attack_energy_bonus_modifier": randint(1, 5)
        },
        # Boots
        "footwear": {
            "armor_class_modifier": randint(0, 1),
            "armor_modifier": randint(0, 1),
            "movement_energy_bonus_modifier": randint(1, 2)
        },
        "boots": {
            "armor_class_modifier": randint(0, 2),
            "armor_modifier": randint(0, 1),
            "movement_energy_bonus_modifier": randint(1, 3)
        },
        "footpads": {
            "armor_class_modifier": randint(0, 2),
            "armor_modifier": randint(0, 1),
            "movement_energy_bonus_modifier": randint(2, 4)
        },
        "sandals": {
            "movement_energy_bonus_modifier": randint(1, 5)
        },
        "sabatons": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": 1,
            "movement_energy_bonus_modifier": randint(0, 4)
        },
        "treads": {
            "armor_class_modifier": randint(1, 3),
            "armor_modifier": randint(1, 2),
            "movement_energy_bonus_modifier": randint(0, 3)
        },
        "warboots": {
            "armor_class_modifier": randint(2, 3),
            "armor_modifier": randint(1, 3),
            "movement_energy_bonus_modifier": randint(0, 2)
        },
        # Shields
        "guige": {
            "shield_armor_class": 1,
        },
        "buckler": {
            "shield_armor_class": randint(1, 2),
        },
        "small shield": {
            "shield_armor_class": randint(1, 2),
            "armor_modifier": randint(0, 1)
        },
        "shield": {
            "shield_armor_class": randint(1, 3),
            "armor_modifier": 1
        },
        "round shield": {
            "shield_armor_class": randint(2, 3),
            "armor_modifier": 1
        },
        "large shield": {
            "shield_armor_class": randint(2, 4),
            "armor_modifier": randint(1, 2)
        },
        "war shield": {
            "shield_armor_class": randint(2, 5),
            "armor_modifier": randint(1, 2)
        },
        "bulwark": {
            "shield_armor_class": randint(2, 5),
            "armor_modifier": randint(1, 3)
        },
        "enarmes": {
            "shield_armor_class": randint(3, 5),
            "armor_modifier": 2,
            "resistances": {
                "physical": randint(1, 3) / 100
            }
        },
        "heater shield": {
            "shield_armor_class": randint(2, 6),
            "armor_modifier": randint(1, 2),
            "resistances": {
                "physical": randint(1, 4) / 100
            }
        },
        "kite shield": {
            "shield_armor_class": randint(2, 6),
            "armor_modifier": 2,
            "resistances": {
                "physical": randint(1, 5) / 100
            }
        },
        "rondache": {
            "shield_armor_class": randint(1, 7),
            "armor_modifier": randint(2, 3),
            "resistances": {
                "physical": randint(1, 6) / 100
            }
        },
        "targe": {
            "shield_armor_class": randint(1, 8),
            "armor_modifier": randint(2, 4),
            "resistances": {
                "physical": randint(1, 7) / 100
            }
        },
        "tower shield": {
            "shield_armor_class": randint(3, 8),
            "armor_modifier": randint(2, 5),
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
    "HEAD": 0x100A,
    "SHOULDERS": 0x1011,
    "TORSO": 0x100B,
    "LEGS": 0x100F,
    "WRISTS": 0x1010,
    "GLOVES": 0x100E,
    "BOOTS": 0x100D,
    "OFF_HAND": 0x100C
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
    material = ''.join(
        choices(armor_material_names, armor_material_weights, k=1))
    rarity_level = ''.join(
        choices(rarities["rarity_levels"], rarities["rarity_weights"], k=1))
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
        "rarity_color": rarities["rarity_colors"][rarity_level]
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
        modifier_count = rarities["rarity_modifier_counts"][rarity_level]
        rarity_modifier_sample = sample(possible_rarity_modifiers,
                                        modifier_count)
        rarity_modifiers = {}
        for modifier in rarity_modifier_sample:
            for modifier_name in modifier.keys():
                rarity_modifiers.update(
                    {modifier_name: modifier[modifier_name]})
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
        "melee_chance_to_hit_modifier": 0,
        "ranged_chance_to_hit_modifier": 0,
        "armor_modifier": 0,
        "armor_class_modifier": 0,
        "dodge_modifier": 0,
        "shield_armor_class": 0,
        "max_hp_modifier": 0,
        "speed_modifier": 0,
        "movement_energy_bonus_modifier": 0,
        "attack_energy_bonus_modifier": 0,
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
                    if "damage_dice" in modifier_name:
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

    equippable_component = Equippable(random_armor, slot)

    for modifier_name, modifier_value in combined_modifiers.items():
        setattr(equippable_component, modifier_name, modifier_value)

    new_armor = Entity(0,
                       0,
                       armor_characters[slot._name_],
                       random_armor.unidentified_name,
                       equippable=equippable_component)

    return new_armor
