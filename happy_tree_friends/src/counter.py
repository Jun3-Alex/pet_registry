class CounterError(Exception):
    """Кастомное исключение для класса Counter."""
    pass


class Counter:
    def __init__(self):
        self.value = 0
        self._is_in_context = False

    def __enter__(self):
        self._is_in_context = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._is_in_context = False

    def add(self):
        if not self._is_in_context:
            raise CounterError("Counter должен использоваться внутри контекстного менеджера 'with'")
        self.value += 1
