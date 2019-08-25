import tcod as libtcod
from components.equippable import Equippable
from components.equipment_attributes import qualities, quality_weights, rarities, weapon_metal_material_names, weapon_metal_material_weights, weapon_wood_material_names, weapon_wood_material_weights, weapon_prefixes, weapon_prefix_weights, weapon_suffixes, weapon_suffix_weights
from components.status_effects import ApplyDecayP50OnAttack, Regeneration, ApplyArmorPierce25OnAttack, ApplyArmorPierce50OnAttack, OnCriticalApplyPhysicalDamage25
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


def generate_melee_weapon_rarity_modifiers():
    weapon_rarity_modifiers = {
        "common": [{
            "armor_class_modifier": randint(1, 1)
        }, {
            "max_hp_modifier": randint(1, 3)
        }, {
            "melee_chance_to_hit_modifier": randint(1, 2)
        }, {
            "speed_modifier": randint(1, 3)
        }, {
            "movement_energy_bonus_modifier": randint(1, 2)
        }, {
            "melee_attack_energy_bonus_modifier": randint(1, 2)
        }],
        "uncommon": [{
            "armor_class_modifier": randint(1, 2)
        }, {
            "max_hp_modifier": randint(1, 4)
        }, {
            "melee_chance_to_hit_modifier": randint(1, 3)
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
            "armor_class_modifier": randint(1, 3)
        }, {
            "max_hp_modifier": randint(1, 5)
        }, {
            "melee_chance_to_hit_modifier": randint(1, 4)
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
            "armor_class_modifier": randint(2, 4)
        }, {
            "max_hp_modifier": randint(2, 6)
        }, {
            "melee_chance_to_hit_modifier": randint(2, 5)
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
            "armor_class_modifier": randint(3, 6)
        }, {
            "max_hp_modifier": randint(3, 8)
        }, {
            "melee_chance_to_hit_modifier": randint(3, 6)
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


def generate_ranged_weapon_rarity_modifiers():
    weapon_rarity_modifiers = {
        "common": [{
            "armor_class_modifier": randint(1, 2)
        }, {
            "max_hp_modifier": randint(1, 3)
        }, {
            "ranged_chance_to_hit_modifier": randint(1, 2)
        }, {
            "speed_modifier": randint(1, 3)
        }, {
            "movement_energy_bonus_modifier": randint(1, 2)
        }, {
            "ranged_attack_energy_bonus_modifier": randint(1, 2)
        }],
        "uncommon": [{
            "armor_class_modifier": randint(1, 2)
        }, {
            "max_hp_modifier": randint(1, 4)
        }, {
            "ranged_chance_to_hit_modifier": randint(1, 3)
        }, {
            "speed_modifier": randint(1, 4)
        }, {
            "movement_energy_bonus_modifier": randint(1, 3)
        }, {
            "ranged_attack_energy_bonus_modifier": randint(1, 3)
        }, {
            "resistances": {
                "physical": randint(1, 3) / 100
            }
        }],
        "rare": [{
            "armor_class_modifier": randint(1, 3)
        }, {
            "max_hp_modifier": randint(1, 5)
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
            "ranged_attack_energy_bonus_modifier": randint(1, 4)
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
            "armor_class_modifier": randint(2, 4)
        }, {
            "max_hp_modifier": randint(2, 6)
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
            "ranged_attack_energy_bonus_modifier": randint(2, 5)
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
            "armor_class_modifier": randint(3, 6)
        }, {
            "max_hp_modifier": randint(3, 8)
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
            "ranged_attack_energy_bonus_modifier": randint(2, 6)
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
                "physical": randint(0, 1),
            }
        },
        "bronze": {
            "melee_chance_to_hit_modifier": randint(0, 1),
            "melee_damage_modifiers": {
                "physical": randint(0, 1),
            }
        },
        "iron": {
            "melee_chance_to_hit_modifier": randint(0, 1),
            "melee_damage_modifiers": {
                "physical": 1,
            }
        },
        "steel": {
            "melee_chance_to_hit_modifier": randint(0, 2),
            "melee_damage_modifiers": {
                "physical": randint(1, 2),
            }
        },
        "truesteel": {
            "melee_chance_to_hit_modifier": randint(1, 3),
            "melee_damage_modifiers": {
                "physical": randint(1, 2),
            },
            "melee_damage_dice_modifiers": {
                "physical": [[0, 2]]
            },
            "critical_hit_chance_modifier": randint(1, 3) / 100,
            "critical_hit_damage_multiplier_modifier": randint(5, 10) / 100
        },
        "darksteel": {
            "melee_chance_to_hit_modifier": randint(-4, 1),
            "melee_damage_modifiers": {
                "physical": randint(2, 6),
            },
            "melee_damage_dice_modifiers": {
                "physical": [[2, 0]]
            }
        },
        "orichalcum": {
            "melee_chance_to_hit_modifier": randint(-1, 2),
            "melee_damage_modifiers": {
                "physical": randint(1, 4),
            },
            "melee_damage_dice_modifiers": {
                "physical": [[0, 4]]
            }
        },
        "mithril": {
            "melee_chance_to_hit_modifier": randint(1, 4),
            "melee_damage_modifiers": {
                "physical": randint(2, 4),
            },
            "melee_damage_dice_modifiers": {
                "physical": [[1, 0]]
            }
        },
        "voidstone": {
            "melee_chance_to_hit_modifier": randint(1, 2),
            "melee_damage_modifiers": {
                "chaos": randint(1, 4),
            },
            "melee_damage_dice_modifiers": {
                "chaos": [[1, 2]]
            },
            "resistances": {
                "chaos": randint(1, 5) / 100
            }
        },
        "brimstone": {
            "melee_chance_to_hit_modifier": randint(1, 2),
            "melee_damage_modifiers": {
                "fire": randint(1, 4),
            },
            "melee_damage_dice_modifiers": {
                "fire": [[1, 2]]
            },
            "resistances": {
                "fire": randint(1, 5) / 100
            }
        },
        "cold iron": {
            "melee_chance_to_hit_modifier": randint(1, 2),
            "melee_damage_modifiers": {
                "ice": randint(1, 4),
            },
            "melee_damage_dice_modifiers": {
                "ice": [[1, 2]]
            },
            "resistances": {
                "ice": randint(1, 5) / 100
            }
        },
        "thunderstone": {
            "melee_chance_to_hit_modifier": randint(1, 2),
            "melee_damage_modifiers": {
                "lightning": randint(1, 4),
            },
            "melee_damage_dice_modifiers": {
                "lightning": [[1, 2]]
            },
            "resistances": {
                "lightning": randint(1, 5) / 100
            }
        },
        "pearlstone": {
            "melee_chance_to_hit_modifier": randint(1, 2),
            "melee_damage_modifiers": {
                "holy": randint(1, 4),
            },
            "melee_damage_dice_modifiers": {
                "holy": [[1, 2]]
            },
            "resistances": {
                "holy": randint(1, 5) / 100
            }
        },
        "electrum": {
            "melee_chance_to_hit_modifier": randint(1, 2),
            "melee_damage_modifiers": {
                "arcane": randint(1, 4),
            },
            "melee_damage_dice_modifiers": {
                "arcane": [[1, 2]]
            },
            "resistances": {
                "arcane": randint(1, 5) / 100
            }
        },
        "adamantine": {
            "melee_chance_to_hit_modifier": randint(-1, 1),
            "melee_damage_modifiers": {
                "physical": randint(4, 8),
            },
            "melee_damage_dice_modifiers": {
                "physical": [[3, 0]]
            }
        },
        "meteoric iron": {
            "melee_chance_to_hit_modifier": randint(0, 5),
            "melee_damage_modifiers": {
                "physical": randint(1, 3),
            },
            "melee_damage_dice_modifiers": {
                "physical": [[2, 2]]
            }
        },
    }
    return melee_weapon_material_modifiers


def generate_pistol_and_rifle_material_modifiers():
    pistol_and_rifle_material_modifiers = {
        "copper": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(0, 1),
            }
        },
        "bronze": {
            "ranged_chance_to_hit_modifier": randint(0, 1),
            "ranged_damage_modifiers": {
                "physical": randint(0, 1),
            }
        },
        "iron": {
            "ranged_chance_to_hit_modifier": randint(0, 1),
            "ranged_damage_modifiers": {
                "physical": 1,
            }
        },
        "steel": {
            "ranged_chance_to_hit_modifier": randint(0, 2),
            "ranged_damage_modifiers": {
                "physical": randint(1, 2),
            }
        },
        "truesteel": {
            "ranged_chance_to_hit_modifier": randint(1, 3),
            "ranged_damage_modifiers": {
                "physical": randint(1, 2),
            },
            "ranged_damage_dice_modifiers": {
                "physical": [[0, 2]]
            },
            "critical_hit_chance_modifier": randint(1, 3) / 100,
            "critical_hit_damage_multiplier_modifier": randint(5, 10) / 100
        },
        "darksteel": {
            "ranged_chance_to_hit_modifier": randint(-4, 1),
            "ranged_damage_modifiers": {
                "physical": randint(2, 6),
            },
            "ranged_damage_dice_modifiers": {
                "physical": [[2, 0]]
            }
        },
        "orichalcum": {
            "ranged_chance_to_hit_modifier": randint(-1, 2),
            "ranged_damage_modifiers": {
                "physical": randint(1, 4),
            },
            "ranged_damage_dice_modifiers": {
                "physical": [[0, 4]]
            }
        },
        "mithril": {
            "ranged_chance_to_hit_modifier": randint(1, 4),
            "ranged_damage_modifiers": {
                "physical": randint(2, 4),
            },
            "ranged_damage_dice_modifiers": {
                "physical": [[1, 0]]
            }
        },
        "voidstone": {
            "ranged_chance_to_hit_modifier": randint(1, 2),
            "ranged_damage_modifiers": {
                "chaos": randint(1, 4),
            },
            "ranged_damage_dice_modifiers": {
                "chaos": [[1, 2]]
            },
            "resistances": {
                "chaos": randint(1, 5) / 100
            }
        },
        "brimstone": {
            "ranged_chance_to_hit_modifier": randint(1, 2),
            "ranged_damage_modifiers": {
                "fire": randint(1, 4),
            },
            "ranged_damage_dice_modifiers": {
                "fire": [[1, 2]]
            },
            "resistances": {
                "fire": randint(1, 5) / 100
            }
        },
        "cold iron": {
            "ranged_chance_to_hit_modifier": randint(1, 2),
            "ranged_damage_modifiers": {
                "ice": randint(1, 4),
            },
            "ranged_damage_dice_modifiers": {
                "ice": [[1, 2]]
            },
            "resistances": {
                "ice": randint(1, 5) / 100
            }
        },
        "thunderstone": {
            "ranged_chance_to_hit_modifier": randint(1, 2),
            "ranged_damage_modifiers": {
                "lightning": randint(1, 4),
            },
            "ranged_damage_dice_modifiers": {
                "lightning": [[1, 2]]
            },
            "resistances": {
                "lightning": randint(1, 5) / 100
            }
        },
        "pearlstone": {
            "ranged_chance_to_hit_modifier": randint(1, 2),
            "ranged_damage_modifiers": {
                "holy": randint(1, 4),
            },
            "ranged_damage_dice_modifiers": {
                "holy": [[1, 2]]
            },
            "resistances": {
                "holy": randint(1, 5) / 100
            }
        },
        "electrum": {
            "ranged_chance_to_hit_modifier": randint(1, 2),
            "ranged_damage_modifiers": {
                "arcane": randint(1, 4),
            },
            "ranged_damage_dice_modifiers": {
                "arcane": [[1, 2]]
            },
            "resistances": {
                "arcane": randint(1, 5) / 100
            }
        },
        "adamantine": {
            "ranged_chance_to_hit_modifier": randint(-1, 1),
            "ranged_damage_modifiers": {
                "physical": randint(4, 8),
            },
            "ranged_damage_dice_modifiers": {
                "physical": [[3, 0]]
            }
        },
        "meteoric iron": {
            "ranged_chance_to_hit_modifier": randint(0, 5),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3),
            },
            "ranged_damage_dice_modifiers": {
                "physical": [[2, 2]]
            }
        },
    }
    return pistol_and_rifle_material_modifiers


def generate_bow_and_crossbow_material_modifiers():
    bow_and_crossbow_material_modifiers = {
        "maple": {
            "ranged_chance_to_hit_modifier": randint(0, 1),
            "ranged_damage_modifiers": {
                "physical": randint(0, 1)
            }
        },
        "ash": {
            "ranged_chance_to_hit_modifier": randint(0, 2),
            "ranged_damage_modifiers": {
                "physical": randint(0, 1)
            }
        },
        "elm": {
            "ranged_chance_to_hit_modifier": randint(1, 2),
            "ranged_damage_modifiers": {
                "physical": randint(0, 1)
            }
        },
        "oak": {
            "ranged_chance_to_hit_modifier": randint(1, 3),
            "ranged_damage_modifiers": {
                "physical": randint(0, 2)
            }
        },
        "hickory": {
            "ranged_chance_to_hit_modifier": randint(1, 3),
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "walnut": {
            "ranged_chance_to_hit_modifier": randint(1, 3),
            "ranged_damage_modifiers": {
                "physical": randint(2, 3)
            }
        },
        "ironwood": {
            "ranged_chance_to_hit_modifier": randint(1, 3),
            "ranged_damage_modifiers": {
                "physical": randint(2, 3)
            },
            "ranged_damage_dice_modifiers": {
                "physical": [[0, 2]]
            }
        },
        "rosewood": {
            "ranged_chance_to_hit_modifier": randint(1, 3),
            "ranged_damage_modifiers": {
                "physical": randint(2, 3)
            },
            "ranged_damage_dice_modifiers": {
                "physical": [[0, 4]]
            }
        },
        "juniper": {
            "ranged_chance_to_hit_modifier": randint(2, 4),
            "ranged_damage_modifiers": {
                "physical": randint(2, 4)
            },
            "ranged_damage_dice_modifiers": {
                "physical": [[1, 2]]
            }
        },
        "yew": {
            "ranged_chance_to_hit_modifier": randint(2, 6),
            "ranged_damage_modifiers": {
                "physical": randint(2, 6)
            },
            "ranged_damage_dice_modifiers": {
                "physical": [[2, 2]]
            }
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
            "trident",
            "spetum",
            "brandistock",
            "guisarme",
            "glaive",
            "partisan",
            "lochaber axe",
            "war scythe",
            "pike",
            "lance",
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
            0.065,
            0.06,
            0.055,
            0.05,
            0.045,
            0.04,
            0.035,
            0.03,
            0.025,
            0.02,
            0.01,
        ]
    },
    "spear": {
        "names": [
            "shortspear",
            "spear",
            "javelin",
            "pilum",
            "harpoon",
            "fuscina",
            "longspear",
            "war spear",
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
    "long knife": "slashing",
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
    "trident": "piercing",
    "guisarme": "piercing",
    "glaive": "slashing",
    "partisan": "slashing",
    "lochaber axe": "slashing",
    "war scythe": "slashing",
    "shortspear": "piercing",
    "spear": "piercing",
    "longspear": "piercing",
    "pike": "piercing",
    "harpoon": "piercing",
    "javelin": "piercing",
    "fuscina": "piercing",
    "pilum": "piercing",
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
    "long knife": 0.07,
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
    "trident": 0.11,
    "lochaber axe": 0.13,
    "war scythe": 0.18,
    "shortspear": 0.08,
    "spear": 0.09,
    "longspear": 0.1,
    "javelin": 0.07,
    "pilum": 0.09,
    "harpoon": 0.15,
    "fuscina": 0.11,
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
                "physical": [[1, 7]]
            }
        },
        "longsword": {
            "melee_damage_dice": {
                "physical": [[1, 8]]
            }
        },
        "bastard sword": {
            "melee_damage_dice": {
                "physical": [[1, 10]]
            }
        },
        "scimitar": {
            "melee_damage_dice": {
                "physical": [[1, 8]]
            },
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "falchion": {
            "melee_damage_dice": {
                "physical": [[1, 9]]
            }
        },
        "gladius": {
            "melee_chance_to_hit_modifier": 1,
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "arming sword": {
            "melee_chance_to_hit_modifier": randint(1, 2),
            "melee_damage_dice": {
                "physical": [[1, 8]]
            },
            "melee_damage_modifiers": {
                "physical": randint(1, 2)
            }
        },
        "sabre": {
            "melee_chance_to_hit_modifier": randint(1, 3),
            "melee_damage_dice": {
                "physical": [[1, 7]]
            },
            "melee_damage_modifiers": {
                "physical": randint(0, 2)
            }
        },
        "estoc": {
            "melee_chance_to_hit_modifier": randint(1, 2),
            "melee_damage_dice": {
                "physical": [[1, 7]]
            },
            "melee_damage_modifiers": {
                "physical": randint(1, 2)
            }
        },
        "rapier": {
            "melee_chance_to_hit_modifier": randint(2, 3),
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_attack_energy_bonus_modifier": randint(2, 4)
        },
        "fencing sword": {
            "melee_chance_to_hit_modifier": 1,
            "melee_damage_dice": {
                "physical": [[1, 8]]
            },
            "melee_attack_energy_bonus_modifier": randint(3, 6),
            "melee_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "hand axe": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_chance_to_hit_modifier": -1,
            "critical_hit_damage_multiplier_modifier": 1 / 100
        },
        "axe": {
            "melee_damage_dice": {
                "physical": [[1, 7]]
            },
            "melee_chance_to_hit_modifier": randint(-1, 0),
            "critical_hit_damage_multiplier_modifier": randint(1, 2) / 100
        },
        "double axe": {
            "melee_damage_dice": {
                "physical": [[1, 8]]
            },
            "melee_chance_to_hit_modifier": randint(-2, 0),
            "critical_hit_damage_multiplier_modifier": randint(1, 3) / 100,
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "war axe": {
            "melee_damage_dice": {
                "physical": [[1, 9]]
            },
            "melee_chance_to_hit_modifier": randint(-2, 0),
            "critical_hit_damage_multiplier_modifier": randint(1, 4) / 100,
            "melee_damage_modifiers": {
                "physical": randint(1, 2)
            }
        },
        "military pick": {
            "melee_damage_dice": {
                "physical": [[1, 7]]
            },
            "melee_chance_to_hit_modifier": randint(-2, 0),
            "critical_hit_damage_multiplier_modifier": randint(2, 3) / 100,
            "melee_damage_modifiers": {
                "physical": randint(0, 2)
            }
        },
        "war pick": {
            "melee_damage_dice": {
                "physical": [[1, 8]]
            },
            "melee_chance_to_hit_modifier": randint(-2, 0),
            "critical_hit_damage_multiplier_modifier": randint(2, 4) / 100,
            "melee_damage_modifiers": {
                "physical": randint(0, 3)
            }
        },
        "battleaxe": {
            "melee_damage_dice": {
                "physical": [[1, 8]]
            },
            "melee_chance_to_hit_modifier": randint(-3, 0),
            "critical_hit_damage_multiplier_modifier": randint(2, 5) / 100,
            "melee_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "broadaxe": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_chance_to_hit_modifier": randint(-1, 0),
            "critical_hit_damage_multiplier_modifier": randint(2, 6) / 100,
            "melee_damage_modifiers": {
                "physical": randint(2, 3)
            }
        },
        "hatchet": {
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_chance_to_hit_modifier": randint(-2, 0),
            "critical_hit_damage_multiplier_modifier": randint(1, 6) / 100,
            "melee_damage_modifiers": {
                "physical": randint(1, 2)
            }
        },
        "cleaver": {
            "melee_damage_dice": {
                "physical": [[1, 7]]
            },
            "melee_chance_to_hit_modifier": randint(-3, 0),
            "critical_hit_damage_multiplier_modifier": randint(1, 8) / 100,
            "melee_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "bearded axe": {
            "melee_damage_dice": {
                "physical": [[1, 8]]
            },
            "melee_chance_to_hit_modifier": randint(-1, 0),
            "critical_hit_damage_multiplier_modifier": randint(1, 10) / 100,
            "melee_damage_modifiers": {
                "physical": randint(2, 3)
            }
        },
        "knife": {
            "melee_chance_to_hit_modifier": 1,
            "melee_damage_dice": {
                "physical": [[1, 3]]
            },
            "melee_attack_energy_bonus_modifier": randint(1, 2)
        },
        "long knife": {
            "melee_chance_to_hit_modifier": 1,
            "melee_damage_dice": {
                "physical": [[1, 3]]
            },
            "melee_damage_modifiers": {
                "physical": randint(0, 1)
            },
            "melee_attack_energy_bonus_modifier": randint(1, 3)
        },
        "dagger": {
            "melee_chance_to_hit_modifier": randint(1, 2),
            "melee_damage_dice": {
                "physical": [[1, 4]]
            },
            "melee_attack_energy_bonus_modifier": randint(1, 3)
        },
        "dirk": {
            "melee_chance_to_hit_modifier": randint(1, 3),
            "melee_damage_dice": {
                "physical": [[1, 5]]
            },
            "melee_attack_energy_bonus_modifier": randint(1, 4)
        },
        "kris": {
            "melee_chance_to_hit_modifier": randint(2, 3),
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_attack_energy_bonus_modifier": randint(1, 5)
        },
        "rondel dagger": {
            "melee_chance_to_hit_modifier": randint(2, 3),
            "melee_damage_dice": {
                "physical": [[1, 7]]
            },
            "melee_attack_energy_bonus_modifier": randint(2, 4)
        },
        "hunting dagger": {
            "melee_chance_to_hit_modifier": randint(0, 1),
            "melee_damage_dice": {
                "physical": [[2, 2]]
            },
            "melee_attack_energy_bonus_modifier": randint(2, 5)
        },
        "blade": {
            "melee_chance_to_hit_modifier": randint(0, 2),
            "melee_damage_dice": {
                "physical": [[2, 2]]
            },
            "melee_attack_energy_bonus_modifier": randint(2, 6)
        },
        "stiletto": {
            "melee_chance_to_hit_modifier": randint(1, 4),
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_attack_energy_bonus_modifier": randint(3, 8),
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "light mace": {
            "melee_chance_to_hit_modifier": randint(-1, 0),
            "melee_damage_dice": {
                "physical": [[2, 2]]
            },
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "mace": {
            "melee_chance_to_hit_modifier": randint(-2, 0),
            "melee_damage_dice": {
                "physical": [[3, 2]]
            },
            "melee_damage_modifiers": {
                "physical": randint(1, 2)
            }
        },
        "ball mace": {
            "melee_chance_to_hit_modifier": randint(-2, 0),
            "melee_damage_dice": {
                "physical": [[2, 3]]
            },
            "melee_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "heavy mace": {
            "melee_chance_to_hit_modifier": randint(-3, 0),
            "melee_damage_dice": {
                "physical": [[2, 4]]
            },
            "melee_damage_modifiers": {
                "physical": randint(1, 4)
            }
        },
        "morning star": {
            "melee_chance_to_hit_modifier": randint(-3, 0),
            "melee_damage_dice": {
                "physical": [[3, 3]]
            },
            "melee_damage_modifiers": {
                "physical": randint(2, 3)
            }
        },
        "light flail": {
            "melee_chance_to_hit_modifier": randint(-3, 0),
            "melee_damage_dice": {
                "physical": [[2, 5]]
            },
            "melee_damage_modifiers": {
                "physical": randint(2, 3)
            }
        },
        "flail": {
            "melee_chance_to_hit_modifier": randint(-4, 0),
            "melee_damage_dice": {
                "physical": [[2, 6]]
            },
            "melee_damage_modifiers": {
                "physical": randint(2, 4)
            }
        },
        "flanged mace": {
            "melee_chance_to_hit_modifier": randint(-2, 0),
            "melee_damage_dice": {
                "physical": [[3, 3]]
            },
            "melee_damage_modifiers": {
                "physical": randint(2, 3)
            }
        },
        "bladed mace": {
            "melee_chance_to_hit_modifier": randint(-3, 0),
            "melee_damage_dice": {
                "physical": [[3, 3]]
            },
            "melee_damage_modifiers": {
                "physical": randint(2, 4)
            },
            "critical_hit_chance_modifier": 1 / 100
        },
        "mallet": {
            "melee_chance_to_hit_modifier": randint(-1, 0),
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "club": {
            "melee_chance_to_hit_modifier": randint(-1, 0),
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "cudgel": {
            "melee_chance_to_hit_modifier": randint(-1, 0),
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "bludgeon": {
            "melee_chance_to_hit_modifier": randint(-1, 0),
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "truncheon": {
            "melee_chance_to_hit_modifier": randint(-1, 0),
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "war club": {
            "melee_chance_to_hit_modifier": randint(-1, 0),
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "heavy cudgel": {
            "melee_chance_to_hit_modifier": randint(-1, 0),
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "light hammer": {
            "melee_chance_to_hit_modifier": randint(-1, 0),
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "hammer": {
            "melee_chance_to_hit_modifier": randint(-1, 0),
            "melee_damage_dice": {
                "physical": [[1, 7]]
            },
            "melee_damage_modifiers": {
                "physical": randint(1, 2)
            }
        },
        "war hammer": {
            "melee_chance_to_hit_modifier": -1,
            "melee_damage_dice": {
                "physical": [[1, 8]]
            },
            "melee_damage_modifiers": {
                "physical": 2
            }
        },
        "battle hammer": {
            "melee_chance_to_hit_modifier": -2,
            "melee_damage_dice": {
                "physical": [[1, 9]]
            },
            "melee_damage_modifiers": {
                "physical": randint(2, 3)
            }
        },
        "large hammer": {
            "melee_chance_to_hit_modifier": -3,
            "melee_damage_dice": {
                "physical": [[1, 10]]
            },
            "melee_damage_modifiers": {
                "physical": 3
            }
        },
        "short staff": {
            "melee_chance_to_hit_modifier": -1,
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "staff": {
            "melee_chance_to_hit_modifier": randint(-2, -1),
            "melee_damage_dice": {
                "physical": [[1, 7]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "long staff": {
            "melee_chance_to_hit_modifier": -2,
            "melee_damage_dice": {
                "physical": [[1, 8]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "quarterstaff": {
            "melee_chance_to_hit_modifier": -2,
            "melee_damage_dice": {
                "physical": [[1, 10]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "battle staff": {
            "melee_chance_to_hit_modifier": -2,
            "melee_damage_dice": {
                "physical": [[1, 11]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "war staff": {
            "melee_chance_to_hit_modifier": randint(-3, -2),
            "melee_damage_dice": {
                "physical": [[1, 12]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "spetum": {
            "melee_chance_to_hit_modifier": -2,
            "melee_damage_dice": {
                "physical": [[1, 12]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "trident": {
            "melee_chance_to_hit_modifier": randint(-3, -2),
            "melee_damage_dice": {
                "physical": [[1, 12]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "brandistock": {
            "melee_chance_to_hit_modifier": randint(-4, -3),
            "melee_damage_dice": {
                "physical": [[1, 12]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "pike": {
            "melee_chance_to_hit_modifier": randint(-5, -4),
            "melee_damage_dice": {
                "physical": [[1, 14]]
            },
            "melee_damage_modifiers": {
                "physical": 1
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "lance": {
            "melee_chance_to_hit_modifier": -5,
            "melee_damage_dice": {
                "physical": [[1, 16]]
            },
            "melee_damage_modifiers": {
                "physical": randint(1, 2)
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "halberd": {
            "melee_chance_to_hit_modifier": -1,
            "melee_damage_dice": {
                "physical": [[1, 8]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "bardiche": {
            "melee_chance_to_hit_modifier": -1,
            "melee_damage_dice": {
                "physical": [[1, 9]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "voulge": {
            "melee_chance_to_hit_modifier": randint(-2, -1),
            "melee_damage_dice": {
                "physical": [[1, 10]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "poleaxe": {
            "melee_chance_to_hit_modifier": randint(-2, -1),
            "melee_damage_dice": {
                "physical": [[1, 11]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "fauchard": {
            "melee_chance_to_hit_modifier": -2,
            "melee_damage_dice": {
                "physical": [[1, 12]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "guisarme": {
            "melee_chance_to_hit_modifier": randint(-3, -2),
            "melee_damage_dice": {
                "physical": [[1, 12]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "glaive": {
            "melee_chance_to_hit_modifier": -3,
            "melee_damage_dice": {
                "physical": [[1, 12]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "partisan": {
            "melee_chance_to_hit_modifier": -3,
            "melee_damage_dice": {
                "physical": [[1, 13]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "lochaber axe": {
            "melee_chance_to_hit_modifier": randint(-4, -3),
            "melee_damage_dice": {
                "physical": [[1, 14]]
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "war scythe": {
            "melee_chance_to_hit_modifier": -4,
            "melee_damage_dice": {
                "physical": [[1, 14]]
            },
            "melee_damage_modifiers": {
                "physical": 1
            },
            "melee_attack_energy_bonus_modifier": -10
        },
        "shortspear": {
            "melee_chance_to_hit_modifier": randint(0, 1),
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_attack_energy_bonus_modifier": -5
        },
        "spear": {
            "melee_chance_to_hit_modifier": randint(0, 1),
            "melee_damage_dice": {
                "physical": [[1, 8]]
            },
            "melee_attack_energy_bonus_modifier": -6
        },
        "longspear": {
            "melee_chance_to_hit_modifier": 1,
            "melee_damage_dice": {
                "physical": [[1, 10]]
            },
            "melee_attack_energy_bonus_modifier": -7
        },
        "javelin": {
            "melee_chance_to_hit_modifier": randint(1, 2),
            "melee_damage_dice": {
                "physical": [[1, 6]]
            },
            "melee_attack_energy_bonus_modifier": -5
        },
        "pilum": {
            "melee_chance_to_hit_modifier": randint(1, 2),
            "melee_damage_dice": {
                "physical": [[1, 8]]
            },
            "melee_attack_energy_bonus_modifier": -6
        },
        "harpoon": {
            "melee_chance_to_hit_modifier": 1,
            "melee_damage_dice": {
                "physical": [[1, 9]]
            },
            "melee_attack_energy_bonus_modifier": -7
        },
        "fuscina": {
            "melee_chance_to_hit_modifier": 1,
            "melee_damage_dice": {
                "physical": [[1, 8]]
            },
            "melee_attack_energy_bonus_modifier": -6
        },
        "war spear": {
            "melee_chance_to_hit_modifier": randint(1, 2),
            "melee_damage_dice": {
                "physical": [[1, 8]]
            },
            "melee_attack_energy_bonus_modifier": -8
        },
        "greatsword": {
            "melee_chance_to_hit_modifier": randint(-6, -3),
            "melee_damage_dice": {
                "physical": [[2, 6]]
            },
            "melee_attack_energy_bonus_modifier": -15
        },
        "greataxe": {
            "melee_chance_to_hit_modifier": randint(-6, -3),
            "melee_damage_dice": {
                "physical": [[3, 5]]
            },
            "melee_attack_energy_bonus_modifier": -16
        },
        "claymore": {
            "melee_chance_to_hit_modifier": randint(-6, -3),
            "melee_damage_dice": {
                "physical": [[2, 8]]
            },
            "melee_attack_energy_bonus_modifier": -17
        },
        "zweihänder": {
            "melee_chance_to_hit_modifier": randint(-6, -3),
            "melee_damage_dice": {
                "physical": [[4, 5]]
            },
            "melee_attack_energy_bonus_modifier": -18
        },
        "flamberge": {
            "melee_chance_to_hit_modifier": randint(-6, -3),
            "melee_damage_dice": {
                "physical": [[3, 6]]
            },
            "melee_attack_energy_bonus_modifier": -19
        },
        "warsword": {
            "melee_chance_to_hit_modifier": randint(-6, -3),
            "melee_damage_dice": {
                "physical": [[4, 4]]
            },
            "melee_attack_energy_bonus_modifier": -20
        },
        "maul": {
            "melee_chance_to_hit_modifier": randint(-6, -3),
            "melee_damage_dice": {
                "physical": [[2, 10]]
            },
            "melee_attack_energy_bonus_modifier": -21
        },
        "heavy maul": {
            "melee_chance_to_hit_modifier": randint(-6, -3),
            "melee_damage_dice": {
                "physical": [[2, 11]]
            },
            "melee_attack_energy_bonus_modifier": -22
        },
        "two-handed hammer": {
            "melee_chance_to_hit_modifier": randint(-6, -3),
            "melee_damage_dice": {
                "physical": [[2, 12]]
            },
            "melee_attack_energy_bonus_modifier": -23
        },
        "two-handed war hammer": {
            "melee_chance_to_hit_modifier": randint(-6, -3),
            "melee_damage_dice": {
                "physical": [[3, 8]]
            },
            "melee_attack_energy_bonus_modifier": -24
        },
        "heavy flail": {
            "melee_chance_to_hit_modifier": randint(-6, -3),
            "melee_damage_dice": {
                "physical": [[5, 4]]
            },
            "melee_attack_energy_bonus_modifier": -25
        },
        "revolver": {
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            },
            "ranged_damage_modifiers": {
                "physical": randint(2, 4)
            },
            "ranged_attack_energy_bonus_modifier": 10
        },
        "repeater": {
            "ranged_damage_dice": {
                "physical": [[3, 2]]
            },
            "ranged_damage_modifiers": {
                "physical": randint(1, 5)
            },
            "ranged_attack_energy_bonus_modifier": 12
        },
        "flintlock pistol": {
            "ranged_damage_dice": {
                "physical": [[1, 8]]
            },
            "ranged_damage_modifiers": {
                "physical": randint(3, 6)
            },
            "ranged_attack_energy_bonus_modifier": 5
        },
        "howdah": {
            "ranged_damage_dice": {
                "physical": [[2, 4]]
            },
            "ranged_damage_modifiers": {
                "physical": randint(3, 7)
            },
            "ranged_attack_energy_bonus_modifier": 8
        },
        "hand cannon": {
            "ranged_damage_dice": {
                "physical": [[1, 10]]
            },
            "ranged_damage_modifiers": {
                "physical": randint(2, 8)
            },
            "ranged_attack_energy_bonus_modifier": 10
        },
        "derringer": {
            "ranged_chance_to_hit_modifier": randint(3, 5),
            "ranged_damage_dice": {
                "physical": [[2, 2]]
            },
            "ranged_damage_modifiers": {
                "physical": 1
            },
            "ranged_attack_energy_bonus_modifier": 15
        },
        "rifle": {
            "ranged_chance_to_hit_modifier": randint(1, 5),
            "ranged_damage_dice": {
                "physical": [[1, 10]]
            },
            "ranged_attack_energy_bonus_modifier": -15
        },
        "repeater carbine": {
            "ranged_chance_to_hit_modifier": randint(1, 6),
            "ranged_damage_dice": {
                "physical": [[1, 12]]
            },
            "ranged_attack_energy_bonus_modifier": -16
        },
        "flintlock rifle": {
            "ranged_chance_to_hit_modifier": randint(2, 5),
            "ranged_damage_dice": {
                "physical": [[2, 5]]
            },
            "ranged_attack_energy_bonus_modifier": -17
        },
        "musket": {
            "ranged_chance_to_hit_modifier": randint(2, 6),
            "ranged_damage_dice": {
                "physical": [[3, 5]]
            },
            "ranged_attack_energy_bonus_modifier": -18
        },
        "blunderbuss": {
            "ranged_chance_to_hit_modifier": randint(0, 3),
            "ranged_damage_dice": {
                "physical": [[6, 3]]
            },
            "ranged_attack_energy_bonus_modifier": -19
        },
        "bolt-action rifle": {
            "ranged_chance_to_hit_modifier": randint(2, 7),
            "ranged_damage_dice": {
                "physical": [[1, 14]]
            },
            "ranged_attack_energy_bonus_modifier": -20
        },
        "repeating rifle": {
            "ranged_chance_to_hit_modifier": randint(1, 4),
            "ranged_damage_dice": {
                "physical": [[1, 16]]
            },
            "ranged_attack_damage_modifiers": {
                "physical": randint(1, 2)
            },
            "ranged_attack_energy_bonus_modifier": -22
        },
        "carbine": {
            "ranged_chance_to_hit_modifier": randint(2, 6),
            "ranged_damage_dice": {
                "physical": [[1, 18]]
            },
            "ranged_attack_energy_bonus_modifier": -24
        },
        "assault carbine": {
            "ranged_chance_to_hit_modifier": randint(1, 5),
            "ranged_damage_dice": {
                "physical": [[4, 6]]
            },
            "ranged_attack_energy_bonus_modifier": -25
        },
        "revolver rifle": {
            "ranged_chance_to_hit_modifier": randint(1, 4),
            "ranged_damage_dice": {
                "physical": [[5, 6]]
            },
            "ranged_attack_energy_bonus_modifier": -25
        },
        "shortbow": {
            "ranged_chance_to_hit_modifier": 1,
            "ranged_damage_dice": {
                "physical": [[1, 6]]
            },
            "ranged_damage_modifiers": {
                "physical": 1
            }
        },
        "bow": {
            "ranged_chance_to_hit_modifier": randint(1, 2),
            "ranged_damage_dice": {
                "physical": [[1, 8]]
            },
            "ranged_damage_modifiers": {
                "physical": randint(1, 2)
            }
        },
        "hunting bow": {
            "ranged_chance_to_hit_modifier": 2,
            "ranged_damage_dice": {
                "physical": [[1, 8]]
            },
            "ranged_damage_modifiers": {
                "physical": 2
            }
        },
        "composite bow": {
            "ranged_chance_to_hit_modifier": randint(2, 3),
            "ranged_damage_dice": {
                "physical": [[1, 10]]
            },
            "ranged_damage_modifiers": {
                "physical": randint(1, 3)
            }
        },
        "longbow": {
            "ranged_chance_to_hit_modifier": randint(2, 4),
            "ranged_damage_dice": {
                "physical": [[1, 12]]
            },
            "ranged_damage_modifiers": {
                "physical": 3
            }
        },
        "recurve bow": {
            "ranged_chance_to_hit_modifier": randint(2, 5),
            "ranged_damage_dice": {
                "physical": [[1, 12]]
            },
            "ranged_damage_modifiers": {
                "physical": randint(2, 4)
            }
        },
        "war bow": {
            "ranged_chance_to_hit_modifier": randint(2, 6),
            "ranged_damage_dice": {
                "physical": [[1, 14]]
            },
            "ranged_damage_modifiers": {
                "physical": randint(2, 5)
            }
        },
        "siege bow": {
            "ranged_chance_to_hit_modifier": 5,
            "ranged_damage_dice": {
                "physical": [[1, 16]]
            },
            "ranged_damage_modifiers": {
                "physical": randint(2, 6)
            }
        },
        "light crossbow": {
            "ranged_chance_to_hit_modifier": 1,
            "ranged_damage_dice": {
                "physical": [[2, 4]]
            },
            "ranged_attack_energy_bonus_modifier": -5
        },
        "crossbow": {
            "ranged_chance_to_hit_modifier": randint(1, 2),
            "ranged_damage_dice": {
                "physical": [[2, 6]]
            },
            "ranged_attack_energy_bonus_modifier": -7
        },
        "heavy crossbow": {
            "ranged_chance_to_hit_modifier": 1,
            "ranged_damage_dice": {
                "physical": [[2, 8]]
            },
            "ranged_attack_energy_bonus_modifier": -10
        },
        "repeating crossbow": {
            "ranged_chance_to_hit_modifier": -1,
            "ranged_damage_dice": {
                "physical": [[4, 4]]
            },
            "ranged_attack_energy_bonus_modifier": -15
        },
        "arbalest": {
            "ranged_chance_to_hit_modifier": -2,
            "ranged_damage_dice": {
                "physical": [[2, 10]]
            },
            "ranged_attack_energy_bonus_modifier": -20
        },
        "heavy arbalest": {
            "ranged_chance_to_hit_modifier": randint(-3, -2),
            "ranged_damage_dice": {
                "physical": [[2, 12]]
            },
            "ranged_attack_energy_bonus_modifier": -25
        },
        "siege crossbow": {
            "ranged_chance_to_hit_modifier": -3,
            "ranged_damage_dice": {
                "physical": [[3, 8]]
            },
            "ranged_attack_energy_bonus_modifier": -28
        },
        "hand ballista": {
            "ranged_chance_to_hit_modifier": randint(-4, -3),
            "ranged_damage_dice": {
                "physical": [[4, 8]]
            },
            "ranged_attack_energy_bonus_modifier": -30
        },
    }
    return weapon_name_modifiers


def generate_melee_weapon_prefix_modifiers():
    melee_weapon_prefix_modifiers = {
        "Deadly": {
            "critical_hit_chance_modifier": randint(3, 8) / 100,
            "critical_hit_damage_multiplier_modifier": randint(5, 15) / 100
        },
        "Blazing": {
            "melee_damage_dice": {
                "fire": [[1, 4]]
            },
            "melee_damage_modifiers": {
                "fire": randint(1, 3)
            },
            "resistances": {
                "fire": randint(1, 5) / 100
            }
        },
        "Searing": {
            "melee_damage_dice": {
                "fire": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "fire": randint(2, 3)
            },
            "resistances": {
                "fire": randint(1, 8) / 100
            }
        },
        "Fireborn": {
            "melee_damage_dice": {
                "fire": [[1, 8]]
            },
            "melee_damage_modifiers": {
                "fire": randint(2, 4)
            },
            "resistances": {
                "fire": randint(1, 10) / 100
            }
        },
        "Chilled": {
            "melee_damage_dice": {
                "ice": [[1, 4]]
            },
            "melee_damage_modifiers": {
                "ice": randint(1, 3)
            },
            "resistances": {
                "ice": randint(1, 5) / 100
            }
        },
        "Freezing": {
            "melee_damage_dice": {
                "ice": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "ice": randint(2, 3)
            },
            "resistances": {
                "ice": randint(1, 8) / 100
            }
        },
        "Frostborn": {
            "melee_damage_dice": {
                "ice": [[1, 8]]
            },
            "melee_damage_modifiers": {
                "ice": randint(2, 4)
            },
            "resistances": {
                "ice": randint(1, 10) / 100
            }
        },
        "Shocking": {
            "melee_damage_dice": {
                "lightning": [[1, 4]]
            },
            "melee_damage_modifiers": {
                "lightning": randint(1, 3)
            },
            "resistances": {
                "lightning": randint(1, 5) / 100
            }
        },
        "Charged": {
            "melee_damage_dice": {
                "lightning": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "lightning": randint(2, 3)
            },
            "resistances": {
                "lightning": randint(1, 8) / 100
            }
        },
        "Thunderstruck": {
            "melee_damage_dice": {
                "lightning": [[1, 8]]
            },
            "melee_damage_modifiers": {
                "lightning": randint(2, 4)
            },
            "resistances": {
                "lightning": randint(1, 10) / 100
            }
        },
        "Holy": {
            "melee_damage_dice": {
                "holy": [[1, 4]]
            },
            "melee_damage_modifiers": {
                "holy": randint(1, 3)
            },
            "resistances": {
                "holy": randint(1, 5) / 100
            }
        },
        "Sanctified": {
            "melee_damage_dice": {
                "holy": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "holy": randint(2, 3)
            },
            "resistances": {
                "holy": randint(1, 8) / 100
            }
        },
        "Sacred": {
            "melee_damage_dice": {
                "holy": [[1, 8]]
            },
            "melee_damage_modifiers": {
                "holy": randint(2, 4)
            },
            "resistances": {
                "holy": randint(1, 10) / 100
            }
        },
        "Abyssal": {
            "melee_damage_dice": {
                "chaos": [[1, 4]]
            },
            "melee_damage_modifiers": {
                "chaos": randint(1, 3)
            },
            "resistances": {
                "chaos": randint(1, 5) / 100
            }
        },
        "Demonic": {
            "melee_damage_dice": {
                "chaos": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "chaos": randint(2, 3)
            },
            "resistances": {
                "chaos": randint(1, 8) / 100
            }
        },
        "Infernal": {
            "melee_damage_dice": {
                "chaos": [[1, 8]]
            },
            "melee_damage_modifiers": {
                "chaos": randint(2, 4)
            },
            "resistances": {
                "chaos": randint(1, 10) / 100
            }
        },
        "Enchanted": {
            "melee_damage_dice": {
                "arcane": [[1, 4]]
            },
            "melee_damage_modifiers": {
                "arcane": randint(1, 3)
            },
            "resistances": {
                "arcane": randint(1, 5) / 100
            }
        },
        "Esoteric": {
            "melee_damage_dice": {
                "arcane": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "arcane": randint(2, 3)
            },
            "resistances": {
                "arcane": randint(1, 8) / 100
            }
        },
        "Eldritch": {
            "melee_damage_dice": {
                "arcane": [[1, 8]]
            },
            "melee_damage_modifiers": {
                "arcane": randint(2, 4)
            },
            "resistances": {
                "arcane": randint(1, 10) / 100
            }
        },
        "Venomous": {
            "melee_damage_dice": {
                "poison": [[1, 4]]
            },
            "melee_damage_modifiers": {
                "poison": randint(1, 3)
            },
            "resistances": {
                "poison": randint(1, 5) / 100
            }
        },
        "Toxic": {
            "melee_damage_dice": {
                "poison": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "poison": randint(2, 3)
            },
            "resistances": {
                "poison": randint(1, 8) / 100
            }
        },
        "Blighted": {
            "melee_damage_dice": {
                "poison": [[1, 8]]
            },
            "melee_damage_modifiers": {
                "poison": randint(2, 4)
            },
            "resistances": {
                "poison": randint(1, 10) / 100
            }
        },
        "Relentless": {
            "melee_chance_to_hit_modifier": 2,
            "melee_damage_dice_modifiers": {
                "physical": [[1, 0]]
            },
            "melee_damage_modifiers": {
                "physical": 1
            },
        },
        "Murderous": {
            "melee_chance_to_hit_modifier": 3,
            "melee_damage_dice_modifiers": {
                "physical": [[2, 0]]
            },
            "melee_damage_modifiers": {
                "physical": 2
            },
        },
        "Masterwork": {
            "melee_chance_to_hit_modifier": 4,
            "melee_damage_modifiers": {
                "physical": 4
            },
            "melee_attack_energy_bonus_modifier": 5
        },
        "Nimble": {
            "speed_modifier": 3,
            "melee_attack_energy_bonus_modifier": 3
        },
        "Swift": {
            "speed_modifier": 5,
            "melee_attack_energy_bonus_modifier": 5
        },
        "Quick": {
            "speed_modifier": 8,
            "melee_attack_energy_bonus_modifier": 8
        },
        "Bloodthirsty": {
            "life_steal_modifier": randint(5, 10) / 100,
            "melee_damage_modifiers": {
                "physical": 1
            }
        },
        "Vampiric": {
            "life_steal_modifier": randint(5, 15) / 100,
            "melee_damage_modifiers": {
                "physical": 2
            }
        },
        "Dastardly": {
            "melee_damage_dice_modifiers": {
                "melee_chance_to_hit_modifier": 1,
                "physical": [[0, 4]]
            },
        },
        "Wretched": {
            "melee_chance_to_hit_modifier": randint(1, 2),
            "melee_damage_dice_modifiers": {
                "physical": [[1, 2]]
            },
        },
        "Sinister": {
            "melee_chance_to_hit_modifier": randint(1, 3),
            "melee_damage_dice_modifiers": {
                "physical": [[2, 2]]
            },
        },
        "Brutal": {
            "melee_chance_to_hit_modifier": randint(2, 3),
            "melee_damage_dice_modifiers": {
                "physical": [[3, 0]]
            },
        },
        "Barbaric": {
            "melee_chance_to_hit_modifier": -4,
            "melee_damage_modifiers": {
                "physical": 6
            },
            "melee_damage_dice_modifiers": {
                "physical": [[0, 2]]
            },
        },
        "Stoneforged": {
            "melee_chance_to_hit_modifier": 2,
            "melee_damage_modifiers": {
                "physical": 2
            },
            "melee_damage_dice_modifiers": {
                "physical": [[1, 0]]
            }
        },
        "Skyforged": {
            "melee_chance_to_hit_modifier": 3,
            "melee_damage_modifiers": {
                "physical": 3
            },
            "melee_damage_dice_modifiers": {
                "physical": [[1, 4]]
            }
        },
    }
    return melee_weapon_prefix_modifiers


def generate_ranged_weapon_prefix_modifiers():
    ranged_weapon_prefix_modifiers = {
        "Deadly": {
            "critical_hit_chance_modifier": randint(3, 8) / 100,
            "critical_hit_damage_multiplier_modifier": randint(5, 15) / 100
        },
        "Blazing": {
            "ranged_damage_dice": {
                "fire": [[1, 4]]
            },
            "ranged_damage_modifiers": {
                "fire": randint(1, 3)
            },
            "resistances": {
                "fire": randint(1, 5) / 100
            }
        },
        "Searing": {
            "ranged_damage_dice": {
                "fire": [[1, 6]]
            },
            "ranged_damage_modifiers": {
                "fire": randint(2, 3)
            },
            "resistances": {
                "fire": randint(1, 8) / 100
            }
        },
        "Fireborn": {
            "ranged_damage_dice": {
                "fire": [[1, 8]]
            },
            "ranged_damage_modifiers": {
                "fire": randint(2, 4)
            },
            "resistances": {
                "fire": randint(1, 10) / 100
            }
        },
        "Chilled": {
            "ranged_damage_dice": {
                "ice": [[1, 4]]
            },
            "ranged_damage_modifiers": {
                "ice": randint(1, 3)
            },
            "resistances": {
                "ice": randint(1, 5) / 100
            }
        },
        "Freezing": {
            "ranged_damage_dice": {
                "ice": [[1, 6]]
            },
            "ranged_damage_modifiers": {
                "ice": randint(2, 3)
            },
            "resistances": {
                "ice": randint(1, 8) / 100
            }
        },
        "Frostborn": {
            "ranged_damage_dice": {
                "ice": [[1, 8]]
            },
            "ranged_damage_modifiers": {
                "ice": randint(2, 4)
            },
            "resistances": {
                "ice": randint(1, 10) / 100
            }
        },
        "Shocking": {
            "ranged_damage_dice": {
                "lightning": [[1, 4]]
            },
            "ranged_damage_modifiers": {
                "lightning": randint(1, 3)
            },
            "resistances": {
                "lightning": randint(1, 5) / 100
            }
        },
        "Charged": {
            "ranged_damage_dice": {
                "lightning": [[1, 6]]
            },
            "ranged_damage_modifiers": {
                "lightning": randint(2, 3)
            },
            "resistances": {
                "lightning": randint(1, 8) / 100
            }
        },
        "Thunderstruck": {
            "ranged_damage_dice": {
                "lightning": [[1, 8]]
            },
            "ranged_damage_modifiers": {
                "lightning": randint(2, 4)
            },
            "resistances": {
                "lightning": randint(1, 10) / 100
            }
        },
        "Holy": {
            "ranged_damage_dice": {
                "holy": [[1, 4]]
            },
            "ranged_damage_modifiers": {
                "holy": randint(1, 3)
            },
            "resistances": {
                "holy": randint(1, 5) / 100
            }
        },
        "Sanctified": {
            "ranged_damage_dice": {
                "holy": [[1, 6]]
            },
            "ranged_damage_modifiers": {
                "holy": randint(2, 3)
            },
            "resistances": {
                "holy": randint(1, 8) / 100
            }
        },
        "Sacred": {
            "ranged_damage_dice": {
                "holy": [[1, 8]]
            },
            "ranged_damage_modifiers": {
                "holy": randint(2, 4)
            },
            "resistances": {
                "holy": randint(1, 10) / 100
            }
        },
        "Abyssal": {
            "ranged_damage_dice": {
                "chaos": [[1, 4]]
            },
            "ranged_damage_modifiers": {
                "chaos": randint(1, 3)
            },
            "resistances": {
                "chaos": randint(1, 5) / 100
            }
        },
        "Demonic": {
            "ranged_damage_dice": {
                "chaos": [[1, 6]]
            },
            "ranged_damage_modifiers": {
                "chaos": randint(2, 3)
            },
            "resistances": {
                "chaos": randint(1, 8) / 100
            }
        },
        "Infernal": {
            "ranged_damage_dice": {
                "chaos": [[1, 8]]
            },
            "ranged_damage_modifiers": {
                "chaos": randint(2, 4)
            },
            "resistances": {
                "chaos": randint(1, 10) / 100
            }
        },
        "Enchanted": {
            "ranged_damage_dice": {
                "arcane": [[1, 4]]
            },
            "ranged_damage_modifiers": {
                "arcane": randint(1, 3)
            },
            "resistances": {
                "arcane": randint(1, 5) / 100
            }
        },
        "Esoteric": {
            "ranged_damage_dice": {
                "arcane": [[1, 6]]
            },
            "ranged_damage_modifiers": {
                "arcane": randint(2, 3)
            },
            "resistances": {
                "arcane": randint(1, 8) / 100
            }
        },
        "Eldritch": {
            "ranged_damage_dice": {
                "arcane": [[1, 8]]
            },
            "ranged_damage_modifiers": {
                "arcane": randint(2, 4)
            },
            "resistances": {
                "arcane": randint(1, 10) / 100
            }
        },
        "Venomous": {
            "ranged_damage_dice": {
                "poison": [[1, 4]]
            },
            "ranged_damage_modifiers": {
                "poison": randint(1, 3)
            },
            "resistances": {
                "poison": randint(1, 5) / 100
            }
        },
        "Toxic": {
            "ranged_damage_dice": {
                "poison": [[1, 6]]
            },
            "ranged_damage_modifiers": {
                "poison": randint(2, 3)
            },
            "resistances": {
                "poison": randint(1, 8) / 100
            }
        },
        "Blighted": {
            "ranged_damage_dice": {
                "poison": [[1, 8]]
            },
            "ranged_damage_modifiers": {
                "poison": randint(2, 4)
            },
            "resistances": {
                "poison": randint(1, 10) / 100
            }
        },
        "Relentless": {
            "ranged_chance_to_hit_modifier": 2,
            "ranged_damage_dice_modifiers": {
                "physical": [[1, 0]]
            },
            "ranged_damage_modifiers": {
                "physical": 1
            },
        },
        "Murderous": {
            "ranged_chance_to_hit_modifier": 3,
            "ranged_damage_dice_modifiers": {
                "physical": [[2, 0]]
            },
            "ranged_damage_modifiers": {
                "physical": 2
            },
        },
        "Masterwork": {
            "ranged_chance_to_hit_modifier": 4,
            "ranged_damage_modifiers": {
                "physical": 4
            },
            "melee_attack_energy_bonus_modifier": 5
        },
        "Nimble": {
            "speed_modifier": 3,
            "melee_attack_energy_bonus_modifier": 3
        },
        "Swift": {
            "speed_modifier": 5,
            "melee_attack_energy_bonus_modifier": 5
        },
        "Quick": {
            "speed_modifier": 8,
            "melee_attack_energy_bonus_modifier": 8
        },
        "Bloodthirsty": {
            "life_steal_modifier": randint(5, 10) / 100,
            "ranged_damage_modifiers": {
                "physical": 1
            }
        },
        "Vampiric": {
            "life_steal_modifier": randint(5, 15) / 100,
            "ranged_damage_modifiers": {
                "physical": 2
            }
        },
        "Dastardly": {
            "ranged_damage_dice_modifiers": {
                "ranged_chance_to_hit_modifier": 1,
                "physical": [[0, 4]]
            },
        },
        "Wretched": {
            "ranged_chance_to_hit_modifier": randint(1, 2),
            "ranged_damage_dice_modifiers": {
                "physical": [[1, 2]]
            },
        },
        "Sinister": {
            "ranged_chance_to_hit_modifier": randint(1, 3),
            "ranged_damage_dice_modifiers": {
                "physical": [[2, 2]]
            },
        },
        "Brutal": {
            "ranged_chance_to_hit_modifier": randint(2, 3),
            "ranged_damage_dice_modifiers": {
                "physical": [[3, 0]]
            },
        },
        "Barbaric": {
            "ranged_chance_to_hit_modifier": -4,
            "ranged_damage_modifiers": {
                "physical": 6
            },
            "ranged_damage_dice_modifiers": {
                "physical": [[0, 2]]
            },
        },
        "Stoneforged": {
            "ranged_chance_to_hit_modifier": 2,
            "ranged_damage_modifiers": {
                "physical": 2
            },
            "ranged_damage_dice_modifiers": {
                "physical": [[1, 0]]
            }
        },
        "Skyforged": {
            "ranged_chance_to_hit_modifier": 3,
            "ranged_damage_modifiers": {
                "physical": 3
            },
            "ranged_damage_dice_modifiers": {
                "physical": [[1, 4]]
            }
        },
    }
    return ranged_weapon_prefix_modifiers


def generate_melee_weapon_suffix_modifiers():
    melee_weapon_suffix_modifiers = {
        "of Alacrity": {
            "speed_modifier": 3,
            "melee_attack_energy_bonus_modifier": 3
        },
        "of Celerity": {
            "speed_modifier": 5,
            "melee_attack_energy_bonus_modifier": 5
        },
        "of Defense": {
            "armor_class_modifier": 3
        },
        "of Protection": {
            "armor_modifier": 2
        },
        "of Strength": {
            "strength_modifier": 1,
            "melee_chance_to_hit_modifier": 1
        },
        "of the Juggernaut": {
            "strength_modifier": 2,
            "melee_chance_to_hit_modifier": 2
        },
        "of the Hawk": {
            "perception_modifier": 1,
            "ranged_chance_to_hit_modifier": 1
        },
        "of the Eagle": {
            "perception_modifier": 2,
            "ranged_chance_to_hit_modifier": 2
        },
        "of the Cat": {
            "dexterity_modifier": 1,
            "melee_chance_to_hit_modifier": 1,
            "ranged_chance_to_hit_modifier": 1
        },
        "of the Fox": {
            "dexterity_modifier": 2,
            "melee_chance_to_hit_modifier": 1,
            "ranged_chance_to_hit_modifier": 1
        },
        "of Endurance": {
            "constitution_modifier": 1,
            "max_hp_modifier": 5
        },
        "of Toughness": {
            "constitution_modifier": 2,
            "armor_modifier": 1
        },
        "of the Magi": {
            "intelligence_modifier": 1,
            "melee_damage_modifiers": {
                "arcane": 1
            }
        },
        "of the Wizard": {
            "intelligence_modifier": 2,
            "melee_damage_modifiers": {
                "arcane": 2
            }
        },
        "of Wisdom": {
            "wisdom_modifier": 1,
            "melee_damage_modifiers": {
                "holy": 1
            }
        },
        "of Piety": {
            "wisdom_modifier": 2,
            "melee_damage_modifiers": {
                "holy": 2
            }
        },
        "of Charisma": {
            "charisma_modifier": 1
        },
        "of the Silver Tongue": {
            "charisma_modifier": 2
        },
        "of Fate": {
            "luck_modifier": 1,
            "melee_chance_to_hit_modifier": 1,
            "critical_hit_chance_modifier": 1 / 100
        },
        "of Fortune": {
            "luck_modifier": 2,
            "melee_chance_to_hit_modifier": 1,
            "critical_hit_chance_modifier": 1 / 100
        },
        "of Longevity": {
            "max_hp_modifier": randint(5, 10)
        },
        "of Health": {
            "max_hp_modifier": randint(10, 15)
        },
        "of Life": {
            "max_hp_modifier": 5,
            "max_hp_multiplier_modifier": 0.2
        },
        "of Flames": {
            "melee_damage_dice_modifiers": {
                "fire": [[1, 2]]
            },
            "melee_damage_modifiers": {
                "fire": 1
            }
        },
        "of Scorching": {
            "melee_damage_dice_modifiers": {
                "fire": [[1, 3]]
            },
            "melee_damage_modifiers": {
                "fire": 2
            }
        },
        "of Conflagaration": {
            "melee_damage_dice_modifiers": {
                "fire": [[1, 4]]
            },
            "melee_damage_multiplier_modifiers": {
                "fire": 0.1
            }
        },
        "of the Flamecaller": {
            "melee_damage_dice_modifiers": {
                "fire": [[2, 2]]
            },
            "melee_damage_multiplier_modifiers": {
                "fire": 0.25
            }
        },
        "of Frostbite": {
            "melee_damage_dice_modifiers": {
                "ice": [[1, 1]]
            },
            "melee_damage_modifiers": {
                "ice": 2
            },
            "melee_damage_multiplier_modifiers": {
                "ice": 0.1
            }
        },
        "of the Glacier": {
            "melee_damage_dice_modifiers": {
                "ice": [[1, 2]]
            },
            "melee_damage_modifiers": {
                "ice": 4
            },
            "melee_damage_multiplier_modifiers": {
                "ice": 0.2
            }
        },
        "of Shocking": {
            "melee_damage_dice_modifiers": {
                "thunder": [[1, 1]]
            },
            "melee_damage_modifiers": {
                "lightning": 2
            },
            "melee_damage_multiplier_modifiers": {
                "lightning": 0.1
            }
        },
        "of Thunder": {
            "melee_damage_dice_modifiers": {
                "thunder": [[1, 1]]
            },
            "melee_damage_modifiers": {
                "lightning": 4
            },
            "melee_damage_multiplier_modifiers": {
                "lightning": 0.2
            }
        },
        "of Purification": {
            "melee_damage_dice": {
                "holy": [[1, 4]]
            },
            "melee_damage_modifiers": {
                "holy": 2
            }
        },
        "of the Heavens": {
            "melee_damage_dice": {
                "holy": [[1, 4]]
            },
            "melee_damage_modifiers": {
                "holy": 4
            }
        },
        "of Celestial Wrath": {
            "melee_damage_dice": {
                "holy": [[1, 6]]
            },
            "melee_damage_modifiers": {
                "holy": 2
            },
            "melee_damage_multiplier_modifiers": {
                "holy": 0.25
            }
        },
        "of the Void": {
            "melee_damage_dice": {
                "chaos": [[1, 4]]
            },
            "melee_damage_modifiers": {
                "chaos": 2
            }
        },
        "of the Arcane": {
            "melee_damage_dice": {
                "arcane": [[1, 4]]
            },
            "melee_damage_modifiers": {
                "arcane": 2
            }
        },
        "of Wildfire": {
            "melee_damage_modifiers": {
                "fire": 2,
                "arcane": 2
            },
            "melee_damage_multiplier_modifiers": {
                "fire": 0.1,
                "arcane": 0.1
            }
        },
        "of Evasion": {
            "armor_class_modifier": 1,
            "dodge_modifier": 4
        },
        "of Ruin": {
            "melee_damage_modifiers": {
                "physical": 10
            }
        },
        "of Poison": {
            "melee_damage_dice": {
                "poison": [[1, 4]]
            },
            "melee_damage_modifiers": {
                "poison": 2
            }
        },
        "of Decay": {
            "equippable_effects": [ApplyDecayP50OnAttack],
            "melee_damage_modifiers": {
                "physical": 1
            },
            "critical_hit_chance_modifier": randint(1, 3) / 100
        },
        "of Death": {
            "melee_chance_to_hit_modifier": 2,
            "melee_damage_dice": {
                "physical": [[1, 10]]
            },
            "melee_damage_modifiers": {
                "physical": randint(3, 6)
            },
            "melee_damage_dice_modifiers": {
                "physical": [[2, 2]]
            },
            "critical_hit_chance_modifier": randint(1, 2) / 100,
            "max_hp_multiplier_modifier": -0.25
        },
        "of Insanity": {},
        "of the Slayer": {
            "melee_chance_to_hit_modifier": 6,
            "melee_damage_modifiers": {
                "physical": 6
            },
            "critical_hit_chance_modifier": randint(1, 3) / 100,
            "critical_hit_damage_multiplier_modifier": 5 / 100
        },
        "of the Excecutioner": {
            "melee_chance_to_hit_modifier": 8,
            "melee_damage_modifiers": {
                "physical": 8
            },
            "melee_damage_dice_modifiers": {
                "physical": [[0, 1]]
            },
            "critical_hit_chance_modifier": randint(2, 4) / 100,
            "critical_hit_damage_multiplier_modifier": 10 / 100
        },
        "of Fervor": {
            "speed_modifier": 3,
            "melee_attack_energy_bonus_modifier": 8,
            "melee_chance_to_hit_modifier": 2,
        },
        "of Voracity": {
            "speed_modifier": 2,
            "melee_attack_energy_bonus_modifier": 5,
            "life_steal_modifier": 5 / 100
        },
        "of Cruelty": {},
        "of Ruthlessness": {},
        "of Fury": {
            "speed_modifier": randint(1, 10),
            "melee_attack_energy_bonus_modifier": randint(1, 10),
            "melee_damage_modifiers": {
                "physical": randint(1, 4)
            },
            "melee_damage_multiplier_modifiers": {
                "physical": 0.1
            }
        },
        "of Slaughter": {
            "melee_damage_dice": {
                "physical": [[2, 4]]
            },
            "melee_damage_multiplier_modifiers": {
                "physical": 0.2
            }
        },
        "of Ferocity": {
            "melee_attack_energy_bonus_modifier": 5,
            "melee_damage_modifiers": {
                "physical": 2
            },
            "melee_chance_to_hit_modifier": 2
        },
        "of Onslaught": {
            "speed_modifier": 5,
            "melee_attack_energy_bonus_modifier": 5,
            "equippable_effects": [OnCriticalApplyPhysicalDamage25]
        },
        "of Destruction": {
            "melee_damage_dice_modifiers": {
                "physical": [[2, 0]]
            }
        },
        "of Devastation": {
            "melee_damage_dice_modifiers": {
                "physical": [[3, 0]]
            }
        },
        "of Decimation": {
            "melee_damage_dice_modifiers": {
                "physical": [[4, 0]]
            }
        },
        "of Annihilation": {
            "melee_damage_dice_modifiers": {
                "physical": [[2, 2]]
            }
        },
        "of Disintegration": {
            "melee_damage_dice_modifiers": {
                "physical": [[1, 0]],
                "arcane": [[2, 4]]
            }
        },
        "of Obliteration": {
            "melee_damage_dice_modifiers": {
                "physical": [[3, 3]]
            },
            "melee_damage_modifiers": {
                "physical": 6
            }
        },
        "of the Elements": {
            "melee_damage_dice": {
                "fire": [[1, 2]],
                "ice": [[1, 2]],
                "lightning": [[1, 2]]
            },
            "melee_damage_modifiers": {
                "fire": 4,
                "ice": 4,
                "lightning": 4,
            }
        },
        "of Piercing": {
            "equippable_effects": [ApplyArmorPierce25OnAttack]
        },
        "of Shattering": {
            "equippable_effects": [ApplyArmorPierce50OnAttack]
        },
        "of Torment": {},
        "of Mortality": {
            "melee_damage_modifiers": {
                "physical": 8
            },
            "melee_damage_multiplier_modifiers": {
                "physical": 0.5
            },
            "max_hp_multiplier_modifier": -0.5
        },
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
        "of Scorching": {},
        "of Conflagaration": {},
        "of the Flamecaller": {},
        "of Frostbite": {},
        "of the Glacier": {},
        "of Shocking": {},
        "of Thunder": {},
        "of Purification": {},
        "of the Heavens": {},
        "of Celestial Wrath": {},
        "of the Void": {},
        "of the Arcane": {},
        "of Wildfire": {},
        "of Evasion": {},
        "of Ruin": {},
        "of Poison": {},
        "of Decay": {},
        "of Death": {},
        "of Insanity": {},
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
        "of Destruction": {},
        "of Devastation": {},
        "of Decimation": {},
        "of Annihilation": {},
        "of Disintegration": {},
        "of Obliteration": {},
        "of the Elements": {},
        "of Shattering": {},
        "of Piercing": {},
        "of Torment": {},
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

    suffix = "of Decay"

    rarity = {
        "rarity_level": rarity_level,
        "rarity_color": rarities["rarity_colors"][rarity_level]
    }

    weapon_type = "".join(
        choices(weapon_types["types"], weapon_types["weights"]))

    if weapon_type in ["pistol", "rifle", "bow", "crossbow"]:
        slot = EquipmentSlots.RANGED_WEAPON
        weapon_quality_modifiers = generate_ranged_quality_modifiers()[quality]
        if prefix:
            prefix_modifiers = generate_ranged_weapon_prefix_modifiers(
            )[prefix]
        if suffix:
            suffix_modifiers = generate_ranged_weapon_suffix_modifiers(
            )[suffix]
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

    ammunitions = {
        "bow": "arrow",
        "crossbow": "bolt",
        "pistol": "bullet",
        "rifle": "bullet"
    }

    ammunition = ammunitions.get(weapon_type, None)

    two_handed = True if weapon_type in ["twohanded", "polearm"] else False

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
        possible_rarity_modifiers = generate_ranged_weapon_rarity_modifiers(
        )[rarity_level] if weapon_type in [
            "pistol", "rifle", "bow", "crossbow"
        ] else generate_melee_weapon_rarity_modifiers()[rarity_level]
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
        "armor_multiplier_modifier": 0,
        "armor_class_modifier": 0,
        "armor_class_multiplier_modifier": 0,
        "dodge_modifier": 0,
        "shield_armor_class": 0,
        "max_hp_modifier": 0,
        "max_hp_multiplier_modifier": 0,
        "speed_modifier": 0,
        "movement_energy_bonus_modifier": 0,
        "melee_attack_energy_bonus_modifier": 0,
        "ranged_attack_energy_bonus_modifier": 0,
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
        "melee_damage_multiplier_modifiers": {
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
        "ranged_damage_multiplier_modifiers": {
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
        },
        "resistance_multiplier_modifiers": {
            "physical": 0,
            "fire": 0,
            "ice": 0,
            "lightning": 0,
            "holy": 0,
            "chaos": 0,
            "arcane": 0,
            "poison": 0,
        },
        "equippable_effects": []
    }

    for modifiers in total_modifiers:
        for modifier_name, modifier_value in modifiers.items():
            if modifier_name in modifiers:
                if modifier_name == "equippable_effects":
                    combined_modifiers[modifier_name].extend(modifier_value)
                elif type(modifier_value) is dict:
                    if modifier_name in [
                            "melee_damage_dice", "ranged_damage_dice"
                    ]:
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

    # Instantiate the equippable effects, replacing the function with the class instance
    equippable_component.equippable_effects = [
        effect_function() for effect_function in equippable_component.equippable_effects
    ]

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
