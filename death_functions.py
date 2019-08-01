import tcod
from game_states import GameStates
from bearlibterminal import terminal
from render_order import RenderOrder
from game_messages import Message


def kill_player(player):
    player.char = 0x1006
    player.color = terminal.color_from_name("dark red")

    return Message('You are killed!', "red"), GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = Message(f'{monster.name.capitalize()} is killed!',
                            "orange")

    monster.char = 0x1006
    monster.color = terminal.color_from_name("dark red")
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE
    return death_message