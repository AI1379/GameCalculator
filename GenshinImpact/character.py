from typing import List, Dict
import copy
from .element import ElementType, EMPTY_ELEMENTS
from .enemy import Enemy
from .weapon import WeaponType, Weapon
from .artifacts import Artifact, ArtifactSet
from .timeline import *


def merge_stats(stats1: dict, stats2: dict) -> dict:
    res = copy.deepcopy(stats1)
    for key in stats2.keys():
        if key in stats1.keys():
            if (isinstance(stats2[key], dict)):
                res[key] = merge_stats(stats1[key], stats2[key])
            elif (isinstance(stats2[key], list)):
                res[key] = [stats1[key][i] + stats2[key][i]
                            for i in range(len(stats1[key]))]
            else:
                res[key] += stats2[key]
        else:
            res[key] = stats2[key]
    return res


def set_stats(stats1: dict, stats2: dict) -> dict:
    res = copy.deepcopy(stats1)
    for key in stats2.keys():
        if key in stats1.keys():
            if (isinstance(stats2[key], dict)):
                res[key] = set_stats(stats1[key], stats2[key])
            elif (isinstance(stats2[key], list)):
                res[key] = copy.deepcopy(stats2[key])
            else:
                res[key] = stats2[key]
        else:
            res[key] = stats2[key]
    return res


"""
States of damage:

type: str // type of the damage
attack: int // attack of the character
crit_rate: float // critical rate of the character
crit_dmg: float // critical damage of the character
elemental_bonus: float // elemental bonus of the character
dmg_bonus: float // damage bonus of the character excluding elemental bonus
defense_reduction: float // defense reduction of the enemy
defense_ignore: float // defense ignore of the character
enemy_resistance: dict(float) // resistance of the enemy
character_level: int // level of the character
enemy_level: int // level of the enemy
reaction_coefficient: float // coefficient of the element reaction
elemental_mastery_coefficient: float // coefficient of the elemental mastery
skill_coefficient: float // coefficient of the character

"""


class Damage:
    def __init__(self, stats):
        self.stats = stats

    def calculate_damage(self) -> int:
        print(self.stats)
        # Base damage
        result = self.stats["attack"] * \
            self.stats["skill_coefficient"] + self.stats["extra_damage"]
        # Expected CRIT damage
        result *= (1+self.stats["crit_dmg"]*self.stats["crit_rate"])
        # Damage bonus
        result *= (1+self.stats["elemental_bonus"]+self.stats["dmg_bonus"])
        # Enhance element reaction: Melt, Vaporize
        result *= (1 + self.stats["extra_reaction_coefficient"] +
                   self.stats["elemental_mastery_coefficient"]) * \
            (1 + self.stats["reaction_coefficient"]) * \
            self.stats["reaction_rate"] + 1 - self.stats["reaction_rate"]
        # Resistance
        type = self.stats["type"]
        enemy_resistance = self.stats["enemy_resistance"][type]
        if enemy_resistance < 0:
            res_coefficient = 1 - enemy_resistance/2
        elif 0 <= enemy_resistance <= 0.75:
            res_coefficient = 1 - enemy_resistance
        elif 0.75 < enemy_resistance <= 10:
            res_coefficient = 1/(1+4*enemy_resistance)
        else:
            res_coefficient = 0  # Immune
        result *= res_coefficient
        # Defence
        defence_coefficient = (100 + self.stats["character_level"]) / (
            (self.stats["character_level"] + 100) +
            (self.stats["enemy_level"] + 100) * (1 - self.stats["defense_ignore"]) * (1 - self.stats["defense_reduction"]))
        result *= defence_coefficient

        return result


def enhance_reaction_coefficient(em):
    return em * 2.785 / (em + 1404.5)

# TODO: Level base coefficient


def catalyst_coefficient(em):
    return em * 5 / (em + 1200)


"""
States of the character:

base_attack: int
base_defense: int
base_hp: int
base_crit_rate: float
base_crit_dmg: float
base_energy_recharge: float
base_elemental_mastery: int
dmg_bonus: list // dmg_bonus[ELEMENT] = float. ELEMENT == 0 means physical damage

"""


class Character(Listener):
    BASE_STATS = {
        "crit_rate": 0.05,
        "crit_dmg": 0.5,
        "energy_recharge": 0,
        "elemental_mastery": 0,
        "attack_percentage": 0,
        "fixed_attack": 0,
        "elemental_bonus": EMPTY_ELEMENTS,
        "dmg_bonus": 0,
        "reaction_rate": 0
    }

    def __init__(self, stats, timeline: Timeline = None):
        if timeline is not None:
            super().__init__(timeline)
        self.name = stats["name"]
        self.element = stats["element"]
        self.weapon_type = stats["weapon_type"]
        self.stats = merge_stats(self.BASE_STATS, stats)
        self.hooks = []

    def __str__(self) -> str:
        return f"{self.name}"

    def attach(self, timeline: Timeline):
        super().attach(timeline)

    def append_attributes(self, attributes: dict):
        self.stats = merge_stats(self.stats, attributes)
        
    def set_attributes(self, attributes: dict):
        self.stats = set_stats(self.stats, attributes)

    # Return current attack of the character

    def current_attack(self):
        return self.stats["base_attack"] * (1 + self.stats["attack_percentage"]) + self.stats["fixed_attack"]

    # Equip a weapon to the character
    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        self.stats["base_attack"] += weapon.stats["base_attack"]
        self.stats[weapon.stats["main_attribute"]
                   ] += weapon.stats["main_attribute_value"]
        self.hooks.append(weapon.stats["secondary_attribute"])

    def equip_artifact(self, artifact: Artifact):
        for attr in artifact.stats["attributes"]:
            self.stats[attr["attribute"]] += attr["value"]

    def set_artifact_set(self, artifact_set: ArtifactSet, num):
        for attr in artifact_set.stats["attributes"]:
            self.stats[attr["attributes"]] += attr["value"]
        if num >= 2:
            self.hooks.append(artifact_set.stats["set_arrtibute_2"])
        if num >= 4:
            self.hooks.append(artifact_set.stats["set_attribute_4"])

    def current_stats(self):
        cp = copy.deepcopy(self.stats)
        for hook in self.hooks:
            hook(cp)
        # Cap crit_rate
        if cp["crit_rate"] > 1:
            cp["crit_rate"] = 1
        return cp

    # Return the damage dealt to the enemy
    def attack(self, enemy: Enemy, **kwargs) -> int:
        stats = self.current_stats()
        elem = self.element
        if "element" in kwargs.keys():
            elem = kwargs["element"]
        dmg = Damage({
            "type": elem,
            "attack": stats["base_attack"] * (1 + stats["attack_percentage"]) + stats["fixed_attack"],
            "crit_rate": stats["crit_rate"],
            "crit_dmg": stats["crit_dmg"],
            "extra_damage": 0,
            "elemental_bonus": stats["elemental_bonus"][elem],
            "dmg_bonus": stats["dmg_bonus"],
            "defense_reduction": enemy.stats["defense_reduction"],
            "defense_ignore": stats["defense_ignore"],
            "enemy_resistance": enemy.stats["resistance"],
            "character_level": stats["level"],
            "enemy_level": enemy.stats["level"],
            "extra_reaction_coefficient": 0,
            "reaction_coefficient": stats["reaction_coefficient"],
            "reaction_rate": stats["reaction_rate"],
            "elemental_mastery_coefficient": enhance_reaction_coefficient(stats["elemental_mastery"]),
            "skill_coefficient": stats["skill_coefficient"]
        })
        return dmg.calculate_damage()


Xiangling = Character({
    "name": "Xiangling",
    "element": ElementType.PYRO,
    "weapon_type": WeaponType.POLEARM,
    "level": 90,
    "base_hp": 10874.91499475576,
    "base_attack": 225.14102222725342,
    "base_defence": 668.8711049900703,
    "elemental_mastery": 96,
    "reaction_coefficient": 0.5,
    "skill_coefficient": 2.38,
    "defense_ignore": 0
})
