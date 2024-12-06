from .element import ElementType
from .timeline import *

class Enemy(Listener):
    def __init__(self,  stats):
        self.name = stats['name']
        self.stats = stats


HydroTulpa = Enemy({
    "name": "Hydro Tulpa: Flashflood",
    "level": 103,
    "resistance": {
        ElementType.PHYICAL: 0.1,
        ElementType.ANEMO: 0.1,
        ElementType.CRYO: 0.1,
        ElementType.DENDRO: 0.1,
        ElementType.ELECTRO: 0.1,
        ElementType.GEO: 0.1,
        ElementType.HYDRO: 100,
        ElementType.PYRO: 0.1
    }
})
