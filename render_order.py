from enum import Enum, auto


class RenderOrder(Enum):
    # Entities are rendered in this order.
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()