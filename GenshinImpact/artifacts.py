from enum import Enum
from .element import ElementType


class ArtifactType(Enum):
    FLOWER = 0
    PLUME = 1
    SANDS = 2
    GOBLET = 3
    CIRCLET = 4


def Singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


class ArtifactSet:
    def __init__(self):
        self.name = ""
        self.bonus2attributes = {}
        self.bonus4attributes = {}
        pass

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return f"{self.name}"

    def bonus2(self, stats):
        pass

    def bonus4(self, stats):
        pass


class Artifact:
    def __init__(self, stats):
        self.name = stats["name"]
        self.set = stats["set"]
        self.type = stats["type"]
        self.stats = stats

    def calculate_bonus(self):
        pass


def empty_artifact(type: ArtifactType):
    return Artifact({
        "name": "Empty",
        "set": ArtifactSet(),
        "type": type
    })


@Singleton
class EmblemOfSeveredFate(ArtifactSet):
    def __init__(self):
        super().__init__()
        self.name = "Emblem of Severed Fate"
        self.bonus2attributes = {
            "energy_recharge": 0.2
        }

    def bonus2(self, character):
        pass

    def bonus4(self, character):
        stats = character.stats
        stats["dmg_bonus"] += min(0.75, stats["energy_recharge"] * 0.25)


flower = Artifact({
    "name": "Flower of Life",
    "set": EmblemOfSeveredFate(),
    "type": ArtifactType.FLOWER,
    "attributes": [
        {"attribute": "fixed_hp", "value": 4780},
        {"attribute": "crit_dmg", "value": 0.202},
        {"attribute": "crit_rate", "value": 0.062},
        {"attribute": "hp_percentage", "value": 0.041},
        {"attribute": "attack_percentage", "value": 0.099}
    ]
})

plume = Artifact({
    "name": "Plume of Death",
    "set": EmblemOfSeveredFate(),
    "type": ArtifactType.PLUME,
    "attributes": [
        {"attribute": "fixed_attack", "value": 311},
        {"attribute": "crit_dmg", "value": 0.124},
        {"attribute": "elemental_mastery", "value": 38},
        {"attribute": "hp_percentage", "value": 0.099},
        {"attribute": "energy_recharge", "value": 0.130}
    ]
})

sands = Artifact({
    "name": "Sands of Eon",
    "set": EmblemOfSeveredFate(),
    "type": ArtifactType.SANDS,
    "attributes": [
        {"attribute": "energy_recharge", "value": 0.518},
        {"attribute": "crit_dmg", "value": 0.140},
        {"attribute": "fixed_hp", "value": 478},
        {"attribute": "fixed_defense", "value": 58},
        {"attribute": "attack_percentage", "value": 0.047}
    ]
})

goblet = Artifact({
    "name": "Goblet of Eonothem",
    "set": EmblemOfSeveredFate(),
    "type": ArtifactType.GOBLET,
    "attributes": [
        {"attribute": "pyro_bonus", "value": 0.466},
        {"attribute": "crit_rate", "value": 0.125},
        {"attribute": "crit_dmg", "value": 0.063},
        {"attribute": "hp_percentage", "value": 0.087},
        {"attribute": "fixed_hp", "value": 418}
    ]
})

circlet = Artifact({
    "name": "Circlet of Logos",
    "set": EmblemOfSeveredFate(),
    "type": ArtifactType.CIRCLET,
    "attributes": [
        {"attribute": "crit_rate", "value": 0.311},
        {"attribute": "elemental_mastery", "value": 23},
        {"attribute": "energy_recharge", "value": 0.227},
        {"attribute": "hp_percentage", "value": 0.140},
        {"attribute": "fixed_attack", "value": 18}
    ]
})
