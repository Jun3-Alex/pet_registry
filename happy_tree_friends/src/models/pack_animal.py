from .animal import Animal


class PackAnimal(Animal):
    def __init__(self, name, type_name, birth_date, load_capacity):
        super().__init__(name, type_name, birth_date)
        self.load_capacity = load_capacity
