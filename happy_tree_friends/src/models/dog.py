from .pets import Pet

class Dog(Pet):
    def __init__(self, name, type_name, birth_date, breed, commands):
        super().__init__(name, type_name, birth_date, commands)
        self.breed = breed