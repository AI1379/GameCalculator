from typing import List, Dict
import copy
from .element import ElementType
from .enemy import Enemy
from .weapon import WeaponType, Weapon
from .artifacts import Artifact, ArtifactSet

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
        # Base damage
        result = self.stats["attack"] * self.stats["skill_coefficient"]
        # Expected CRIT damage
        result *= (1+self.stats["crit_dmg"]*self.stats["crit_rate"])
        # Damage bonus
        result *= (1+self.stats["elemental_bonus"]+self.stats["dmg_bonus"])
        # Element reaction
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


class Character:
    def __init__(self,  stats):
        self.name = stats["name"]
        self.element = stats["element"]
        self.weapon_type = stats["weapon_type"]
        self.stats = stats
        self.stats["crit_rate"] = 0.05
        self.stats["crit_dmg"] = 0.5
        self.stats["energy_recharge"] = 0
        self.stats["elemental_mastery"] = 0
        self.stats["attack_percentage"] = 0
        self.stats["fixed_attack"] = 0
        self.stats["elemental_bonus"] = [0]*8
        self.stats["dmg_bonus"] = 0
        self.stats["reaction_rate"] = 0
        self.stats[stats["secondary_attribute"]
                   ] += stats["secondary_attribute_value"]
        self.hooks = []

    def __str__(self) -> str:
        return f"{self.name}"

    def append_attributes(self, attributes: dict):
        for key in attributes.keys():
            self.stats[key] = attributes[key]

    # Return the coefficient of the elemental mastery

    def elemental_mastery_coefficient(self):
        return self.stats["elemental_mastery"] * 2.785 / (self.stats["elemental_mastery"] + 1404.5)

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

    def run_hooks(self):
        cp = copy.deepcopy(self)
        for hook in cp.hooks:
            hook(cp)
        return cp

    # Return the damage dealt to the enemy
    def attack(self, enemy: Enemy) -> int:
        original_stats = copy.deepcopy(self.stats)
        for hook in self.hooks:
            hook(self)
        dmg = Damage({
            "type": self.element,
            "attack": self.current_attack(),
            "crit_rate": self.stats["crit_rate"],
            "crit_dmg": self.stats["crit_dmg"],
            "elemental_bonus": self.stats["elemental_bonus"][self.element.value],
            "dmg_bonus": self.stats["dmg_bonus"],
            "defense_reduction": self.stats["defense_reduction"],
            "defense_ignore": self.stats["defense_ignore"],
            "enemy_resistance": enemy.stats["resistance"],
            "character_level": self.stats["level"],
            "enemy_level": enemy.stats["level"],
            "extra_reaction_coefficient": 0,
            "reaction_coefficient": self.stats["reaction_coefficient"],
            "reaction_rate": self.stats["reaction_rate"],
            "elemental_mastery_coefficient": self.elemental_mastery_coefficient(),
            "skill_coefficient": self.stats["skill_coefficient"]
        })
        self.stats = original_stats
        return dmg.calculate_damage()


Xiangling = Character({
    "name": "Xiangling",
    "element": ElementType.PYRO,
    "weapon_type": WeaponType.POLEARM,
    "level": 90,
    "base_hp": 10874.91499475576,
    "base_attack": 225.14102222725342,
    "base_defence": 668.8711049900703,
    "secondary_attribute": "elemental_mastery",
    "secondary_attribute_value": 96,
    "reaction_coefficient": 0.5,
    "skill_coefficient": 2.38,
    "defense_reduction": 0,
    "defense_ignore": 0
})
