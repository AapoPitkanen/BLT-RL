from random import randint, random
from types import MethodType
from game_messages import Message
import tcod as libtcod


class Effect():
    def __init__(self,
                 name,
                 duration=None,
                 start_message=None,
                 end_message=None,
                 resist_message=None,
                 stacking=True,
                 modifiers=None,
                 owner=None):
        self.name = name
        self.duration = duration
        self.start_message = start_message
        self.end_message = end_message
        self.resist_message = resist_message
        self.stacking = stacking
        self.modifiers = modifiers
        self.owner = owner
        self.resolve_effect = None
        self.on_apply = None


# SLOW #


def resolve_slow(self):
    if self.duration > 0:
        self.duration -= 1


def Slow():
    Slow = Effect("slow",
                  10, {
                      "player": {
                          "message": "Your movements slow down!",
                          "message_color": libtcod.purple
                      },
                      "monster": {
                          "message": "'s movements seem to slow down!",
                          "message_color": libtcod.light_purple
                      }
                  }, {
                      "player": {
                          "message": "Your movements speed up again!",
                          "message_color": libtcod.light_green
                      },
                      "monster": {
                          "message": "'s movements seem to speed up again!",
                          "message_color": libtcod.yellow
                      }
                  },
                  modifiers=[["speed_modifier", -50]])
    Slow.resolve_effect = MethodType(resolve_slow, Slow)
    Slow.on_apply = MethodType(on_apply_modifiers, Slow)
    return Slow


# POISON #


def resolve_poison(self):
    results = []
    poison_seed = random()
    if self.duration > 0:
        self.duration -= 1
    if poison_seed > self.owner.fighter.resistances["poison"]:
        results.extend(self.owner.fighter.take_damage(randint(1, 6)))
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
                            "message_color": libtcod.dark_green
                        },
                        "monster": {
                            "message": " is poisoned!",
                            "message_color": libtcod.dark_green
                        }
                    },
                    end_message={
                        "player": {
                            "message": "You feel the poison wearing off!",
                            "message_color": libtcod.lighter_green
                        },
                        "monster": {
                            "message": " is no longer poisoned!",
                            "message_color": libtcod.yellow
                        }
                    },
                    resist_message={
                        "player": {
                            "message": "You resist the effects of the poison!",
                            "message_color": libtcod.light_green
                        },
                        "monster": {
                            "message":
                            " doesn't seem to be affected by the poison!",
                            "message_color": libtcod.red
                        }
                    })
    Poison.resolve_effect = MethodType(resolve_poison, Poison)
    return Poison


# BLEED #


def resolve_bleed(self):
    if self.duration > 0:
        self.duration -= 1
    return self.owner.fighter.take_damage(1)


def Bleed():
    Bleed = Effect("bleed",
                   randint(2, 6),
                   start_message={
                       "player": {
                           "message": "Your wounds start to bleed!",
                           "message_color": libtcod.dark_red
                       },
                       "monster": {
                           "message": "'s wounds start to bleed!",
                           "message_color": libtcod.red
                       }
                   },
                   end_message={
                       "player": {
                           "message": "The bleeding suddenly stops!",
                           "message_color": libtcod.light_red
                       },
                       "monster": {
                           "message": " is no longer bleeding!",
                           "message_color": libtcod.yellow
                       }
                   },
                   stacking=False)
    Bleed.resolve_effect = MethodType(resolve_bleed, Bleed)
    return Bleed


# BURN #


def resolve_burn(self):
    results = []
    burn_seed = random()
    if self.duration > 0:
        self.duration -= 1
    if burn_seed > self.owner.fighter.resistances["fire"]:
        results.extend(self.owner.fighter.take_damage(self.duration + 1))
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
                "message_color": libtcod.flame
            },
            "monster": {
                "message": " bursts into flames!",
                "message_color": libtcod.flame
            }
        },
        end_message={
            "player": {
                "message": "The flames around you dissipate!",
                "message_color": libtcod.light_flame
            },
            "monster": {
                "message": " is no longer burning!",
                "message_color": libtcod.yellow
            }
        },
        resist_message={
            "player": {
                "message": "You resist the searing flames!",
                "message_color": libtcod.light_green
            },
            "monster": {
                "message":
                " doesn't seem to be affected by the searing flames!",
                "message_color": libtcod.red
            }
        })
    Burn.resolve_effect = MethodType(resolve_burn, Burn)
    return Burn


# CHILLED #


def resolve_chilled(self):
    results = []
    chill_seed = random()

    if chill_seed > self.owner.fighter.resistances["fire"]:
        if self.duration > 0:
            self.duration -= 1
    else:
        if self.owner.ai:
            results.append({
                "message":
                Message(
                    f"The {self.owner.name} {self.resist_message['monster']}",
                    self.resist_message['monster']['message_color'])
            })
            self.duration = 0
        else:
            results.append({
                "message":
                Message(f"{self.resist_message['player']['message']}",
                        self.resist_message['player']['message_color'])
            })
            self.duration = 0
    return results


def Chilled():
    Chilled = Effect(
        "chilled",
        randint(2, 6),
        start_message={
            "player": {
                "message": "The freezing cold slows down your movements!",
                "message_color": libtcod.azure
            },
            "monster": {
                "message": " slows down from the freezing cold!",
                "message_color": libtcod.light_azure
            }
        },
        end_message={
            "player": {
                "message": "You feel much warmer again!",
                "message_color": libtcod.lighter_azure
            },
            "monster": {
                "message": " is no longer slowed down from the cold!",
                "message_color": libtcod.yellow
            }
        },
        resist_message={
            "player": {
                "message": "You resist freezing cold!",
                "message_color": libtcod.light_green
            },
            "monster": {
                "message":
                " doesn't seem to slow down from the freezing cold!",
                "message_color": libtcod.red
            }
        },
        modifiers=[["movement_cost_modifier", 1000],
                   ["attack_cost_modifier", 1000]])
    Chilled.resolve_effect = MethodType(resolve_chilled, Chilled)
    Chilled.on_apply = MethodType(on_apply_modifiers, Chilled)
    return Chilled


# GENERAL EFFECT RESOLVER #


def resolve_effects(fighter):
    results = []
    for effect in fighter.status_effects:
        if fighter.current_hp > 0 and effect.resolve_effect and effect.duration > 0:
            resolve_effect_result = effect.resolve_effect()
            if resolve_effect_result is not None:
                results.extend(effect.resolve_effect())
        if effect.duration == 0:
            fighter.status_effects.remove(effect)
            if effect.modifiers:
                for modifier_name, modifier_value in effect.modifiers:
                    fighter.temporary_modifiers[
                        modifier_name] -= modifier_value
            if fighter.current_hp > 0:
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


# GENERAL "ON APPLY" FUNCTION FOR MODIFIERS


def on_apply_modifiers(self):
    for modifier_name, modifier_value in self.modifiers:
        self.owner.fighter.temporary_modifiers[modifier_name] += modifier_value


status_effects_by_damage_type = {
    "physical": Bleed,
    "fire": Burn,
    "ice": Chilled,
    "lightning": Bleed,
    "holy": Bleed,
    "chaos": Bleed,
    "arcane": Bleed,
    "poison": Poison
}
