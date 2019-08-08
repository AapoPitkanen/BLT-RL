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
                 stacking=True,
                 modifiers=None,
                 owner=None,
                 resolve=None,
                 on_apply=None,
                 on_expire=None,
                 on_deal_damage=None,
                 on_take_damage=None,
                 on_critical_hit=None,
                 on_critical_miss=None):
        self.name = name
        self.duration = duration
        self.start_message = start_message
        self.end_message = end_message
        self.resist_message = resist_message
        self.resolve_message = resolve_message
        self.stacking = stacking
        self.modifiers = modifiers
        self.owner = owner
        self.resolve = resolve
        self.on_apply = on_apply
        self.on_expire = on_expire
        self.on_deal_damage = on_deal_damage
        self.on_take_damage = on_take_damage
        self.on_critical_hit = on_critical_hit
        self.on_critical_miss = on_critical_miss


def resolve_curse_of_frailty(self):
    results = []
    if self.duration > 0:
        results.append({"duration": -1})
    return results


def CurseOfFrailty():
    CurseOfFrailty = Effect("curse_of_frailty",
                            duration=10,
                            resolve=resolve_curse_of_frailty,
                            modifiers={"resistances": {
                                "physical": -0.5
                            }})
    return CurseOfFrailty


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
                  10, {
                      "player": {
                          "message": "Your movements slow down!",
                          "message_color": "purple"
                      },
                      "monster": {
                          "message": "'s movements seem to slow down!",
                          "message_color": "light purple"
                      }
                  }, {
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
    Poison = Effect("poison",
                    randint(3, 6),
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
                   stacking=False,
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
