

class Character:
    def __init__(self,  **kwargs):
        self.name = kwargs['name']
        self.element = kwargs['element']
        self.weapon = kwargs['weapon']
        self.stats = kwargs
