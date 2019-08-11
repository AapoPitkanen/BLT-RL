from enum import Enum, auto


class EquipmentSlots(Enum):
    HEAD = auto()
    SHOULDERS = auto()
    CLOAK = auto()
    NECKLACE = auto()
    TORSO = auto()
    LEGS = auto()
    WRISTS = auto()
    GLOVES = auto()
    BOOTS = auto()
    RIGHT_RING = auto()
    LEFT_RING = auto()
    MAIN_HAND = auto()
    OFF_HAND = auto()


equipment_slot_armor_list = [
    EquipmentSlots.HEAD, EquipmentSlots.SHOULDERS, EquipmentSlots.TORSO,
    EquipmentSlots.LEGS, EquipmentSlots.WRISTS, EquipmentSlots.GLOVES,
    EquipmentSlots.BOOTS, EquipmentSlots.OFF_HAND
]

equipment_slot_trinket_list = [
    EquipmentSlots.CLOAK, EquipmentSlots.NECKLACE, EquipmentSlots.RIGHT_RING,
    EquipmentSlots.LEFT_RING
]