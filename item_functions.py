import tcod

from game_messages import Message
from components.ai import ConfusedMonster
from components.status_effects import Fireball
from utils import disk
from effect import GFX_Effect


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.current_hp == entity.fighter.max_hp:
        results.append({
            'consumed':
            False,
            'message':
            Message('You are already at full health', "yellow")
        })
    else:
        results.append({"heal": amount})
        results.append({
            'consumed':
            True,
            'message':
            Message('Your wounds start to feel better!', "green")
        })

    return results


def cast_chaos_bolt(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get("entities")
    game_map = kwargs.get("game_map")
    damage = kwargs.get("damage")
    maximum_range = kwargs.get("maximum_range")

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and game_map.fov[entity.
                                                                x, entity.y]:
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({
            "consumed":
            True,
            "target":
            target,
            "message":
            Message(
                f"A bolt of entropic energies strikes the {target.name} for {damage} damage!",
                "#990000")
        })
        results.extend(target.fighter.take_damage(damage))
        game_map.gfx_effects.append(
            GFX_Effect(target.x, target.y, gfx_effect_tile=0x1009))
    else:
        results.append({
            "consumed":
            False,
            "target":
            None,
            "message":
            Message("There are no enemies in range.", "red")
        })

    return results


def cast_fireball(*args, **kwargs):

    caster = args[0]
    entities = kwargs.get("entities")
    game_map = kwargs.get("game_map")
    damage = kwargs.get("damage")
    radius = kwargs.get("radius")
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")

    results = []

    if not game_map.fov[target_x, target_y]:
        results.append({
            "consumed":
            False,
            "message":
            Message("You cannot target a tile outside your line of sight.",
                    "yellow")
        })
        return results

    results.append({
        "consumed":
        True,
        "message":
        Message(f"Your ears ring as the fireball explodes in roaring flames!")
    })

    target_area = disk(target_x, target_y, radius)

    for entity in entities:
        if entity.fighter and (entity.x, entity.y) in target_area:
            results.append({
                "message":
                Message(f"The {entity.name} is engulfed in flames!", "orange")
            })
            results.extend(
                entity.fighter.apply_effect(Fireball, effect_caster=caster))

    for map_coordinates in target_area:
        game_map.gfx_effects.append(
            GFX_Effect(map_coordinates[0],
                       map_coordinates[1],
                       gfx_effect_tile=0x1008))

    return results


def cast_confuse(*args, **kwargs):
    entities = kwargs.get("entities")
    game_map = kwargs.get("game_map")
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")

    results = []

    if not game_map.fov[target_x, target_y]:
        results.append({
            "consumed":
            False,
            "message":
            Message("You cannot target a tile outside your line of sight.",
                    "yellow")
        })
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({
                "consumed":
                True,
                "message":
                Message(
                    f"The eyes of the {entity.name} look vacant as it starts to stumble around!",
                    "light green")
            })

            break
    else:
        results.append({
            "consumed":
            False,
            "message":
            Message("There is no targetable enemy at that location.", "yellow")
        })

    return results


def ranged_attack(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get("entities")
    game_map = kwargs.get("game_map")
    ranged_weapon_type = kwargs.get("ranged_weapon_type")
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")
    results = []

    if not game_map.fov[target_x, target_y]:
        results.append({
            "consumed":
            False,
            "message":
            Message("You cannot target a tile outside your line of sight.",
                    "yellow")
        })
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            fire_ranged_weapon_messages = {
                "bow": f"You fire your bow at the {entity.name}!",
                "crossbow": f"You fire your crossbow at the {entity.name}!",
                "pistol": f"You fire your pistol at the {entity.name}!",
                "rifle": f"You fire your rifle at the {entity.name}!",
            }
            results.append({
                "consumed":
                True,
                "message":
                Message(fire_ranged_weapon_messages[ranged_weapon_type])
            })
            results.append({"ranged_attack": True})
            results.extend(caster.fighter.attack(entity, ranged=True))
            break
    else:
        results.append({
            "consumed":
            False,
            "message":
            Message("There is no targetable enemy at that location.", "yellow")
        })

    return results
