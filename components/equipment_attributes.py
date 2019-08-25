# GENERAL EQUIPMENT ATTRIBUTES

rarities = {
    "rarity_levels": [
        "normal",
        "common",
        "uncommon",
        "rare",
        "epic",
        "mythical",
    ],
    "rarity_weights": [
        0.535,
        0.255,
        0.125,
        0.055,
        0.029,
        0.001,
    ],
    "rarity_colors": {
        "normal": "white",
        "common": "green",
        "uncommon": "#308CE8",
        "rare": "#FFD700",
        "epic": "#E600E6",
        "mythical": "red"
    },
    "rarity_modifier_counts": {
        "normal": 0,
        "common": 1,
        "uncommon": 2,
        "rare": 3,
        "epic": 4,
        "mythical": 5
    }
}

qualities = [
    "abysmal",
    "awful",
    "bad",
    "poor",
    "fair",
    "normal",
    "fine",
    "good",
    "superior",
    "excellent",
    "exceptional",
    "exquisite",
    "flawless",
]

quality_weights = [
    0.0075,
    0.0125,
    0.025,
    0.05,
    0.1,
    0.5,
    0.15,
    0.0825,
    0.04,
    0.0225,
    0.01,
    0.00375,
    0.001875,
]

# ARMOR ATTRIBUTES

armor_material_names_and_weights = [{
    "name": "hide",
    "weight": 0.1
}, {
    "name": "leather",
    "weight": 0.11
}, {
    "name": "boiled leather",
    "weight": 0.09
}, {
    "name": "studded leather",
    "weight": 0.08
}, {
    "name": "reinforced leather",
    "weight": 0.06
}, {
    "name": "shadowed leather",
    "weight": 0.05
}, {
    "name": "copper",
    "weight": 0.12
}, {
    "name": "bronze",
    "weight": 0.11
}, {
    "name": "iron",
    "weight": 0.1
}, {
    "name": "steel",
    "weight": 0.08
}, {
    "name": "truesteel",
    "weight": 0.01
}, {
    "name": "darksteel",
    "weight": 0.02
}, {
    "name": "orichalcum",
    "weight": 0.02
}, {
    "name": "mithril",
    "weight": 0.02
}, {
    "name": "voidstone",
    "weight": 0.0045
}, {
    "name": "brimstone",
    "weight": 0.0045
}, {
    "name": "cold iron",
    "weight": 0.0045
}, {
    "name": "thunderstone",
    "weight": 0.0045
}, {
    "name": "pearlstone",
    "weight": 0.0045
}, {
    "name": "electrum",
    "weight": 0.0045
}, {
    "name": "adamantine",
    "weight": 0.0005
}, {
    "name": "meteoric iron",
    "weight": 0.0025
}]

armor_material_names = [
    material["name"] for material in armor_material_names_and_weights
]
armor_material_weights = [
    material["weight"] for material in armor_material_names_and_weights
]

armor_prefix_names_and_weights = [{
    "name": "Tempered",
    "weight": 0.12
}, {
    "name": "Hardened",
    "weight": 0.06
}, {
    "name": "Unbreakable",
    "weight": 0.03
}, {
    "name": "Indestructible",
    "weight": 0.015
}, {
    "name": "Healing",
    "weight": 0.08
}, {
    "name": "Vampiric",
    "weight": 0.05
}, {
    "name": "Swift",
    "weight": 0.08
}, {
    "name": "Quick",
    "weight": 0.04
}, {
    "name": "Targeting",
    "weight": 0.08
}, {
    "name": "Lucky",
    "weight": 0.06
}, {
    "name": "Light",
    "weight": 0.06
}, {
    "name": "Impervious",
    "weight": 0.03
}, {
    "name": "Deadly",
    "weight": 0.025
}, {
    "name": "Vigilant",
    "weight": 0.05
}, {
    "name": "Blazing",
    "weight": 0.01
}, {
    "name": "Freezing",
    "weight": 0.01
}, {
    "name": "Shocking",
    "weight": 0.01
}, {
    "name": "Sanctified",
    "weight": 0.01
}, {
    "name": "Abyssal",
    "weight": 0.01
}, {
    "name": "Esoteric",
    "weight": 0.01
}, {
    "name": "Venomous",
    "weight": 0.01
}, {
    "name": "Agile",
    "weight": 0.025
}, {
    "name": "Stalwart",
    "weight": 0.025
}, {
    "name": "Robust",
    "weight": 0.025
}, {
    "name": "Astute",
    "weight": 0.025
}, {
    "name": "Enlightened",
    "weight": 0.025
}, {
    "name": "Appealing",
    "weight": 0.025
}]

armor_prefixes = [prefix["name"] for prefix in armor_prefix_names_and_weights]
armor_prefix_weights = [
    prefix["weight"] for prefix in armor_prefix_names_and_weights
]

armor_suffix_names_and_weights = [{
    "name": "of Spikes",
    "weight": 0.05
}, {
    "name": "of Thorns",
    "weight": 0.025
}, {
    "name": "of Retaliation",
    "weight": 0.0125
}, {
    "name": "of Strength",
    "weight": 0.025
}, {
    "name": "of the Juggernaut",
    "weight": 0.0125
}, {
    "name": "of the Hawk",
    "weight": 0.025
}, {
    "name": "of the Eagle",
    "weight": 0.0125
}, {
    "name": "of the Cat",
    "weight": 0.025
}, {
    "name": "of the Fox",
    "weight": 0.0125
}, {
    "name": "of Endurance",
    "weight": 0.025
}, {
    "name": "of Toughness",
    "weight": 0.0125
}, {
    "name": "of the Magi",
    "weight": 0.025
}, {
    "name": "of the Wizard",
    "weight": 0.0125
}, {
    "name": "of Wisdom",
    "weight": 0.025
}, {
    "name": "of Piety",
    "weight": 0.0125
}, {
    "name": "of Charisma",
    "weight": 0.025
}, {
    "name": "of the Silver Tongue",
    "weight": 0.0125
}, {
    "name": "of Fate",
    "weight": 0.025
}, {
    "name": "of Fortune",
    "weight": 0.0125
}, {
    "name": "of Defense",
    "weight": 0.09
}, {
    "name": "of the Rampart",
    "weight": 0.04
}, {
    "name": "of Protection",
    "weight": 0.09
}, {
    "name": "of the Fortress",
    "weight": 0.04
}, {
    "name": "of Longevity",
    "weight": 0.075
}, {
    "name": "of Health",
    "weight": 0.0525
}, {
    "name": "of Life",
    "weight": 0.025
}, {
    "name": "of Flames",
    "weight": 0.025
}, {
    "name": "of the Glacier",
    "weight": 0.025
}, {
    "name": "of Thunder",
    "weight": 0.025
}, {
    "name": "of the Heavens",
    "weight": 0.025
}, {
    "name": "of the Void",
    "weight": 0.025
}, {
    "name": "of the Arcane",
    "weight": 0.025
}, {
    "name": "of Toxins",
    "weight": 0.025
}, {
    "name": "of Alacrity",
    "weight": 0.025
}, {
    "name": "of Evasion",
    "weight": 0.03
}, {
    "name": "of Regeneration",
    "weight": 0.01
}]
armor_suffixes = [suffix["name"] for suffix in armor_suffix_names_and_weights]
armor_suffix_weights = [
    suffix["weight"] for suffix in armor_suffix_names_and_weights
]

# WEAPON ATTRIBUTES

weapon_prefix_names_and_weights = [{
    "name": "Deadly",
    "weight": 0.05
}, {
    "name": "Blazing",
    "weight": 0.05
}, {
    "name": "Searing",
    "weight": 0.025
}, {
    "name": "Fireborn",
    "weight": 0.01
}, {
    "name": "Chilled",
    "weight": 0.05
}, {
    "name": "Freezing",
    "weight": 0.025
}, {
    "name": "Frostborn",
    "weight": 0.01
}, {
    "name": "Shocking",
    "weight": 0.05
}, {
    "name": "Charged",
    "weight": 0.025
}, {
    "name": "Thunderstruck",
    "weight": 0.01
}, {
    "name": "Holy",
    "weight": 0.05
}, {
    "name": "Sanctified",
    "weight": 0.025
}, {
    "name": "Sacred",
    "weight": 0.01
}, {
    "name": "Abyssal",
    "weight": 0.05
}, {
    "name": "Demonic",
    "weight": 0.025
}, {
    "name": "Infernal",
    "weight": 0.01
}, {
    "name": "Enchanted",
    "weight": 0.05
}, {
    "name": "Esoteric",
    "weight": 0.025
}, {
    "name": "Eldritch",
    "weight": 0.01
}, {
    "name": "Venomous",
    "weight": 0.05
}, {
    "name": "Toxic",
    "weight": 0.025
}, {
    "name": "Blighted",
    "weight": 0.01
}, {
    "name": "Relentless",
    "weight": 0.05
}, {
    "name": "Murderous",
    "weight": 0.05
}, {
    "name": "Masterwork",
    "weight": 0.05
}, {
    "name": "Nimble",
    "weight": 0.05
}, {
    "name": "Swift",
    "weight": 0.025
}, {
    "name": "Quick",
    "weight": 0.01
}, {
    "name": "Bloodthirsty",
    "weight": 0.05
}, {
    "name": "Vampiric",
    "weight": 0.025
}, {
    "name": "Dastardly",
    "weight": 0.05
}, {
    "name": "Brutal",
    "weight": 0.05
}, {
    "name": "Barbaric",
    "weight": 0.05
}, {
    "name": "Wretched",
    "weight": 0.05
}, {
    "name": "Sinister",
    "weight": 0.05
}, {
    "name": "Stoneforged",
    "weight": 0.05
}, {
    "name": "Skyforged",
    "weight": 0.025
}]

weapon_prefixes = [
    prefix["name"] for prefix in weapon_prefix_names_and_weights
]
weapon_prefix_weights = [
    prefix["weight"] for prefix in weapon_prefix_names_and_weights
]

weapon_suffix_names_and_weights = [{
    "name": "of Alacrity",
    "weight": 0.05
}, {
    "name": "of Celerity",
    "weight": 0.025
}, {
    "name": "of Defense",
    "weight": 0.1
}, {
    "name": "of Protection",
    "weight": 0.1
}, {
    "name": "of Strength",
    "weight": 0.05
}, {
    "name": "of the Juggernaut",
    "weight": 0.025
}, {
    "name": "of the Hawk",
    "weight": 0.05
}, {
    "name": "of the Eagle",
    "weight": 0.025
}, {
    "name": "of the Cat",
    "weight": 0.05
}, {
    "name": "of the Fox",
    "weight": 0.025
}, {
    "name": "of Endurance",
    "weight": 0.05
}, {
    "name": "of Toughness",
    "weight": 0.025
}, {
    "name": "of the Magi",
    "weight": 0.05
}, {
    "name": "of the Wizard",
    "weight": 0.025
}, {
    "name": "of Wisdom",
    "weight": 0.05
}, {
    "name": "of Piety",
    "weight": 0.025
}, {
    "name": "of Charisma",
    "weight": 0.05
}, {
    "name": "of the Silver Tongue",
    "weight": 0.025
}, {
    "name": "of Fate",
    "weight": 0.05
}, {
    "name": "of Fortune",
    "weight": 0.025
}, {
    "name": "of Longevity",
    "weight": 0.05
}, {
    "name": "of Health",
    "weight": 0.025
}, {
    "name": "of Life",
    "weight": 0.01
}, {
    "name": "of Scorching",
    "weight": 0.05
}, {
    "name": "of Flames",
    "weight": 0.025
}, {
    "name": "of Conflagaration",
    "weight": 0.01
}, {
    "name": "of the Flamecaller",
    "weight": 0.005
}, {
    "name": "of Frostbite",
    "weight": 0.05
}, {
    "name": "of the Glacier",
    "weight": 0.025
}, {
    "name": "of Shocking",
    "weight": 0.05
}, {
    "name": "of Thunder",
    "weight": 0.025
}, {
    "name": "of Purification",
    "weight": 0.05
}, {
    "name": "of the Heavens",
    "weight": 0.025
}, {
    "name": "of Celestial Wrath",
    "weight": 0.001
}, {
    "name": "of the Void",
    "weight": 0.05
}, {
    "name": "of the Arcane",
    "weight": 0.05
}, {
    "name": "of Wildfire",
    "weight": 0.01
}, {
    "name": "of Evasion",
    "weight": 0.05
}, {
    "name": "of Ruin",
    "weight": 0.05
}, {
    "name": "of Poison",
    "weight": 0.05
}, {
    "name": "of Decay",
    "weight": 0.01
}, {
    "name": "of Death",
    "weight": 0.01
}, {
    "name": "of Insanity",
    "weight": 0.05
}, {
    "name": "of the Slayer",
    "weight": 0.01
}, {
    "name": "of the Excecutioner",
    "weight": 0.005
}, {
    "name": "of Fervor",
    "weight": 0.05
}, {
    "name": "of Voracity",
    "weight": 0.05
}, {
    "name": "of Cruelty",
    "weight": 0.05
}, {
    "name": "of Ruthlessness",
    "weight": 0.05
}, {
    "name": "of Fury",
    "weight": 0.05
}, {
    "name": "of Slaughter",
    "weight": 0.05
}, {
    "name": "of Ferocity",
    "weight": 0.05
}, {
    "name": "of Onslaught",
    "weight": 0.02
}, {
    "name": "of Destruction",
    "weight": 0.05
}, {
    "name": "of Devastation",
    "weight": 0.005
}, {
    "name": "of Decimation",
    "weight": 0.025
}, {
    "name": "of Annihilation",
    "weight": 0.01
}, {
    "name": "of Disintegration",
    "weight": 0.008
}, {
    "name": "of Obliteration",
    "weight": 0.006
}, {
    "name": "of the Elements",
    "weight": 0.025
}, {
    "name": "of Piercing",
    "weight": 0.05
}, {
    "name": "of Shattering",
    "weight": 0.025
}, {
    "name": "of Torment",
    "weight": 0.05
}, {
    "name": "of Mortality",
    "weight": 0.05
},
{"name": "of Regeneration", "weight": 0.01}]

weapon_suffixes = [
    suffix["name"] for suffix in weapon_suffix_names_and_weights
]
weapon_suffix_weights = [
    suffix["weight"] for suffix in weapon_suffix_names_and_weights
]

weapon_metal_material_names = [
    "copper",
    "bronze",
    "iron",
    "steel",
    "truesteel",
    "darksteel",
    "orichalcum",
    "mithril",
    "voidstone",
    "brimstone",
    "cold iron",
    "thunderstone",
    "pearlstone",
    "electrum",
    "adamantine",
    "meteoric iron",
]

weapon_metal_material_weights = [
    0.2,
    0.2,
    0.23,
    0.15,
    0.0275,
    0.04,
    0.04,
    0.04,
    0.01,
    0.01,
    0.01,
    0.01,
    0.01,
    0.01,
    0.005,
    0.0075,
]

weapon_wood_material_names = [
    "maple",
    "ash",
    "elm",
    "oak",
    "hickory",
    "walnut",
    "ironwood",
    "rosewood",
    "juniper",
    "yew",
]

weapon_wood_material_weights = [
    0.2,
    0.18,
    0.16,
    0.14,
    0.12,
    0.075,
    0.05,
    0.025,
    0.025,
    0.025,
]
