from random import randint, random


class Equippable:
    def __init__(
            self,
            equippable_type=None,
            slot=None,
            chance_to_hit_modifier=0,
            armor_modifier=0,
            armor_class_modifier=0,
            max_hp_modifier=0,
            speed_modifier=0,
            movement_energy_bonus_modifier=0,
            attack_energy_bonus_modifier=0,
            critical_hit_chance_modifier=0,
            critical_hit_multiplier_modifier=0,
            strength_modifier=0,
            perception_modifier=0,
            dexterity_modifier=0,
            constitution_modifier=0,
            intelligence_modifier=0,
            wisdom_modifier=0,
            charisma_modifier=0,
            luck_modifier=0,
            life_steal_modifier=0,
            damage_reflection_modifier=0,
            natural_hp_regeneration_speed_modifier=0,
            damage_modifiers={
                "physical": 0,
                "fire": 0,
                "ice": 0,
                "lightning": 0,
                "holy": 0,
                "chaos": 0,
                "arcane": 0,
                "poison": 0,
            },
            damage_dice={
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
        self.chance_to_hit_modifier = chance_to_hit_modifier
        self.armor_modifier = armor_modifier
        self.armor_class_modifier = armor_class_modifier
        self.max_hp_modifier = max_hp_modifier
        self.speed_modifier = speed_modifier
        self.movement_energy_bonus_modifier = movement_energy_bonus_modifier
        self.attack_energy_bonus_modifier = attack_energy_bonus_modifier
        self.critical_hit_chance_modifier = critical_hit_chance_modifier / 100
        self.critical_hit_multiplier_modifier = critical_hit_multiplier_modifier / 100
        self.strength_modifier = strength_modifier
        self.perception_modifier = perception_modifier
        self.dexterity_modifier = dexterity_modifier
        self.constitution_modifier = constitution_modifier
        self.intelligence_modifier = intelligence_modifier
        self.wisdom_modifier = wisdom_modifier
        self.charisma_modifier = charisma_modifier
        self.luck_modifier = luck_modifier
        self.life_steal_modifier = life_steal_modifier / 100
        self.damage_reflection_modifier = damage_reflection_modifier / 100
        self.natural_hp_regeneration_speed_modifier = natural_hp_regeneration_speed_modifier
        self.damage_modifiers = damage_modifiers
        self.damage_dice = damage_dice
        self.resistances = resistances