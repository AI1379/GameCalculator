import GenshinImpact
import GenshinImpact.enemy
import GenshinImpact.weapon
import GenshinImpact.character
import GenshinImpact.element

character = GenshinImpact.character.Xiangling
weapon = GenshinImpact.weapon.EngulfingLighting

print(character.stats)
print(weapon.stats)
character.equip_weapon(weapon)
print(character.stats)

additional_attributes = {
    "crit_rate": 0.548,
    "crit_dmg": 1.029,
    "energy_recharge": 2.926,
    "attack_percentage": 0.146,
    "fixed_attack": 329,
    "elemental_mastery": 157,
    "dmg_bonus": 2.926*0.25,
    "reaction_coefficient": 0.5,
    "reaction_rate": 1
}
character.append_attributes(additional_attributes)
character.stats["elemental_bonus"][GenshinImpact.element.ElementType.PYRO.value] = 0.466
print(character.stats)
print(character.run_hooks().current_attack(), character.elemental_mastery_coefficient())

enemy = GenshinImpact.enemy.HydroTulpa
print(enemy.stats)
res = character.attack(enemy)
print(res)
