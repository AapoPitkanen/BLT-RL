from enum import Enum, auto


class RenderLayer(Enum):
    # Layers for the terminal
    MAP = auto()
    ENTITIES = auto()
    OVERLAY = auto()
    HUD = auto()
    MENU = auto()
    MENU_ICON = auto()


class RenderOrder(Enum):
    # Entities are rendered in this order.
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


class Visible(Enum):
    # Visibility levels used in map rendering

    HIDDEN = auto()
    IN_FOV = auto()
    EXPLORED = auto()
    BOUNDARY = auto()
