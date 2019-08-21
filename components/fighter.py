from typing import TYPE_CHECKING, List, Dict, Any
from game_messages import Message
import tcod
from random import randint, random
from components.attributes import attribute_modifier_values
from components.status_effects import status_effects_by_damage_type, HalveMaxHP
from copy import deepcopy

if TYPE_CHECKING:
    from components.attributes import Attributes
    from entity import Entity


class Fighter:
    def __init__(
            self,
            attributes: "Attributes",
            current_hp: int,
            base_armor_class: int,
            base_dodge: int,
            base_armor: int,
            base_melee_cth_modifier: int,
            base_ranged_cth_modifier: int,
            base_speed: int,
            base_melee_attack_energy_bonus: int,
            base_ranged_attack_energy_bonus: int,
            base_movement_energy_bonus: int,
            base_natural_hp_regeneration_speed: int,
            base_resistances: Dict[str, float] = {
                "physical": 0,
                "fire": 0,
                "ice": 0,
                "lightning": 0,
                "holy": 0,
                "chaos": 0,
                "arcane": 0,
                "poison": 0,
            },
            base_critical_hit_chance: float = 0.05,
            base_critical_hit_damage_multiplier: float = 1.5,
            base_life_steal: float = 0,
            base_damage_reflection: float = 0,
            base_melee_damage_modifiers: Dict[str, int] = {
                "physical": 0,
                "fire": 0,
                "ice": 0,
                "lightning": 0,
                "holy": 0,
                "chaos": 0,
                "arcane": 0,
                "poison": 0,
            },
            base_ranged_damage_modifiers: Dict[str, int] = {
                "physical": 0,
                "fire": 0,
                "ice": 0,
                "lightning": 0,
                "holy": 0,
                "chaos": 0,
                "arcane": 0,
                "poison": 0,
            },
            base_melee_damage_dice: Dict[str, List] = {
                "physical": [],
                "fire": [],
                "ice": [],
                "lightning": [],
                "holy": [],
                "chaos": [],
                "arcane": [],
                "poison": [],
            },
            base_ranged_damage_dice: Dict[str, List] = {
                "physical": [],
                "fire": [],
                "ice": [],
                "lightning": [],
                "holy": [],
                "chaos": [],
                "arcane": [],
                "poison": [],
            },
            xp_reward: int = 0,
    ):
        self.attributes = attributes
        self.current_hp = current_hp
        self.base_armor_class = base_armor_class
        self.base_armor_class_multiplier = 1
        self.base_dodge = base_dodge
        self.base_max_hp: int = self.current_hp
        self.base_max_hp_multiplier = 1
        self.base_armor = base_armor
        self.base_armor_multiplier = 1
        self.base_melee_cth_modifier = base_melee_cth_modifier
        self.base_melee_cth_multiplier = 1
        self.base_ranged_cth_modifier = base_ranged_cth_modifier
        self.base_ranged_cth_multiplier = 1
        self.base_speed = base_speed
        self.base_melee_attack_energy_bonus = base_melee_attack_energy_bonus
        self.base_ranged_attack_energy_bonus = base_ranged_attack_energy_bonus
        self.base_movement_energy_bonus = base_movement_energy_bonus
        self.base_natural_hp_regeneration_speed = base_natural_hp_regeneration_speed
        self.turns_to_natural_regenerate: int = 0
        self.base_resistances = base_resistances
        self.base_resistance_multipliers = {
            "physical": 1,
            "fire": 1,
            "ice": 1,
            "lightning": 1,
            "holy": 1,
            "chaos": 1,
            "arcane": 1,
            "poison": 1,
        }
        self.base_critical_hit_chance = base_critical_hit_chance
        self.base_critical_hit_damage_multiplier = base_critical_hit_damage_multiplier
        self.base_life_steal = base_life_steal
        self.base_damage_reflection = base_damage_reflection
        self.base_melee_damage_modifiers = base_melee_damage_modifiers
        self.base_melee_damage_multipliers = {
            "physical": 1,
            "fire": 1,
            "ice": 1,
            "lightning": 1,
            "holy": 1,
            "chaos": 1,
            "arcane": 1,
            "poison": 1,
        }
        self.base_ranged_damage_modifiers = base_ranged_damage_modifiers
        self.base_ranged_damage_multipliers = {
            "physical": 1,
            "fire": 1,
            "ice": 1,
            "lightning": 1,
            "holy": 1,
            "chaos": 1,
            "arcane": 1,
            "poison": 1,
        }
        self.base_melee_damage_dice = base_melee_damage_dice
        self.base_ranged_damage_dice = base_ranged_damage_dice
        self.status_effects: List = []
        self.xp_reward: int = xp_reward
        self.energy: int = 0
        self.base_fov_radius: int = 7
        self.owner = None
        self.actions = 0

    def recalculate_hp(self) -> None:
        self.current_hp = self.max_hp

    def calculate_effect_modifiers(self, modifier_name: str) -> Any:
        if not self.effects_with_modifiers:
            return 0
        modifier = 0
        for effect in self.effects_with_modifiers:
            if effect.modifiers:
                modifier += effect.modifiers.get(modifier_name, 0)
        return modifier

    @property
    def effects_with_modifiers(self):
        return [effect for effect in self.status_effects if effect.modifiers]

    @property
    def effects_with_melee_damage_modifiers(self):
        return [
            effect for effect in self.status_effects if effect.modifiers
            and effect.modifiers.get("melee_damage_modifiers", {})
        ]

    @property
    def effects_with_melee_damage_multiplier_modifiers(self):
        return [
            effect for effect in self.status_effects if effect.modifiers
            and effect.modifiers.get("melee_damage_multiplier_modifiers", {})
        ]

    @property
    def effects_with_ranged_damage_modifiers(self):
        return [
            effect for effect in self.status_effects if effect.modifiers
            and effect.modifiers.get("ranged_damage_modifiers", {})
        ]

    @property
    def effects_with_ranged_damage_multiplier_modifiers(self):
        return [
            effect for effect in self.status_effects if effect.modifiers
            and effect.modifiers.get("ranged_damage_multiplier_modifiers", {})
        ]

    @property
    def effects_with_melee_damage_dice(self):
        return [
            effect for effect in self.status_effects if effect.modifiers
            and effect.modifiers.get("melee_damage_dice", {})
        ]

    @property
    def effects_with_ranged_damage_dice(self):
        return [
            effect for effect in self.status_effects if effect.modifiers
            and effect.modifiers.get("ranged_damage_dice", {})
        ]

    @property
    def effects_with_resistances(self):
        return [
            effect for effect in self.status_effects
            if effect.modifiers and effect.modifiers.get("resistances", {})
        ]

    @property
    def effects_with_resistance_multiplier_modifiers(self):
        return [
            effect for effect in self.status_effects if effect.modifiers
            and effect.modifiers.get("resistance_multiplier_modifiers", {})
        ]

    @property
    def fov_radius(self) -> int:
        return min(
            20, self.base_fov_radius +
            int(round(self.perception["attribute_modifier"] / 2)))

    @property
    def natural_hp_regeneration_speed(self) -> int:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.natural_hp_regeneration_speed + self.constitution[
                "attribute_modifier"]
        else:
            modifier = self.constitution["attribute_modifier"]

        return max(self.base_natural_hp_regeneration_speed + modifier,
                   1) + self.calculate_effect_modifiers(
                       "natural_hp_regeneration_speed_modifier")

    @property
    def melee_chance_to_hit_modifier(self) -> int:
        if self.owner and self.owner.equipment:
            modifier = int(
                round((self.strength["attribute_modifier"] +
                       self.dexterity["attribute_modifier"]) /
                      2)) + self.owner.equipment.melee_chance_to_hit_modifier
        else:
            modifier = int(
                round((self.strength["attribute_modifier"] +
                       self.dexterity["attribute_modifier"]) / 2))
        cth = self.base_melee_cth_modifier + modifier + self.calculate_effect_modifiers(
            "melee_chance_to_hit_modifier")
        if cth > 0:
            cth = int(round(cth * self.melee_chance_to_hit_multiplier))
        return cth

    @property
    def melee_chance_to_hit_multiplier(self) -> float:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.melee_chance_to_hit_multiplier_modifier
        else:
            modifier = 0
        return self.base_melee_cth_multiplier + modifier + self.calculate_effect_modifiers(
            "melee_chance_to_hit_multiplier_modifier")

    @property
    def ranged_chance_to_hit_modifier(self) -> int:
        if self.owner and self.owner.equipment:
            modifier = int(
                round((self.dexterity["attribute_modifier"] +
                       self.perception["attribute_modifier"]) /
                      2)) + self.owner.equipment.ranged_chance_to_hit_modifier
        else:
            modifier = int(
                round((self.dexterity["attribute_modifier"] +
                       self.perception["attribute_modifier"]) / 2))
        cth = self.base_ranged_cth_modifier + modifier + self.calculate_effect_modifiers(
            "ranged_chance_to_hit_modifier")
        if cth > 0:
            cth = int(round(cth * self.ranged_chance_to_hit_multiplier))
        return cth

    @property
    def ranged_chance_to_hit_multiplier(self) -> float:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.ranged_chance_to_hit_multiplier_modifier
        else:
            modifier = 0
        return self.base_ranged_cth_multiplier + modifier + self.calculate_effect_modifiers(
            "ranged_chance_to_hit_multiplier_modifier")

    @property
    def chance_to_hit_lower_bound_modifier(self) -> int:
        return int(
            round((self.strength["attribute_modifier"] +
                   self.luck["attribute_modifier"] +
                   self.dexterity["attribute_modifier"] +
                   self.perception["attribute_modifier"]) / 4))

    @property
    def critical_hit_damage_multiplier(self) -> float:
        if self.owner and self.owner.equipment:
            modifier = (
                self.luck["attribute_modifier"] * 0.05
            ) + self.owner.equipment.critical_hit_damage_multiplier_modifier
        else:
            modifier = (self.luck["attribute_modifier"] * 0.05)
        return self.base_critical_hit_damage_multiplier + modifier + self.calculate_effect_modifiers(
            "critical_hit_damage_multiplier")

    @property
    def critical_hit_chance(self) -> float:
        if self.owner and self.owner.equipment:
            modifier = (self.luck["attribute_modifier"] / 100
                        ) + self.owner.equipment.critical_hit_chance_modifier
        else:
            modifier = self.luck["attribute_modifier"] / 100
        return round(self.base_critical_hit_chance + modifier,
                     2) + self.calculate_effect_modifiers(
                         "critical_hit_chance_modifier")

    @property
    def armor_class(self) -> int:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.armor_class_modifier
        else:
            modifier = 0
        ac = self.base_armor_class + modifier + self.calculate_effect_modifiers(
            "armor_class_modifier")
        if ac > 0:
            ac = int(round(ac * self.armor_class_multiplier))
        return ac

    @property
    def armor_class_multiplier(self) -> float:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.armor_class_multiplier_modifier
        else:
            modifier = 0
        return self.base_armor_class_multiplier + modifier + self.calculate_effect_modifiers(
            "armor_class_multiplier_modifier")

    @property
    def shield_armor_class(self) -> int:
        if self.owner and self.owner.equipment:
            return self.owner.equipment.shield_armor_class
        else:
            return 0

    @property
    def dodge(self) -> int:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.dodge_modifier
        else:
            modifier = 0
        return self.dexterity[
            "attribute_modifier"] + self.base_dodge + modifier + self.calculate_effect_modifiers(
                "dodge_modifier")

    @property
    def speed(self) -> int:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.speed_modifier
        else:
            modifier = 0
        return self.base_speed + modifier + self.calculate_effect_modifiers(
            "speed_modifier")

    @property
    def melee_attack_energy_bonus(self) -> int:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.melee_attack_energy_bonus_modifier
        else:
            modifier = 0
        return self.base_melee_attack_energy_bonus + modifier + self.calculate_effect_modifiers(
            "melee_attack_energy_bonus_modifier")

    @property
    def ranged_attack_energy_bonus(self) -> int:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.ranged_attack_energy_bonus_modifier
        else:
            modifier = 0
        return self.base_ranged_attack_energy_bonus + modifier + self.calculate_effect_modifiers(
            "ranged_attack_energy_bonus_modifier")

    @property
    def movement_energy_bonus(self) -> int:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.movement_energy_bonus_modifier
        else:
            modifier = 0
        return self.base_movement_energy_bonus + modifier + self.calculate_effect_modifiers(
            "movement_energy_bonus_modifier")

    @property
    def max_hp(self) -> int:
        if self.owner and self.owner.equipment:
            modifier = self.constitution[
                "attribute_modifier"] + self.owner.equipment.max_hp_modifier
        else:
            modifier = self.constitution["attribute_modifier"]
        max_hp = (self.base_max_hp + modifier +
                  self.calculate_effect_modifiers("max_hp_modifier"))

        if max_hp > 0:
            max_hp = int(round(max_hp * self.max_hp_multiplier))

        return max_hp

    @property
    def max_hp_multiplier(self) -> float:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.max_hp_multiplier_modifier
        else:
            modifier = 0
        return self.base_max_hp_multiplier + modifier + self.calculate_effect_modifiers(
            "max_hp_multiplier_modifier")

    @property
    def melee_damage(self) -> Dict[str, int]:
        if self.owner and self.owner.equipment:
            return self.owner.equipment.calculate_melee_damage_modifiers
        else:
            return self.base_melee_damage_modifiers

    @property
    def ranged_damage(self) -> Dict[str, int]:
        if self.owner and self.owner.equipment:
            return self.owner.equipment.calculate_ranged_damage_modifiers
        else:
            return self.base_ranged_damage_modifiers

    @property
    def melee_damage_dice(self) -> Dict[str, List]:
        if self.owner and self.owner.equipment:
            total_melee_damage_dice = self.owner.equipment.calculate_total_melee_damage_dice
        else:
            total_melee_damage_dice = self.base_melee_damage_dice

        # If the fighter doesn't have any damage dice from its base damage dice or from equipment, default to
        # a 1d3 physical damage dice.
        for dice_list in total_melee_damage_dice.values():
            if dice_list:
                break
        else:
            total_melee_damage_dice = {
                "physical": [[1, 3]],
                "fire": [],
                "ice": [],
                "lightning": [],
                "holy": [],
                "chaos": [],
                "arcane": [],
                "poison": [],
            }

        return total_melee_damage_dice

    @property
    def ranged_damage_dice(self) -> Dict[str, List]:
        if self.owner and self.owner.equipment:
            return self.owner.equipment.calculate_total_ranged_damage_dice
        else:
            return self.base_ranged_damage_dice

    @property
    def damage_reflection(self) -> float:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.damage_reflection_modifier
        else:
            modifier = 0

        return self.base_damage_reflection + modifier + self.calculate_effect_modifiers(
            "damage_reflection_modifier")

    @property
    def life_steal(self) -> float:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.life_steal_modifier
        else:
            modifier = 0

        return self.base_life_steal + modifier + self.calculate_effect_modifiers(
            "life_steal_modifier")

    @property
    def armor(self) -> int:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.armor_modifier
        else:
            modifier = 0

        armor = self.base_armor + modifier + self.calculate_effect_modifiers(
            "armor_modifier")

        armor = int(round(armor * self.armor_multiplier))

        # Prevent armor from going below zero, negative armor wouldn't make sense thematically
        return max(0, armor)

    @property
    def armor_multiplier(self) -> float:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.armor_multiplier_modifier
        else:
            modifier = 0
        return self.base_armor_multiplier + modifier + self.calculate_effect_modifiers(
            "armor_multiplier_modifier")

    @property
    def strength(self) -> Dict[str, int]:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.strength_modifier
        else:
            modifier = 0
        attribute_value = self.attributes.STR.attribute_value + modifier + self.calculate_effect_modifiers(
            "strength_modifier")
        attribute = {
            "attribute_value": attribute_value,
            "attribute_modifier": attribute_modifier_values[attribute_value]
        }
        return attribute

    @property
    def perception(self) -> Dict[str, int]:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.perception_modifier
        else:
            modifier = 0
        attribute_value = self.attributes.PER.attribute_value + modifier + self.calculate_effect_modifiers(
            "perception_modifier")
        attribute = {
            "attribute_value": attribute_value,
            "attribute_modifier": attribute_modifier_values[attribute_value]
        }
        return attribute

    @property
    def dexterity(self) -> Dict[str, int]:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.dexterity_modifier
        else:
            modifier = 0
        attribute_value = self.attributes.DEX.attribute_value + modifier + self.calculate_effect_modifiers(
            "dexterity_modifier")
        attribute = {
            "attribute_value": attribute_value,
            "attribute_modifier": attribute_modifier_values[attribute_value]
        }
        return attribute

    @property
    def constitution(self) -> Dict[str, int]:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.constitution_modifier
        else:
            modifier = 0
        attribute_value = self.attributes.CON.attribute_value + modifier + self.calculate_effect_modifiers(
            "constitution_modifier")
        attribute = {
            "attribute_value": attribute_value,
            "attribute_modifier": attribute_modifier_values[attribute_value]
        }
        return attribute

    @property
    def intelligence(self) -> Dict[str, int]:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.intelligence_modifier
        else:
            modifier = 0
        attribute_value = self.attributes.INT.attribute_value + modifier + self.calculate_effect_modifiers(
            "intelligence_modifier")
        attribute = {
            "attribute_value": attribute_value,
            "attribute_modifier": attribute_modifier_values[attribute_value]
        }
        return attribute

    @property
    def wisdom(self) -> Dict[str, int]:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.wisdom_modifier
        else:
            modifier = 0
        attribute_value = self.attributes.WIS.attribute_value + modifier + self.calculate_effect_modifiers(
            "wisdom_modifier")
        attribute = {
            "attribute_value": attribute_value,
            "attribute_modifier": attribute_modifier_values[attribute_value]
        }
        return attribute

    @property
    def charisma(self) -> Dict[str, int]:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.charisma_modifier
        else:
            modifier = 0
        attribute_value = self.attributes.CHA.attribute_value + modifier + self.calculate_effect_modifiers(
            "charisma_modifier")
        attribute = {
            "attribute_value": attribute_value,
            "attribute_modifier": attribute_modifier_values[attribute_value]
        }
        return attribute

    @property
    def luck(self) -> Dict[str, int]:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.luck_modifier
        else:
            modifier = 0
        attribute_value = self.attributes.LCK.attribute_value + modifier + self.calculate_effect_modifiers(
            "luck_modifier")
        attribute = {
            "attribute_value": attribute_value,
            "attribute_modifier": attribute_modifier_values[attribute_value]
        }
        return attribute

    @property
    def resistances(self) -> Dict[str, float]:
        if self.owner and self.owner.equipment:
            return self.owner.equipment.calculate_resistances
        else:
            return self.base_resistances

    def apply_effect(self, new_effect, **kwargs):

        effect_caster = kwargs.get("effect_caster")

        results = []
        apply_effect_results = []
        effect = new_effect()
        effect.owner = self.owner
        if not self.status_effects:
            self.status_effects.append(effect)
            if effect.on_apply:
                apply_effect_results.extend(
                    effect.on_apply(effect, effect_caster=effect_caster))
            if effect.start_message:
                if self.owner.ai:
                    results.append({
                        "message":
                        Message(
                            f"The {self.owner.name}{effect.start_message['monster']['message']}",
                            effect.start_message['monster']['message_color'])
                    })
                else:
                    results.append({
                        "message":
                        Message(
                            f"{effect.start_message['player']['message']}",
                            effect.start_message['player']['message_color'])
                    })
        else:
            for old_effect in self.status_effects:
                if effect.name == old_effect.name and effect.stacking_duration:
                    old_effect.duration += effect.duration
                    break
                elif effect.name == old_effect.name and effect.only_one_allowed:
                    break
            else:
                self.status_effects.append(effect)
                if effect.on_apply:
                    apply_effect_results.extend(
                        effect.on_apply(effect, effect_caster=effect_caster))
                if effect.start_message:
                    if self.owner.ai:
                        results.append({
                            "message":
                            Message(
                                f"The {self.owner.name}{effect.start_message['monster']['message']}",
                                effect.start_message['monster']
                                ['message_color'])
                        })
                    else:
                        results.append({
                            "message":
                            Message(
                                f"{effect.start_message['player']['message']}",
                                effect.start_message['player']
                                ['message_color'])
                        })

        for result in apply_effect_results:
            heal = result.get("heal")
            take_damage = result.get("take_damage")
            message = result.get("message")

            if take_damage:
                results.extend(self.take_damage(take_damage, from_effect=True))

            if heal:
                self.heal(heal)

            if message:
                results.append({"message": message})
        return results

    def take_damage(self,
                    damage_by_type,
                    attacker=None,
                    reflected=False,
                    from_effect=False,
                    from_ranged=False):

        results = []
        # There are cases where the entity might take damage from multiple different sources at the same time (such as effects that
        # are applied immediately), so it's easier to just return nothing if the entity is already dead before
        # trying to process the results of the next damage source (there's no point processing anything if the
        # entity is already dead.)
        if self.current_hp <= 0:
            return results

        for effect in self.status_effects:
            if effect.on_take_damage:
                results.extend(effect.on_take_damage(effect))

        # Don't modify the original rolled damage, the original damage is needed for damage reflection
        rolled_damage = dict.copy(damage_by_type)
        resistances = self.resistances

        # Damage is reduced only if the damage does not originate from an effect.
        # Status effects can still trigger from reflected damage
        if not from_effect:
            for damage_type, damage in rolled_damage.items():
                status_effect_seed = random()
                if damage > 0:
                    if status_effect_seed <= (damage / 200):
                        results.extend(
                            self.apply_effect(
                                status_effects_by_damage_type[damage_type]))

                rolled_damage[damage_type] *= (1 - resistances[damage_type])

                if damage_type == "physical":
                    rolled_damage[damage_type] -= self.armor
        # Damage reflection applies only on directly dealt damage, not on reflected damage or damage
        # coming from effects
        if self.damage_reflection and not reflected and not from_effect and not from_ranged:

            damage_reflection_damage = {}

            for damage_type, damage in damage_by_type.items():
                damage_reflection_damage.update(
                    {damage_type: int(round(damage * self.damage_reflection))})

            results.extend(
                attacker.take_damage(damage_reflection_damage, reflected=True))

        for damage_type in rolled_damage.keys():
            rolled_damage[damage_type] = int(round(rolled_damage[damage_type]))

        damage_amount = 0

        for damage_value in rolled_damage.values():
            damage_amount += damage_value

        self.current_hp -= damage_amount

        if self.current_hp <= 0:

            results.append({"dead": self.owner, "xp": self.xp_reward})
            if self.owner.ai:
                drop_loot = {
                    "items": self.owner.inventory.items +
                    self.owner.inventory.equipment,
                    "x": self.owner.x,
                    "y": self.owner.y,
                    "entity": self.owner
                }
                results.append({"drop_loot": drop_loot})

        # Makes most sense to recalculate the HP here in the case that
        # afte receiving damage some effect will cause the fighter's max HP
        # drop below it's current HP.
        if self.current_hp > self.max_hp:
            self.recalculate_hp()

        return results

    def heal(self, amount: int) -> None:
        self.current_hp += amount

        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def attack(self, target, ranged=False):

        results = []

        attack_hit = False

        for effect in self.status_effects:
            if effect.on_attack:
                results.extend(effect.on_attack(effect, target))

        automatic_hit_seed: float = random()
        dodge_seed: int = randint(1, 20)

        dodge: int = target.fighter.dodge
        shield_ac: int = target.fighter.shield_armor_class
        ac: int = target.fighter.armor_class

        target_roll: int = ac + dodge + shield_ac

        critical_seed: float = random()

        if ranged:
            cth_modifier: int = self.ranged_chance_to_hit_modifier
            damage_dice = self.ranged_damage_dice
            damage_modifiers = self.ranged_damage
        else:
            cth_modifier: int = self.melee_chance_to_hit_modifier
            damage_dice = self.melee_damage_dice
            damage_modifiers = self.melee_damage

        lower_bound_cth_modifier: int = self.chance_to_hit_lower_bound_modifier
        dice_roll: int = randint(1,
                                 20 + cth_modifier) + lower_bound_cth_modifier

        if dice_roll >= target_roll and dodge <= dodge_seed:
            dice_roll = randint(1,
                                20 + cth_modifier) + lower_bound_cth_modifier

        rolled_damage: int = 0

        target_resistances = target.fighter.resistances
        target_armor = target.fighter.armor
        rolled_damage_by_type = {}

        for damage_type in damage_dice:
            damage_type_damage = 0
            for dice_count, dice_sides in damage_dice[damage_type]:
                for _i in range(dice_count):
                    if dice_sides == 0:
                        damage_type_damage += 0
                    else:
                        damage_type_damage += randint(1, dice_sides)

            if damage_modifiers[damage_type]:
                damage_type_damage += damage_modifiers[damage_type]

            if critical_seed <= self.critical_hit_chance:
                damage_type_damage *= self.critical_hit_damage_multiplier

            damage_type_damage = int(round(damage_type_damage))

            rolled_damage_by_type.update({damage_type: damage_type_damage})

            rolled_damage += damage_type_damage

        rolled_damage_dealt = dict.copy(rolled_damage_by_type)

        for damage_type in rolled_damage_dealt.keys():

            rolled_damage_dealt[damage_type] *= (
                1 - target_resistances[damage_type])

            if damage_type == "physical":
                rolled_damage_dealt[damage_type] -= target_armor

            rolled_damage_dealt[damage_type] = int(
                round(rolled_damage_dealt[damage_type]))

        total_damage_dealt = 0

        for damage in rolled_damage_dealt.values():
            total_damage_dealt += damage
        messages = {
            "monster_blocked_1":
            Message(f"The {target.name} blocks your attack!", "red"),
            "player_blocked_1":
            Message(f"You block the {self.owner.name}'s attack!", "green"),
            "monster_blocked_2":
            Message(f"The {target.name} deflects your attack!", "red"),
            "player_blocked_2":
            Message(f"You deflect the {self.owner.name}'s attack!", "green"),
            "monster_dodged_1":
            Message(f"The {target.name} dodges your attack!", "red"),
            "player_dodged_1":
            Message(f"You dodge the {self.owner.name}'s attack!", "green"),
            "monster_dodged_2":
            Message(f"The {target.name} evades your attack!", "red"),
            "player_dodged_2":
            Message(f"You evade the {self.owner.name}'s attack!", "green"),
            "monster_critical_hit_no_damage":
            Message(
                f"The {self.owner.name.capitalize()} critically hits you but does not manage to pierce your armor!",
                "green"),
            "monster_critical_hit":
            Message(
                f"The {self.owner.name.capitalize()} critically hits you for {total_damage_dealt} damage!",
                "crimson"),
            "monster_hit":
            Message(
                f"The {self.owner.name.capitalize()} hits you for {total_damage_dealt} damage.",
                "white"),
            "monster_no_damage":
            Message(
                f"Your armor blocks the {self.owner.name.capitalize()}'s attack!",
                "light_green"),
            "monster_miss":
            Message(f"The {self.owner.name.capitalize()}'s attack misses.",
                    "white"),
            "monster_critical_miss":
            Message(
                f"The {self.owner.name.capitalize()} critically misses you and fumbles in its movements!",
                "dark green"),
            "player_hit":
            Message(
                f"You hit the {target.name.capitalize()} for {total_damage_dealt} damage.",
                "white"),
            "player_critical_hit":
            Message(
                f"You critically hit the {target.name.capitalize()} for {total_damage_dealt} damage!",
                "gold"),
            "player_critical_hit_no_damage":
            Message(
                f"You critically hit the {target.name.capitalize()} but still do not manage to harm it!",
                "red"),
            "player_no_damage":
            Message(
                f"You succesfully hit the {target.name.capitalize()} but do not manage to harm it!",
                "light red"),
            "player_miss":
            Message("Your attack misses.", "white"),
            "player_critical_miss":
            Message(
                f"You critically miss the {target.name.capitalize()} and lose your balance!",
                "dark red")
        }

        if automatic_hit_seed >= 0.95:

            if critical_seed <= self.critical_hit_chance and total_damage_dealt > 0:
                results.append({
                    "message":
                    messages["monster_critical_hit"]
                    if self.owner.ai else messages["player_critical_hit"]
                })

                for effect in self.status_effects:
                    if effect.on_deal_damage:
                        results.extend(
                            effect.on_deal_damage(
                                effect,
                                target=target,
                                damage_dealt=total_damage_dealt))

                    if effect.on_critical_hit:
                        results.extend(effect.on_critical_hit(effect))

                    if effect.on_attack_hit:
                        results.extend(effect.on_attack_hit(effect))

                results.extend(
                    target.fighter.take_damage(rolled_damage_by_type,
                                               attacker=self,
                                               from_ranged=ranged))

                if not self.owner.ai:
                    self.energy += 25

                attack_hit = True

            elif critical_seed <= self.critical_hit_chance and total_damage_dealt < 0:

                results.append({
                    "message":
                    messages["monster_critical_hit_no_damage"] if self.owner.ai
                    else messages["player_critical_hit_no_damage"]
                })

                for effect in self.status_effects:
                    if effect.on_critical_hit:
                        results.extend(effect.on_critical_hit(effect))

                if not self.owner.ai:
                    self.energy += 25

                attack_hit = True

            elif total_damage_dealt > 0:
                results.append({
                    "message":
                    messages["monster_hit"]
                    if self.owner.ai else messages["player_hit"]
                })

                for effect in self.status_effects:
                    if effect.on_deal_damage:
                        results.extend(
                            effect.on_deal_damage(
                                effect,
                                target=target,
                                damage_dealt=total_damage_dealt))

                    if effect.on_attack_hit:
                        results.extend(effect.on_attack_hit(effect))

                results.extend(
                    target.fighter.take_damage(rolled_damage_by_type,
                                               attacker=self,
                                               from_ranged=ranged))

                attack_hit = True
            else:
                results.append({
                    "message":
                    messages["monster_no_damage"]
                    if self.owner.ai else messages["player_no_damage"]
                })

                for effect in self.status_effects:
                    if effect.on_attack_hit:
                        results.extend(effect.on_attack_hit(effect))
                attack_hit = True

        elif critical_seed >= 0.95:
            results.append({
                "message":
                messages["monster_critical_miss"]
                if self.owner.ai else messages["player_critical_miss"]
            })

            for effect in self.status_effects:
                if effect.on_critical_miss:
                    results.extend(effect.on_critical_miss(effect))

                if effect.on_attack_miss:
                    results.extend(effect.on_attack_miss(effect))

            self.energy -= 50

        elif dice_roll > ac and dice_roll < (ac + dodge):
            if randint(0, 1) == 1:
                results.append({
                    "message":
                    messages["monster_dodged_1"]
                    if target.ai else messages["player_dodged_1"]
                })
            else:
                results.append({
                    "message":
                    messages["monster_dodged_2"]
                    if target.ai else messages["player_dodged_2"]
                })

            for effect in self.status_effects:
                if effect.on_attack_miss:
                    results.extend(effect.on_attack_miss(effect))

        elif dice_roll > (ac + dodge) and dice_roll < (ac + dodge + shield_ac):
            if randint(0, 1) == 1:
                results.append({
                    "message":
                    messages["monster_blocked_1"]
                    if target.ai else messages["player_blocked_1"]
                })
            else:
                results.append({
                    "message":
                    messages["monster_blocked_2"]
                    if target.ai else messages["player_blocked_2"]
                })
            for effect in self.status_effects:
                if effect.on_attack_miss:
                    results.extend(effect.on_attack_miss(effect))

        elif dice_roll >= target_roll:
            if critical_seed <= self.critical_hit_chance and total_damage_dealt > 0:
                results.append({
                    "message":
                    messages["monster_critical_hit"]
                    if self.owner.ai else messages["player_critical_hit"]
                })

                for effect in self.status_effects:
                    if effect.on_deal_damage:
                        results.extend(
                            effect.on_deal_damage(
                                effect,
                                target=target,
                                damage_dealt=total_damage_dealt))

                    if effect.on_critical_hit:
                        results.extend(effect.on_critical_hit(effect))

                results.extend(
                    target.fighter.take_damage(rolled_damage_by_type,
                                               attacker=self,
                                               from_ranged=ranged))

                if not self.owner.ai:
                    self.energy += 25

                attack_hit = True

            elif critical_seed <= self.critical_hit_chance and total_damage_dealt < 0:
                results.append({
                    "message":
                    messages["monster_critical_hit_no_damage"] if self.owner.ai
                    else messages["player_critical_hit_no_damage"]
                })

                for effect in self.status_effects:
                    if effect.on_critical_hit:
                        results.extend(effect.on_critical_hit(effect))

                if not self.owner.ai:
                    self.energy += 25

            elif total_damage_dealt > 0:
                results.append({
                    "message":
                    messages["monster_hit"]
                    if self.owner.ai else messages["player_hit"]
                })

                for effect in self.status_effects:
                    if effect.on_deal_damage:
                        results.extend(
                            effect.on_deal_damage(
                                effect,
                                target=target,
                                damage_dealt=total_damage_dealt))

                    if effect.on_attack_hit:
                        results.extend(effect.on_attack_hit(effect))

                results.extend(
                    target.fighter.take_damage(rolled_damage_by_type,
                                               attacker=self,
                                               from_ranged=ranged))

                attack_hit = True
            else:
                results.append({
                    "message":
                    messages["monster_no_damage"]
                    if self.owner.ai else messages["player_no_damage"]
                })

                for effect in self.status_effects:

                    if effect.on_attack_hit:
                        results.extend(effect.on_attack_hit(effect))
        else:
            results.append({
                "message":
                messages["monster_miss"]
                if self.owner.ai else messages["player_miss"]
            })
            for effect in self.status_effects:
                if effect.on_attack_miss:
                    results.extend(effect.on_attack_miss(effect))

        if ranged and attack_hit:
            results.append({"ranged_attack_hit": target})
            results.append({"ammo_type": self.owner.equipment.RANGED_WEAPON_AMMUNITION.equippable.equippable_type.ammunition_name})

        return results
