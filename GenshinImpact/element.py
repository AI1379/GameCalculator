from enum import Enum


class ElementType(Enum):
    PHYICAL = 0
    PYRO = 1
    HYDRO = 2
    DENDRO = 3
    ANEMO = 4
    CRYO = 5
    GEO = 6
    ELECTRO = 7


class Element:
    def __init__(self, type: ElementType, amount) -> None:
        self.type = type
        self.amount = amount

    def __str__(self) -> str:
        return f'{self.type.name}: {self.amount}'
    
    def reaction():
        pass
