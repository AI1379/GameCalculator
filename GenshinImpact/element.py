from enum import Enum
from .timeline import *


class ElementType(Enum):
    PHYICAL = 0
    PYRO = 1
    HYDRO = 2
    DENDRO = 3
    ANEMO = 4
    CRYO = 5
    GEO = 6
    ELECTRO = 7
    # Internal Elements
    FROZEN = 8
    CATALYST = 9


EMPTY_ELEMENTS = {
    ElementType.PHYICAL: 0,
    ElementType.PYRO: 0,
    ElementType.HYDRO: 0,
    ElementType.DENDRO: 0,
    ElementType.ANEMO: 0,
    ElementType.CRYO: 0,
    ElementType.GEO: 0,
    ElementType.ELECTRO: 0
}


class ElementTimer:
    def __init__(self, timeline: Timeline) -> None:
        self.timeline = timeline
        self.count = 0

    def hit(self, time: int) -> bool:
        self.count += 1
        # 2.5s/3hits with 7 element hits per cycle
        if (self.count % 3 == 1 and self.count <= 21) or self.timeline.current_time - time >= 25:
            return True
        return False


class Element:
    def __init__(self, type: ElementType, amount) -> None:
        self.type = type
        self.amount = amount

    def __str__(self) -> str:
        return f'{self.type.name}: {self.amount}'

    def reaction():
        pass
