from .pets import Pet


class Hamster(Pet):
    def __init__(self, name, type_name, birth_date, cage_size, commands):
        super().__init__(name, type_name, birth_date, commands)
        self.cage_size = cage_size
