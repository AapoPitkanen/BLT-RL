from random import randint, random
from types import MethodType
from game_messages import Message
import tcod


class Effect():
    def __init__(self,
                 name,
                 duration=None,
                 start_message=None,
                 end_message=None,
                 resist_message=None,
                 resolve_message=None,
                 stacking_duration=True,
                 only_one_allowed=False,
                 modifiers=None,
                 owner=None,
                 resolve=None,
                 on_apply=None,
                 on_expire=None,
                 on_deal_damage=None,
                 on_take_damage=None,
                 on_attack=None,
                 on_attack_hit=None,
                 on_attack_miss=None,
                 on_critical_hit=None,
                 on_critical_miss=None,
                 effects_to_apply=None,
                 magnitudes=None):
        self.name = name
        self.duration = duration
        self.start_message = start_message
        self.end_message = end_message
        self.resist_message = resist_message
        self.resolve_message = resolve_message
        self.stacking_duration = stacking_duration
        self.only_one_allowed = only_one_allowed
        self.modifiers = modifiers
        self.owner = owner
        self.resolve = resolve
        self.on_apply = on_apply
        self.on_expire = on_expire
        self.on_deal_damage = on_deal_damage
        self.on_take_damage = on_take_damage
        self.on_attack = on_attack
        self.on_attack_hit = on_attack_hit
        self.on_attack_miss = on_attack_miss
        self.on_critical_hit = on_critical_hit
        self.on_critical_miss = on_critical_miss
        # Dict of lists to apply on different triggers, such as on critical hits
        # or on effect expirations. Example:
        # {
        #    "on_critical_hit": [Effect1, Effect2],
        #    "on_take_damage": [Effect3]
        # }
        self.effects_to_apply = effects_to_apply
        self.magnitudes = magnitudes


# DEBUG KILL ON APPLY


def on_apply_kill_target(self):
    results = []
    results.append({"take_damage": {"physical": 10000}})
    return results


def KillTarget():
    KillTarget = Effect(name="kill_target",
                        duration=0,
                        on_apply=on_apply_kill_target)
    return KillTarget


def TouchOfDeath():
    TouchOfDeath = Effect(
        name="touch_of_death",
        on_deal_damage=on_deal_damage_apply_effects_to_target,
        effects_to_apply={"on_deal_damage": [KillTarget]})
    return TouchOfDeath


def DealDurationDamage():
    DealDurationDamage = Effect(name="deal_duration_damage",
                                duration=20,
                                start_message={
                                    "player": {
                                        "message":
                                        "You feel your innards bursting!",
                                        "message_color": "purple"
                                    },
                                    "monster": {
                                        "message":
                                        " starts to bleed all over!",
                                        "message_color": "purple"
                                    }
                                },
                                resolve=resolve_poison,
                                only_one_allowed=True,
                                stacking_duration=False)
    return DealDurationDamage


def OnHitApplyDurationDamage():
    OnHitApplyDurationDamage = Effect(
        name="on_hit_apply_duration_damage",
        on_deal_damage=on_deal_damage_apply_effects_to_target,
        effects_to_apply={"on_deal_damage": [DealDurationDamage]})
    return OnHitApplyDurationDamage


# General on attack handler to add effects to target before attack results are resolved
def on_attack_apply_effects_to_target(self, target):
    results = []
    for effect in self.effects_to_apply.get("on_attack", []):
        results.extend(target.fighter.apply_effect(effect))
    return results


# General on take damage handler to add effects when damage is taken
def on_take_damage_apply_effects(self):
    results = []
    for effect in self.effects_to_apply.get("on_take_damage", []):
        results.extend(self.owner.fighter.apply_effect(effect))
    return results


# General on deal damage handler to add effects to self when damage is dealt
def on_deal_damage_apply_effects_to_target(self, **kwargs):
    results = []
    target = kwargs.get("target")

    for effect in self.effects_to_apply.get("on_deal_damage", []):
        results.extend(target.fighter.apply_effect(effect))
    return results


def on_deal_damage_apply_effects_to_self(self, **kwargs):
    results = []
    for effect in self.effects_to_apply.get("on_deal_damage", []):
        results.extend(self.owner.fighter.apply_effect(effect))
    return results


# General on effect apply handler to add more effects when effect is applied
def on_apply_apply_effects(self):
    results = []
    for effect in self.effects_to_apply.get("on_apply", []):
        results.extend(self.owner.fighter.apply_effect(effect))
    return results


# General critical hit handler to add effects on critical hit
def on_critical_hit_apply_effects(self):
    results = []
    for effect in self.effects_to_apply.get("on_critical_hit", []):
        results.extend(self.owner.fighter.apply_effect(effect))
    return results


# General critical miss handler to add effects on critical miss
def on_critical_hit_apply_effects(self):
    results = []
    for effect in self.effects_to_apply.get("on_critical_miss", []):
        results.extend(self.owner.fighter.apply_effect(effect))
    return results


# General expire handler to add effects on effect expiration
def on_expire_apply_effects(self):
    results = []
    for effect in self.effects_to_apply.get("on_expire", []):
        results.extend(self.owner.fighter.apply_effect(effect))
    return results


# General heal resolver
def resolve_heal_effect(self):
    results = []
    heal_amount = self.magnitudes.get("heal", 0)
    results.append({"heal": heal_amount})
    return results


# General effect resolver that just decrements duration
def general_duration_resolve(self):
    results = []
    if self.duration > 0:
        results.append({"duration": -1})
    return results


# LIFE STEAL


def on_deal_damage_lifesteal(self, **kwargs):
    results = []
    fighter = self.owner.fighter
    damage_dealt = kwargs.get("damage_dealt")
    target = kwargs.get("target")
    healed_amount = int(round(fighter.life_steal * damage_dealt))
    if healed_amount > 0:
        results.append({"heal": healed_amount})
        if self.owner.ai:
            message = f"The {self.owner.name} {self.resolve_message['monster']['message']}"
            results.append({
                "message":
                Message(message,
                        self.resolve_message['monster']['message_color'])
            })
        else:
            message = f"{self.resolve_message['player']['message']} {target.name}!"
            results.append({
                "message":
                Message(message,
                        self.resolve_message['player']['message_color'])
            })
    return results


def LifeSteal():
    LifeSteal = Effect("life_steal",
                       on_deal_damage=on_deal_damage_lifesteal,
                       resolve_message={
                           "player": {
                               "message": "You steal the life force of the",
                               "message_color": "light green"
                           },
                           "monster": {
                               "message": "steals your life force!",
                               "message_color": "red"
                           }
                       })
    return LifeSteal


# NATURAL REGENERATION


def resolve_natural_regeneration(self):
    results = []
    fighter = self.owner.fighter
    fighter.turns_to_natural_regenerate += 1
    if fighter.turns_to_natural_regenerate == fighter.natural_hp_regeneration_speed:
        results.append({"heal": 1})
        fighter.turns_to_natural_regenerate = 0
    return results


def NaturalRegeneration():
    NaturalRegeneration = Effect("natural_regeneration",
                                 resolve=resolve_natural_regeneration)
    return NaturalRegeneration


static_effects = [NaturalRegeneration, LifeSteal]

# SLOW #


def resolve_slow(self):
    results = []
    if self.duration > 0:
        results.append({"duration": -1})
    return results


def Slow():
    Slow = Effect("slow",
                  10,
                  start_message={
                      "player": {
                          "message": "Your movements slow down!",
                          "message_color": "purple"
                      },
                      "monster": {
                          "message": "'s movements seem to slow down!",
                          "message_color": "light purple"
                      }
                  },
                  end_message={
                      "player": {
                          "message": "Your movements speed up again!",
                          "message_color": "light green"
                      },
                      "monster": {
                          "message": "'s movements seem to speed up again!",
                          "message_color": "yellow"
                      }
                  },
                  modifiers={"speed_modifier": -50},
                  resolve=resolve_slow)
    return Slow


# POISON #


def resolve_poison(self):
    results = []
    poison_seed = random()
    if self.duration > 0:
        results.append({"duration": -1})
    if poison_seed > self.owner.fighter.resistances["poison"]:
        results.append({"take_damage": {"poison": randint(1, 6)}})
    else:
        if self.owner.ai:
            results.append({
                "message":
                Message(
                    f"The {self.owner.name} {self.resist_message['monster']}",
                    self.resist_message['monster']['message_color'])
            })
        else:
            results.append({
                "message":
                Message(f"{self.resist_message['player']['message']}",
                        self.resist_message['player']['message_color'])
            })
    return results


def Poison():
    Poison = Effect(name="poison",
                    duration=randint(3, 6),
                    start_message={
                        "player": {
                            "message": "You are poisoned!",
                            "message_color": "dark green"
                        },
                        "monster": {
                            "message": " is poisoned!",
                            "message_color": "dark green"
                        }
                    },
                    end_message={
                        "player": {
                            "message": "You feel the poison wearing off!",
                            "message_color": "lighter green"
                        },
                        "monster": {
                            "message": " is no longer poisoned!",
                            "message_color": "yellow"
                        }
                    },
                    resist_message={
                        "player": {
                            "message": "You resist the effects of the poison!",
                            "message_color": "light green"
                        },
                        "monster": {
                            "message":
                            " doesn't seem to be affected by the poison!",
                            "message_color": "red"
                        }
                    },
                    resolve=resolve_poison)
    return Poison


# INTERNAL TRAUMA


def resolve_internal_trauma(self):
    results = []
    if self.duration > 0:
        results.append({"duration": -1})
    if self.duration % 2 == 0:
        results.append({"take_damage": {"physical": randint(1, 2)}})


def InternalTrauma():
    InternalTrauma = Effect(
        "internal_trauma",
        randint(4, 8),
        start_message={
            "player": {
                "message": "One of your internal organs is crushed!",
                "message_color": "#A80800"
            },
            "monster": {
                "message": " is visibly shaken by the force of your attack!",
                "message_color": "#A80800"
            }
        },
        end_message={
            "player": {
                "message": "You feel slightly better now.",
                "message_color": "light green"
            },
            "monster": {
                "message": " regains its composure!",
                "message_color": "yellow"
            }
        },
        modifiers={})


# BLEED #


def resolve_bleed(self):
    results = []
    if self.duration > 0:
        results.append({"duration": -1})
    results.append({"take_damage": {"physical": 1}})
    return results


def Bleed():
    Bleed = Effect("bleed",
                   randint(2, 6),
                   start_message={
                       "player": {
                           "message": "Your wounds start to bleed!",
                           "message_color": "dark red"
                       },
                       "monster": {
                           "message": "'s wounds start to bleed!",
                           "message_color": "red"
                       }
                   },
                   end_message={
                       "player": {
                           "message": "The bleeding suddenly stops!",
                           "message_color": "light red"
                       },
                       "monster": {
                           "message": " is no longer bleeding!",
                           "message_color": "yellow"
                       }
                   },
                   stacking_duration=False,
                   resolve=resolve_bleed)
    return Bleed


# BURN #


def resolve_burn(self):
    results = []
    burn_seed = random()
    if self.duration > 0:
        results.append({"duration": -1})
    if burn_seed > self.owner.fighter.resistances["fire"]:
        results.append({"take_damage": {"fire": self.duration + 1}})
    else:
        if self.owner.ai:
            results.append({
                "message":
                Message(
                    f"The {self.owner.name} {self.resist_message['monster']}",
                    self.resist_message['monster']['message_color'])
            })
        else:
            results.append({
                "message":
                Message(f"{self.resist_message['player']['message']}",
                        self.resist_message['player']['message_color'])
            })
    return results


def Burn():
    Burn = Effect(
        "burn",
        randint(2, 4),
        start_message={
            "player": {
                "message": "You burst into flames!",
                "message_color": "flame"
            },
            "monster": {
                "message": " bursts into flames!",
                "message_color": "flame"
            }
        },
        end_message={
            "player": {
                "message": "The flames around you dissipate!",
                "message_color": "light flame"
            },
            "monster": {
                "message": " is no longer burning!",
                "message_color": "yellow"
            }
        },
        resist_message={
            "player": {
                "message": "You resist the searing flames!",
                "message_color": "light green"
            },
            "monster": {
                "message":
                " doesn't seem to be affected by the searing flames!",
                "message_color": "red"
            }
        },
        resolve=resolve_burn)
    return Burn


# CHILLED #


def resolve_chilled(self):
    results = []
    chill_seed = random()

    if chill_seed > self.owner.fighter.resistances["ice"]:
        if self.duration > 0:
            results.append({"duration": -1})
    else:
        if self.owner.ai:
            results.append({
                "message":
                Message(
                    f"The {self.owner.name} {self.resist_message['monster']}",
                    self.resist_message['monster']['message_color'])
            })
            results.append({"duration_reset": True})
        else:
            results.append({
                "message":
                Message(f"{self.resist_message['player']['message']}",
                        self.resist_message['player']['message_color'])
            })
            results.append({"duration_reset": True})
    return results


def Chilled():
    Chilled = Effect(
        "chilled",
        randint(2, 6),
        start_message={
            "player": {
                "message": "The freezing cold slows down your movements!",
                "message_color": "azure"
            },
            "monster": {
                "message": " slows down from the freezing cold!",
                "message_color": "light azure"
            }
        },
        end_message={
            "player": {
                "message": "You feel much warmer again!",
                "message_color": "lighter azure"
            },
            "monster": {
                "message": " is no longer slowed down from the cold!",
                "message_color": "yellow"
            }
        },
        resist_message={
            "player": {
                "message": "You resist freezing cold!",
                "message_color": "light green"
            },
            "monster": {
                "message":
                " doesn't seem to slow down from the freezing cold!",
                "message_color": "red"
            }
        },
        modifiers={
            "attack_energy_bonus_modifier": -25,
            "movement_energy_bonus_modifier": -25
        },
        resolve=resolve_chilled)
    return Chilled


# ARMOR NEGATION


def ArmorNegated():
    ArmorNegated = Effect(name="armor_negated",
                          duration=0,
                          modifiers={"armor_modifier": -999})
    return ArmorNegated


def IgnoreArmor():
    IgnoreArmor = Effect(name="ignore_armor",
                         on_attack=on_attack_apply_effects_to_target,
                         effects_to_apply={"on_attack": [ArmorNegated]})
    return IgnoreArmor


# GENERAL EFFECT RESOLVER #


def resolve_effects(fighter):
    results = []

    for effect in fighter.status_effects:
        if fighter.current_hp > 0 and effect.resolve:
            effect_results = effect.resolve(effect)
            for result in effect_results:
                heal = result.get("heal")
                duration = result.get("duration")
                duration_reset = result.get("duration_reset")
                take_damage = result.get("take_damage")
                message = result.get("message")

                if heal:
                    fighter.heal(heal)

                if duration:
                    effect.duration += duration

                if duration_reset:
                    effect.duration = 0

                if take_damage:
                    results.extend(
                        fighter.take_damage(take_damage, from_effect=True))

                if message:
                    results.append({"message": message})

        if effect.duration is not None and effect.duration == 0:

            if effect.on_expire:
                results.extend(effect.on_expire(effect))

            fighter.status_effects.remove(effect)

            if fighter.current_hp > 0 and effect.end_message:

                if fighter.owner.ai:
                    results.append({
                        "message":
                        Message(
                            f"The {fighter.owner.name}{effect.end_message['monster']['message']}",
                            effect.end_message['monster']['message_color'])
                    })

                else:
                    results.append({
                        "message":
                        Message(f"{effect.end_message['player']['message']}",
                                effect.end_message['player']['message_color'])
                    })
    return results


status_effects_by_damage_type = {
    "physical": Bleed,
    "fire": Burn,
    "ice": Chilled,
    "lightning": Bleed,
    "holy": Bleed,
    "chaos": Bleed,
    "arcane": Slow,
    "poison": Poison
}
