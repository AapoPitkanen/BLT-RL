class Ammunition:
    def __init__(
            self,
            rarity=None,
            ammunition_name=None,
            material=None,
            quality=None,
    ):
        self.rarity = rarity
        self.ammunition_name = ammunition_name
        self.material = material
        self.quality = quality
        self.unidentified_name = f"{self.material.title()} {self.ammunition_name}"
        self.identified_name = f"{self.material.title()} {self.ammunition_name.title()}{' (' + quality + ')' if quality != 'normal' else ''}"
