import tcod
from game_states import GameStates
from bearlibterminal import terminal
from render_order import RenderOrder
from game_messages import Message


def kill_player(player, game):
    player.char = 0x1006
    player.color = "dark red"
    game.fighter_entities.remove(player.fighter)
    return Message('You are killed!', "red"), GameStates.PLAYER_DEAD


def kill_monster(monster, game):
    death_message = Message(f'{monster.name.capitalize()} is killed!',
                            "orange")
    game.fighter_entities.remove(monster.fighter)
    game.monster_fighter_entities.remove(monster.fighter)
    monster.char = 0x1006
    monster.color = "dark_red"
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE
    return death_message