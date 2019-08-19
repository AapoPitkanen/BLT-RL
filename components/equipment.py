from equipment_slots import EquipmentSlots
from random import randint
from game_messages import Message
import tcod as libtcod


class Equipment:
    def __init__(self,
                 head=None,
                 shoulders=None,
                 cloak=None,
                 necklace=None,
                 torso=None,
                 legs=None,
                 wrists=None,
                 gloves=None,
                 boots=None,
                 right_ring=None,
                 left_ring=None,
                 main_hand=None,
                 off_hand=None,
                 ranged_weapon=None,
                 ranged_weapon_ammunition=None):
        self.HEAD = head
        self.SHOULDERS = shoulders
        self.CLOAK = cloak
        self.NECKLACE = necklace
        self.TORSO = torso
        self.LEGS = legs
        self.WRISTS = wrists
        self.GLOVES = gloves
        self.BOOTS = boots
        self.RIGHT_RING = right_ring
        self.LEFT_RING = left_ring
        self.MAIN_HAND = main_hand
        self.OFF_HAND = off_hand
        self.RANGED_WEAPON = ranged_weapon
        self.RANGED_WEAPON_AMMUNITION = ranged_weapon_ammunition
        self.owner = None

    def calculate_equipment_modifier(self, modifier_to_search):
        modifier = 0
        for entity in self.__dict__.values():
            if entity and entity.equippable:
                for modifier_name, modifier_value in entity.equippable.__dict__.items(
                ):
                    if modifier_name == modifier_to_search:
                        modifier += modifier_value
        return modifier

    @property
    def calculate_total_melee_damage_dice(self):
        total_damage_dice = {
            "physical": [],
            "fire": [],
            "ice": [],
            "lightning": [],
            "holy": [],
            "chaos": [],
            "arcane": [],
            "poison": [],
        }
        for entity in self.__dict__.values():
            if entity and entity.equippable:
                for damage_type, dice_list in entity.equippable.melee_damage_dice.items(
                ):
                    for dice in dice_list:
                        total_damage_dice[damage_type].append(dice)
        for damage_type, dice_list in self.owner.fighter.base_melee_damage_dice.items(
        ):
            for dice in dice_list:
                total_damage_dice[damage_type].append(dice)

        for effect in self.owner.fighter.effects_with_melee_damage_dice:
            for damage_type, dice_list in effect.modifiers.get(
                    "melee_damage_dice", {}).items():
                for dice in dice_list:
                    total_damage_dice[damage_type].append(dice)

        return total_damage_dice

    @property
    def calculate_total_ranged_damage_dice(self):
        total_damage_dice = {
            "physical": [],
            "fire": [],
            "ice": [],
            "lightning": [],
            "holy": [],
            "chaos": [],
            "arcane": [],
            "poison": [],
        }
        for entity in self.__dict__.values():
            if entity and entity.equippable:
                for damage_type, dice_list in entity.equippable.ranged_damage_dice.items(
                ):
                    for dice in dice_list:
                        total_damage_dice[damage_type].append(dice)
        for damage_type, dice_list in self.owner.fighter.base_ranged_damage_dice.items(
        ):
            for dice in dice_list:
                total_damage_dice[damage_type].append(dice)

        for effect in self.owner.fighter.effects_with_ranged_damage_dice:
            for damage_type, dice_list in effect.modifiers.get(
                    "ranged_damage_dice", {}).items():
                for dice in dice_list:
                    total_damage_dice[damage_type].append(dice)

        return total_damage_dice

    @property
    def calculate_melee_damage_modifiers(self):
        damage_modifiers = {
            "physical": 0,
            "fire": 0,
            "ice": 0,
            "lightning": 0,
            "holy": 0,
            "chaos": 0,
            "arcane": 0,
            "poison": 0,
        }

        damage_multipliers = self.calculate_melee_damage_multipliers

        for slot, entity in self.__dict__.items():
            if entity and entity.equippable:
                for damage_type, damage_modifier in entity.equippable.melee_damage_modifiers.items(
                ):
                    damage_modifiers[damage_type] += damage_modifier
        for damage_type, damage_modifier in self.owner.fighter.base_melee_damage_modifiers.items(
        ):
            damage_modifiers[damage_type] += damage_modifier

        for effect in self.owner.fighter.effects_with_melee_damage_modifiers:
            for damage_type, damage_modifier in effect.modifiers.get(
                    "melee_damage_modifiers", {}).items():
                damage_modifiers[damage_type] += damage_modifier

        damage_modifiers["physical"] += self.owner.fighter.strength[
            "attribute_modifier"]

        for damage_type in damage_modifiers.keys():
            damage_modifiers[damage_type] = int(
                round(damage_modifiers[damage_type] *
                      damage_multipliers[damage_type]))

        return damage_modifiers

    @property
    def calculate_melee_damage_multipliers(self):
        damage_multipliers = {
            "physical": 0,
            "fire": 0,
            "ice": 0,
            "lightning": 0,
            "holy": 0,
            "chaos": 0,
            "arcane": 0,
            "poison": 0,
        }
        for entity in self.__dict__.values():
            if entity and entity.equippable:
                for damage_type, damage_multiplier in entity.equippable.melee_damage_multiplier_modifiers.items(
                ):
                    damage_multipliers[damage_type] += damage_multiplier

        for damage_type, damage_multiplier in self.owner.fighter.base_melee_damage_multipliers.items(
        ):
            damage_multipliers[damage_type] += damage_multiplier

        for effect in self.owner.fighter.effects_with_melee_damage_multiplier_modifiers:
            for damage_type, damage_multiplier in effect.modifiers.get(
                    "melee_damage_multiplier_modifiers", {}).items():
                damage_multipliers[damage_type] += damage_multiplier
        return damage_multipliers

    @property
    def calculate_ranged_damage_modifiers(self):
        damage_modifiers = {
            "physical": 0,
            "fire": 0,
            "ice": 0,
            "lightning": 0,
            "holy": 0,
            "chaos": 0,
            "arcane": 0,
            "poison": 0,
        }

        damage_multipliers = self.calculate_ranged_damage_multipliers

        for slot, entity in self.__dict__.items():
            if entity and entity.equippable:
                for damage_type, damage_modifier in entity.equippable.ranged_damage_modifiers.items(
                ):
                    damage_modifiers[damage_type] += damage_modifier
        for damage_type, damage_modifier in self.owner.fighter.base_ranged_damage_modifiers.items(
        ):
            damage_modifiers[damage_type] += damage_modifier

        for effect in self.owner.fighter.effects_with_ranged_damage_modifiers:
            for damage_type, damage_modifier in effect.modifiers.get(
                    "ranged_damage_modifiers", {}).items():
                damage_modifiers[damage_type] += damage_modifier

        damage_modifiers["physical"] += self.owner.fighter.dexterity[
            "attribute_modifier"]

        for damage_type in damage_modifiers.keys():
            damage_modifiers[damage_type] = int(
                round(damage_modifiers[damage_type] *
                      damage_multipliers[damage_type]))

        return damage_modifiers

    @property
    def calculate_ranged_damage_multipliers(self):
        damage_multipliers = {
            "physical": 0,
            "fire": 0,
            "ice": 0,
            "lightning": 0,
            "holy": 0,
            "chaos": 0,
            "arcane": 0,
            "poison": 0,
        }
        for entity in self.__dict__.values():
            if entity and entity.equippable:
                for damage_type, damage_multiplier in entity.equippable.ranged_damage_multiplier_modifiers.items(
                ):
                    damage_multipliers[damage_type] += damage_multiplier
        for damage_type, damage_multiplier in self.owner.fighter.base_ranged_damage_multipliers.items(
        ):
            damage_multipliers[damage_type] += damage_multiplier

        for effect in self.owner.fighter.effects_with_ranged_damage_multiplier_modifiers:
            for damage_type, damage_multiplier in effect.modifiers.get(
                    "ranged_damage_multiplier_modifiers", {}).items():
                damage_multipliers[damage_type] += damage_multiplier

        return damage_multipliers

    @property
    def calculate_resistance_multipliers(self):
        resistance_multipliers = {
            "physical": 0,
            "fire": 0,
            "ice": 0,
            "lightning": 0,
            "holy": 0,
            "chaos": 0,
            "arcane": 0,
            "poison": 0,
        }
        for entity in self.__dict__.values():
            if entity and entity.equippable:
                for resistance_type, multiplier_value in entity.equippable.resistances.items(
                ):
                    resistance_multipliers[resistance_type] += multiplier_value

        for resistance_type, multiplier_value in self.owner.fighter.base_resistance_multipliers.items(
        ):
            resistance_multipliers[resistance_type] += multiplier_value

        for effect in self.owner.fighter.effects_with_resistance_multiplier_modifiers:
            for resistance_type, multiplier_value in effect.modifiers.get(
                    "resistance_multiplier_modifiers", {}).items():
                resistance_multipliers[resistance_type] += multiplier_value

        # Prevent multiplier from going below zero
        for resistance_type in resistance_multipliers.keys():
            resistance_multipliers[resistance_type] = max(
                0, resistance_multipliers[resistance_type])

        return resistance_multipliers

    @property
    def calculate_resistances(self):
        total_resistances = {
            "physical": 0,
            "fire": 0,
            "ice": 0,
            "lightning": 0,
            "holy": 0,
            "chaos": 0,
            "arcane": 0,
            "poison": 0,
        }

        resistance_multipliers = self.calculate_resistance_multipliers

        for entity in self.__dict__.values():
            if entity and entity.equippable:
                for resistance_type, resistance_value in entity.equippable.resistances.items(
                ):
                    total_resistances[resistance_type] += resistance_value
        for resistance_type, resistance_value in self.owner.fighter.base_resistances.items(
        ):
            total_resistances[resistance_type] += resistance_value

        for effect in self.owner.fighter.effects_with_resistances:
            for resistance_type, resistance_value in effect.modifiers.get(
                    "resistances", {}).items():
                total_resistances[resistance_type] += resistance_value

        if not self.owner.ai:
            physical_and_poison_resistance_modifier = self.owner.fighter.constitution[
                "attribute_modifier"] / 100
            elemental_resistance_modifier = round(
                (self.owner.fighter.intelligence["attribute_modifier"] +
                 self.owner.fighter.luck["attribute_modifier"]) / 2) / 100
            special_resistance_modifier = round(
                (self.owner.fighter.wisdom["attribute_modifier"] +
                 self.owner.fighter.luck["attribute_modifier"]) / 2) / 100
            for resistance_type, resistance_value in self.owner.fighter.base_resistances.items(
            ):
                if resistance_type in ("physical", "poison"):
                    total_resistances[
                        resistance_type] += physical_and_poison_resistance_modifier
                elif resistance_type in ("fire", "ice", "lightning"):
                    total_resistances[
                        resistance_type] += elemental_resistance_modifier
                elif resistance_type in ("holy", "chaos", "arcane"):
                    total_resistances[
                        resistance_type] += special_resistance_modifier

        for resistance_type in total_resistances.keys():
            if total_resistances[resistance_type] > 0:
                total_resistances[resistance_type] *= resistance_multipliers[
                    resistance_type]
            total_resistances[resistance_type] = round(
                total_resistances[resistance_type], 2)

        return total_resistances

    @property
    def damage_reflection_modifier(self):
        return self.calculate_equipment_modifier("damage_reflection_modifier")

    @property
    def life_steal_modifier(self):
        return self.calculate_equipment_modifier("life_steal_modifier")

    @property
    def natural_hp_regeneration_speed(self):
        return self.calculate_equipment_modifier(
            "natural_hp_regeneration_speed_modifier")

    @property
    def melee_chance_to_hit_modifier(self):
        return self.calculate_equipment_modifier(
            "melee_chance_to_hit_modifier")

    @property
    def melee_chance_to_hit_multiplier_modifier(self):
        return self.calculate_equipment_modifier(
            "melee_chance_to_hit_multiplier_modifier")

    @property
    def ranged_chance_to_hit_modifier(self):
        return self.calculate_equipment_modifier(
            "ranged_chance_to_hit_modifier")

    @property
    def ranged_chance_to_hit_multiplier_modifier(self):
        return self.calculate_equipment_modifier(
            "ranged_chance_to_hit_multiplier_modifier")

    @property
    def armor_class_modifier(self):
        return self.calculate_equipment_modifier("armor_class_modifier")

    @property
    def armor_class_multiplier_modifier(self):
        return self.calculate_equipment_modifier(
            "armor_class_multiplier_modifier")

    @property
    def shield_armor_class(self):
        return self.calculate_equipment_modifier("shield_armor_class")

    @property
    def dodge_modifier(self):
        return self.calculate_equipment_modifier("dodge_modifier")

    @property
    def critical_hit_chance_modifier(self):
        return self.calculate_equipment_modifier(
            "critical_hit_chance_modifier")

    @property
    def critical_hit_damage_multiplier_modifier(self):
        return self.calculate_equipment_modifier(
            "critical_hit_damage_multiplier_modifier")

    @property
    def max_hp_modifier(self):
        return self.calculate_equipment_modifier("max_hp_modifier")

    @property
    def max_hp_multiplier_modifier(self):
        return self.calculate_equipment_modifier("max_hp_multiplier_modifier")

    @property
    def speed_modifier(self):
        return self.calculate_equipment_modifier("speed_modifier")

    @property
    def movement_energy_bonus_modifier(self):
        return self.calculate_equipment_modifier(
            "movement_energy_bonus_modifier")

    @property
    def melee_attack_energy_bonus_modifier(self):
        return self.calculate_equipment_modifier(
            "melee_attack_energy_bonus_modifier")
    
    @property
    def ranged_attack_energy_bonus_modifier(self):
        return self.calculate_equipment_modifier(
            "ranged_attack_energy_bonus_modifier")

    @property
    def armor_modifier(self):
        return self.calculate_equipment_modifier("armor_modifier")

    @property
    def armor_multiplier_modifier(self):
        return self.calculate_equipment_modifier("armor_multiplier_modifier")

    @property
    def strength_modifier(self):
        return self.calculate_equipment_modifier("strength_modifier")

    @property
    def perception_modifier(self):
        return self.calculate_equipment_modifier("perception_modifier")

    @property
    def dexterity_modifier(self):
        return self.calculate_equipment_modifier("dexterity_modifier")

    @property
    def constitution_modifier(self):
        return self.calculate_equipment_modifier("constitution_modifier")

    @property
    def intelligence_modifier(self):
        return self.calculate_equipment_modifier("intelligence_modifier")

    @property
    def wisdom_modifier(self):
        return self.calculate_equipment_modifier("wisdom_modifier")

    @property
    def charisma_modifier(self):
        return self.calculate_equipment_modifier("charisma_modifier")

    @property
    def luck_modifier(self):
        return self.calculate_equipment_modifier("luck_modifier")

    def toggle_equip(self, equippable_entity):
        results = []
        equippable_entity_slot = equippable_entity.equippable.slot

        if equippable_entity_slot == EquipmentSlots.OFF_HAND and self.MAIN_HAND and self.MAIN_HAND.equippable.equippable_type.two_handed:
            results.append({
                "cannot_equip":
                Message("Your both hands are in use!", "orange")
            })
            return results
        elif equippable_entity_slot == EquipmentSlots.MAIN_HAND and self.OFF_HAND and equippable_entity.equippable.equippable_type.two_handed:
            results.append({
                "cannot_equip":
                Message("You'll need to free your other hand first!", "orange")
            })
            return results

        elif equippable_entity == self.MAIN_HAND:
            self.MAIN_HAND = None
            results.append({"unequipped": equippable_entity})
            return results

        elif equippable_entity == self.OFF_HAND and self.MAIN_HAND:
            self.OFF_HAND = None
            results.append({"unequipped": equippable_entity})
            return results

        elif equippable_entity == self.OFF_HAND and not self.MAIN_HAND:
            self.OFF_HAND = None
            results.append({"unequipped": equippable_entity})
            return results

        elif equippable_entity_slot == EquipmentSlots.MAIN_HAND and self.MAIN_HAND \
        and not self.OFF_HAND and "weapon_type" in equippable_entity.equippable.equippable_type.__dict__:
            self.OFF_HAND = equippable_entity
            results.append({"dual_wield": equippable_entity})
            return results

        elif equippable_entity_slot == EquipmentSlots.MAIN_HAND and not self.MAIN_HAND \
        and self.OFF_HAND and "weapon_type" in self.OFF_HAND.equippable.equippable_type.__dict__:
            self.MAIN_HAND = equippable_entity
            results.append({"dual_wield": equippable_entity})
            return results

        for slot, equippable in self.__dict__.items():

            if slot == equippable_entity_slot._name_:
                if equippable == equippable_entity:
                    setattr(self, equippable_entity_slot._name_, None)
                    results.append({'unequipped': equippable_entity})
                    break
                else:
                    setattr(self, equippable_entity_slot._name_,
                            equippable_entity)
                    results.append({'equipped': equippable_entity})
                    break

        return results
