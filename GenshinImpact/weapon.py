from typing import Dict, List, Callable
from enum import Enum
from .timeline import *

"""
States of the weapon:

base_attack: int
main_attribute: str
main_attribute_value: int
secondary_attribute: function // it is not quite sure how to implement this

"""


class WeaponType(Enum):
    SWORD = 1
    CLAYMORE = 2
    POLEARM = 3
    BOW = 4
    CATALYST = 5


class Weapon(Listener):
    def __init__(self, stats):
        self.name = stats["name"]
        self.stats = stats

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"{self.name}"


def EngulfingLightingCallback(character):
    stats = character.stats
    stats["energy_recharge"] += 0.3
    stats["attack_percentage"] += min(
        0.8, (stats["energy_recharge"] - 1) * 0.28)
    print(f"Add: {min(0.8, (stats["energy_recharge"] - 1) * 0.28)} with {stats['energy_recharge']}")


EngulfingLighting = Weapon({
    "name": "Engulfing Lighting",
    "base_attack": 608.0745972,
    "main_attribute": "energy_recharge",
    "main_attribute_value": 0.55128,
    "secondary_attribute": EngulfingLightingCallback
})
