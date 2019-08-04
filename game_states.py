from enum import Enum, auto


class GameStates(Enum):
    GAME_TURN = auto()
    PLAYERS_TURN = auto()
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()
    SHOW_INVENTORY = auto()
    SHOW_EQUIPMENT = auto()
    DROP_INVENTORY = auto()
    DROP_EQUIPMENT = auto()
    TARGETING = auto()
    LEVEL_UP = auto()
    CHARACTER_SCREEN = auto()