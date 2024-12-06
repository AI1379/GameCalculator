from enum import Enum


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
        pass

    def __str__(self) -> str:
        return f"{self.name}"

    def bonus2(self):
        pass

    def bonus4(self):
        pass


class Artifact:
    def __init__(self, stats):
        self.name = stats["name"]
        self.set = stats["set"]
        self.type = stats["type"]
        self.stats = stats

    def calculate_bonus(self):
        pass
