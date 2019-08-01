import tcod

from game_messages import Message
from components.ai import ConfusedMonster


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({
            'consumed':
            False,
            'message':
            Message('You are already at full health', "yellow")
        })
    else:
        entity.fighter.heal(amount)
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
                "crimson")
        })
        results.extend(target.fighter.take_damage(damage))
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
        Message(
            f"The fireball explodes in roaring flames, burning everything within {radius} tiles!"
        )
    })

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({
                "message":
                Message(
                    f"The {entity.name} is engulfed in flames and is burned for {damage} hit points!",
                    "orange")
            })
            results.extend(entity.fighter.take_damage(damage))

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