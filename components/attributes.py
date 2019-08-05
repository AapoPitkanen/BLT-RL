import random

attribute_modifier_values = {
    1: -5,
    2: -4,
    3: -4,
    4: -3,
    5: -3,
    6: -2,
    7: -2,
    8: -1,
    9: -1,
    10: 0,
    11: 0,
    12: 1,
    13: 1,
    14: 2,
    15: 2,
    16: 3,
    17: 3,
    18: 4,
    19: 4,
    20: 5,
    21: 5,
    22: 6,
    23: 6,
    24: 7,
    25: 7,
    26: 8,
    27: 8,
    28: 9,
    29: 9,
    30: 10,
    31: 10,
    32: 11,
    33: 11,
    34: 12,
    35: 12,
    36: 13,
    37: 13,
    38: 14,
    39: 14,
    40: 15,
    41: 15,
    42: 16,
    43: 16,
    44: 17,
    45: 17,
    46: 18,
    47: 18,
    48: 19,
    49: 19,
    50: 20,
    51: 20,
    52: 21,
    53: 21,
    54: 22,
    55: 22,
    56: 23,
    57: 23,
    58: 24,
    59: 24,
    60: 25
}


class Attribute:
    def __init__(self, attribute_name: str, attribute_short: str,
                 attribute_value: int, attribute_modifier: int):
        self.attribute_name = attribute_name
        self.attribute_short = attribute_short
        self.attribute_value = attribute_value
        self.attribute_modifier = attribute_modifier


class Attributes:
    def __init__(self, STR: Attribute, PER: Attribute, DEX: Attribute,
                 CON: Attribute, INT: Attribute, WIS: Attribute,
                 CHA: Attribute, LCK: Attribute):
        self.STR = STR
        self.PER = PER
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA
        self.LCK = LCK


def generate_attributes(STR_value: int, PER_value: int, DEX_value: int,
                        CON_value: int, INT_value: int, WIS_value: int,
                        CHA_value: int, LCK_value: int) -> Attributes:

    return Attributes(
        Attribute("Strength", "STR", STR_value,
                  attribute_modifier_values[STR_value]),
        Attribute("Perception", "PER", PER_value,
                  attribute_modifier_values[STR_value]),
        Attribute("Dexterity", "DEX", DEX_value,
                  attribute_modifier_values[DEX_value]),
        Attribute("Constitution", "CON", CON_value,
                  attribute_modifier_values[CON_value]),
        Attribute("Intelligence", "INT", INT_value,
                  attribute_modifier_values[INT_value]),
        Attribute("Wisdom", "WIS", WIS_value,
                  attribute_modifier_values[WIS_value]),
        Attribute("Charisma", "CHA", CHA_value,
                  attribute_modifier_values[CHA_value]),
        Attribute("Luck", "LCK", CHA_value,
                  attribute_modifier_values[CHA_value]))


def roll_character_attributes() -> Attributes:
    attribute_names = ["STR", "PER", "DEX", "CON", "INT", "WIS", "CHA", "LCK"]
    attribute_values = {}
    for _i in range(0, 8):
        random_attribute_values = []
        for _j in range(0, 4):
            random_attribute_values.append(random.randint(1, 6))
        random_attribute_values.remove(min(random_attribute_values))
        attribute_values[attribute_names[_i]] = sum(random_attribute_values)
    return generate_attributes(
        attribute_values["STR"],
        attribute_values["PER"],
        attribute_values["DEX"],
        attribute_values["CON"],
        attribute_values["INT"],
        attribute_values["WIS"],
        attribute_values["CHA"],
        attribute_values["LCK"],
    )
