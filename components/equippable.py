from random import randint, random


class Equippable:
    def __init__(
            self,
            equippable_type=None,
            slot=None,
            melee_chance_to_hit_modifier: int = 0,
            ranged_chance_to_hit_modifier: int = 0,
            armor_modifier: int = 0,
            armor_class_modifier: int = 0,
            dodge_modifier: int = 0,
            shield_armor_class: int = 0,
            max_hp_modifier: int = 0,
            speed_modifier: int = 0,
            movement_energy_bonus_modifier: int = 0,
            attack_energy_bonus_modifier: int = 0,
            critical_hit_chance_modifier: float = 0,
            critical_hit_multiplier_modifier: float = 0,
            strength_modifier: int = 0,
            perception_modifier: int = 0,
            dexterity_modifier: int = 0,
            constitution_modifier: int = 0,
            intelligence_modifier: int = 0,
            wisdom_modifier: int = 0,
            charisma_modifier: int = 0,
            luck_modifier: int = 0,
            life_steal_modifier: float = 0,
            damage_reflection_modifier: float = 0,
            natural_hp_regeneration_speed_modifier: int = 0,
            melee_damage_modifiers={
                "physical": 0,
                "fire": 0,
                "ice": 0,
                "lightning": 0,
                "holy": 0,
                "chaos": 0,
                "arcane": 0,
                "poison": 0,
            },
            ranged_damage_modifiers={
                "physical": 0,
                "fire": 0,
                "ice": 0,
                "lightning": 0,
                "holy": 0,
                "chaos": 0,
                "arcane": 0,
                "poison": 0,
            },
            melee_damage_dice={
                "physical": [],
                "fire": [],
                "ice": [],
                "lightning": [],
                "holy": [],
                "chaos": [],
                "arcane": [],
                "poison": [],
            },
            ranged_damage_dice={
                "physical": [],
                "fire": [],
                "ice": [],
                "lightning": [],
                "holy": [],
                "chaos": [],
                "arcane": [],
                "poison": [],
            },
            resistances={
                "physical": 0,
                "fire": 0,
                "ice": 0,
                "lightning": 0,
                "holy": 0,
                "chaos": 0,
                "arcane": 0,
                "poison": 0,
            }):
        self.slot = slot
        # equippable type is built as a class with the following properties:
        # equipment_type: e.g. "weapon", "torso", "ring" etc.
        # weapons and armor also have additional properties in equipment_type, such as weapon type and such
        # unidentified_name: generic name for the equipment
        # identified_name : full name of the equipment, including material, quality, prefixes and suffixes
        # material: material of the equipment, giving specific bonuses
        # quality: quality of the equipment, giving specific bonuses
        self.equippable_type = equippable_type
        self.melee_chance_to_hit_modifier = melee_chance_to_hit_modifier
        self.ranged_chance_to_hit_modifier = ranged_chance_to_hit_modifier
        self.armor_modifier = armor_modifier
        self.armor_class_modifier = armor_class_modifier
        self.dodge_modifier = dodge_modifier
        self.shield_armor_class = shield_armor_class
        self.max_hp_modifier = max_hp_modifier
        self.speed_modifier = speed_modifier
        self.movement_energy_bonus_modifier = movement_energy_bonus_modifier
        self.attack_energy_bonus_modifier = attack_energy_bonus_modifier
        self.critical_hit_chance_modifier = critical_hit_chance_modifier
        self.critical_hit_multiplier_modifier = critical_hit_multiplier_modifier
        self.strength_modifier = strength_modifier
        self.perception_modifier = perception_modifier
        self.dexterity_modifier = dexterity_modifier
        self.constitution_modifier = constitution_modifier
        self.intelligence_modifier = intelligence_modifier
        self.wisdom_modifier = wisdom_modifier
        self.charisma_modifier = charisma_modifier
        self.luck_modifier = luck_modifier
        self.life_steal_modifier = life_steal_modifier
        self.damage_reflection_modifier = damage_reflection_modifier
        self.natural_hp_regeneration_speed_modifier = natural_hp_regeneration_speed_modifier
        self.melee_damage_modifiers = melee_damage_modifiers
        self.ranged_damage_modifiers = ranged_damage_modifiers
        self.melee_damage_dice = melee_damage_dice
        self.ranged_damage_dice = ranged_damage_dice
        self.resistances = resistances