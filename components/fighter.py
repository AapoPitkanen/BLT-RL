from typing import TYPE_CHECKING, List, Dict, Any
from game_messages import Message
import tcod
from random import randint, random
from components.attributes import attribute_modifier_values
from components.status_effects import status_effects_by_damage_type
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
            base_armor: int,
            base_cth_modifier: int,
            base_speed: int,
            base_attack_energy_bonus: int,
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
            base_critical_hit_multiplier: float = 1.5,
            base_life_steal: float = 0,
            base_damage_reflection: float = 0,
            base_damage_modifiers: Dict[str, int] = {
                "physical": 0,
                "fire": 0,
                "ice": 0,
                "lightning": 0,
                "holy": 0,
                "chaos": 0,
                "arcane": 0,
                "poison": 0,
            },
            base_damage_dice: Dict[str, List] = {
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
        self.base_max_hp: int = self.current_hp
        self.base_armor = base_armor
        self.base_cth_modifier = base_cth_modifier
        self.base_speed = base_speed
        self.base_attack_energy_bonus = base_attack_energy_bonus
        self.base_movement_energy_bonus = base_movement_energy_bonus
        self.base_natural_hp_regeneration_speed = base_natural_hp_regeneration_speed
        self.turns_to_natural_regenerate: int = 0
        self.base_resistances = base_resistances
        self.base_critical_hit_chance = base_critical_hit_chance
        self.base_critical_hit_multiplier = base_critical_hit_multiplier
        self.base_life_steal = base_life_steal
        self.base_damage_reflection = base_damage_reflection
        self.base_damage_modifiers = base_damage_modifiers
        self.base_damage_dice = base_damage_dice
        self.status_effects: List = []
        self.xp_reward = xp_reward
        self.energy: int = 0
        self.base_fov_radius: int = 10
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
    def effects_with_damage_modifiers(self):
        return [
            effect for effect in self.status_effects
            if effect.modifiers and effect.modifiers.get("damage_modifiers")
        ]

    @property
    def effects_with_damage_dice(self):
        return [
            effect for effect in self.status_effects
            if effect.modifiers and effect.modifiers.get("damage_dice")
        ]

    @property
    def effects_with_resistances(self):
        return [
            effect for effect in self.status_effects
            if effect.modifiers and effect.modifiers.get("resistances")
        ]

    @property
    def fov_radius(self) -> int:
        return self.base_fov_radius + self.perception["attribute_modifier"]

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
    def chance_to_hit_modifier(self) -> int:
        if self.owner and self.owner.equipment:
            modifier = int(
                round((self.strength["attribute_modifier"] +
                       self.dexterity["attribute_modifier"] +
                       self.perception["attribute_modifier"]) /
                      2)) + self.owner.equipment.chance_to_hit_modifier
        else:
            modifier = int(
                round((self.strength["attribute_modifier"] +
                       self.dexterity["attribute_modifier"] +
                       self.perception["attribute_modifier"]) / 2))
        return modifier + self.calculate_effect_modifiers(
            "chance_to_hit_modifier")

    @property
    def chance_to_hit_lower_bound_modifier(self) -> int:
        return int(
            round((self.strength["attribute_modifier"] +
                   self.luck["attribute_modifier"] +
                   self.dexterity["attribute_modifier"] +
                   self.perception["attribute_modifier"]) / 4))

    @property
    def critical_hit_multiplier(self) -> float:
        if self.owner and self.owner.equipment:
            modifier = (
                self.luck["attribute_modifier"] *
                0.05) + self.owner.equipment.critical_hit_multiplier_modifier
        else:
            modifier = (self.luck["attribute_modifier"] * 0.05)
        return self.base_critical_hit_multiplier + modifier + self.calculate_effect_modifiers(
            "critical_hit_multiplier")

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
            modifier = self.dexterity[
                "attribute_modifier"] + self.owner.equipment.armor_class_modifier
        else:
            modifier = self.dexterity["attribute_modifier"]
        return self.base_armor_class + modifier + self.calculate_effect_modifiers(
            "armor_class_modifier")

    @property
    def speed(self) -> int:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.speed_modifier
        else:
            modifier = 0
        return self.base_speed + modifier + self.calculate_effect_modifiers(
            "speed_modifier")

    @property
    def attack_energy_bonus(self) -> int:
        if self.owner and self.owner.equipment:
            modifier = self.owner.equipment.attack_energy_bonus_modifier
        else:
            modifier = 0
        return self.base_attack_energy_bonus + modifier + self.calculate_effect_modifiers(
            "attack_energy_bonus_modifier")

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

        return self.base_max_hp + modifier + self.calculate_effect_modifiers(
            "max_hp_modifier")

    @property
    def damage(self) -> Dict[str, int]:
        if self.owner and self.owner.equipment:
            return self.owner.equipment.calculate_damage_modifiers
        else:
            return self.base_damage_modifiers

    @property
    def damage_dice(self) -> Dict[str, List]:
        if self.owner and self.owner.equipment:
            return self.owner.equipment.calculate_total_damage_dice
        else:
            return self.base_damage_dice

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

        return self.base_armor + modifier + self.calculate_effect_modifiers(
            "armor_modifier")

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

    def apply_effect(self, new_effect):
        results = []
        effect = new_effect()
        effect.owner = self.owner
        if not self.status_effects:
            self.status_effects.append(effect)
            if effect.on_apply:
                effect.on_apply(effect)
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
                if effect.name == old_effect.name and effect.stacking:
                    old_effect.duration += effect.duration
                    break
            else:
                self.status_effects.append(effect)
                if effect.on_apply:
                    effect.on_apply(effect)
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
        return results

    def take_damage(self,
                    damage_by_type,
                    attacker=None,
                    reflected=False,
                    from_effect=False):
        results = []
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
        if self.damage_reflection and not reflected and not from_effect:

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

        return results

    def heal(self, amount: int) -> None:
        self.current_hp += amount

        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def attack(self, target):

        damage_dealt: bool = False
        target_hit: bool = False
        results = []

        target_roll: int = target.fighter.armor_class
        critical_seed: float = random()
        cth_modifier: int = self.chance_to_hit_modifier
        lower_bound_cth_modifier: int = self.chance_to_hit_lower_bound_modifier
        dice_roll: int = randint(1,
                                 20 + cth_modifier) + lower_bound_cth_modifier
        damage_dice = self.damage_dice
        damage_modifiers = self.damage
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
                damage_type_damage *= self.critical_hit_multiplier

            damage_type_damage = int(round(damage_type_damage))

            rolled_damage_by_type.update({damage_type: damage_type_damage})

            rolled_damage += damage_type_damage

        rolled_damage_dealt = dict.copy(rolled_damage_by_type)

        for damage_type in rolled_damage_dealt.keys():

            rolled_damage_dealt[damage_type] *= (
                1 - target_resistances[damage_type])

            if damage_type == "physical":
                rolled_damage_dealt[damage_type] -= self.armor

            rolled_damage_dealt[damage_type] = int(
                round(rolled_damage_dealt[damage_type]))

        total_damage_dealt = 0

        for damage in rolled_damage_dealt.values():
            total_damage_dealt += damage

        print("total_damage dealt is", total_damage_dealt)

        messages = {
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

        if critical_seed >= 0.95:
            results.append({
                "message":
                messages["monster_critical_miss"]
                if self.owner.ai else messages["player_critical_miss"]
            })
            self.energy -= 50

        elif critical_seed <= self.critical_hit_chance and total_damage_dealt > 0:

            results.append({
                "message":
                messages["monster_critical_hit"]
                if self.owner.ai else messages["player_critical_hit"]
            })

            for effect in self.status_effects:
                if effect.on_deal_damage:
                    results.extend(
                        effect.on_deal_damage(effect,
                                              target=target,
                                              damage_dealt=total_damage_dealt))

            results.extend(
                target.fighter.take_damage(rolled_damage_by_type,
                                           attacker=self))

            if not self.owner.ai:
                self.energy += 25

        elif critical_seed <= self.critical_hit_chance and total_damage_dealt <= 0:

            results.append({
                "message":
                messages["monster_critical_hit_no_damage"]
                if self.owner.ai else messages["player_critical_hit_no_damage"]
            })

            if not self.owner.ai:
                self.energy += 25

        elif dice_roll >= target_roll:
            if total_damage_dealt > 0:

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

                results.extend(
                    target.fighter.take_damage(rolled_damage_by_type,
                                               attacker=self))
            else:

                results.append({
                    "message":
                    messages["monster_no_damage"]
                    if self.owner.ai else messages["player_no_damage"]
                })
        else:
            results.append({
                "message":
                messages["monster_miss"]
                if self.owner.ai else messages["player_miss"]
            })
        print("rolled damage by type is", rolled_damage_by_type)
        return results
