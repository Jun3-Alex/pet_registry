from .animal import Animal


class Pet(Animal):
    def __init__(self, name, type_name, birth_date, commands):
        super().__init__(name, type_name, birth_date)
        self.commands = commands
