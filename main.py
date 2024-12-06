import GenshinImpact.enemy as enemy
import GenshinImpact.weapon as weapon
import GenshinImpact.character as character
import GenshinImpact.element as element
import GenshinImpact.artifacts as artifacts
import matplotlib.pyplot as plt

char = character.Xiangling
wp = weapon.EngulfingLighting

# print(character.stats)
# print(weapon.stats)
char.equip_weapon(wp)

char.equip_artifact(artifacts.flower)
char.equip_artifact(artifacts.plume)
char.equip_artifact(artifacts.sands)
char.equip_artifact(artifacts.goblet)
char.equip_artifact(artifacts.circlet)
char.set(reaction_coefficient=0.5, reaction_rate=1)

additional_attributes = {
    "crit_rate": 0.548,
    "crit_dmg": 1.029,
    "energy_recharge": 2.926,
    "attack_percentage": 0.146,
    "fixed_attack": 329,
    "elemental_mastery": 157,
    "dmg_bonus": 2.926*0.25,
    "reaction_coefficient": 0.5,
    "reaction_rate": 1,
    "pyro_bonus": 0.466,
}

# stats = char.current_stats()

# for key, value in additional_attributes.items():
#     if key in stats:
#         if stats[key] != additional_attributes[key] and key != "elemental_bonus":
#             print(key, stats[key], additional_attributes[key])

# char.set_attributes(additional_attributes)
print(char.current_stats())

enem = enemy.HydroTulpa
# print(enemy.stats)
res = char.attack(enem)
print(res)


# def dmg(atkpcg):
#     character.stats["attack_percentage"] = atkpcg
#     return character.attack(enemy)


# fig, ax = plt.subplots()       # a figure with a single Axes
# em_lst = [i / 100 for i in range(1, 100)]
# dmg_lst = [dmg(em) for em in em_lst]

# ax.plot(em_lst, dmg_lst)

# plt.show()
