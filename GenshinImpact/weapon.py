from enum import Enum

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


class BaseWeapon:
    pass
