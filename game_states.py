from enum import auto, Enum


class GameStates(Enum):
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