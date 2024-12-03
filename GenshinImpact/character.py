from enemy import Enemy
from weapon import WeaponType, BaseWeapon

"""
States of damage:

type: str // type of the damage
atk: int // attack of the character
crit_rate: float // critical rate of the character
crit_dmg: float // critical damage of the character
elemental_bonus: float // elemental bonus of the character
dmg_bonus: float // damage bonus of the character excluding elemental bonus
enemy_defense: int // defense of the enemy
enemy_resistance: float // resistance of the enemy
character_level: int // level of the character
enemy_level: int // level of the enemy
reaction_magnitude: float // magnitude of the element reaction
character_magnitude: float // magnitude of the character

"""


class Damage:
    def __init__(self, **kwargs):
        self.stats = kwargs

    def calculate_damage(self) -> int:
        result = self.stats['atk'] * self.stats['character_magnitude']
        result *= (1+self.stats['crit_dmg'])*self.stats['crit_rate']
        result *= (1+self.stats['elemental_bonus']+self.stats['dmg_bonus'])
        result *= (1+self.stats['reaction_magnitude'])

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
    def __init__(self,  **kwargs):
        self.name = kwargs['name']
        self.element = kwargs['element']
        self.weapon_type = kwargs['weapon_type']
        self.stats = kwargs

    # Equip a weapon to the character
    def equip_weapon(self, weapon: BaseWeapon):
        self.weapon = weapon
        self.stats['base_attack'] += weapon.stats['base_attack']
        self.stats[weapon.stats['main_attribute']
                   ] += weapon.stats['main_attribute_value']

    # Return the damage dealt to the enemy
    def attack(self, enemy: Enemy) -> int:

        return self.stats['attack'] - enemy.stats['defense']
