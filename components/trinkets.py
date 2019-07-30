material_names = [
    "copper", "silver", "gold", "steel", "voidstone", "ruby", "sapphire",
    "emerald", "pearlstone", "electrum", "diamons"
]

NECKLACE_names = [
    "pendant", "medallion", "necklace", "amulet", "collar", "torc", "locket"
]

RIGHT_RING_names = ["ring", "band", "signet"]
LEFT_RING_names = ["ring", "band", "signet"]


class Trinket:
    def __init__(self,
                 trinket_type=None,
                 unidentified_name=None,
                 indentified_name=None,
                 prefix=None,
                 suffix=None,
                 material=None,
                 quality=None):
        self.trinket_type = trinket_type
        self.unidentified_name = unidentified_name
        self.identified_name = identified_name
        self.prefix = prefix
        self.suffix = suffix
        self.material = material
        self.quality = quality
