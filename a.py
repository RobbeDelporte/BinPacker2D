class ReadOnlyClass:
    def __init__(self, attr1, attr2):
        self._attr1 = attr1
        self._attr2 = attr2

    @property
    def attr1(self):
        return self._attr1

    @property
    def attr2(self):
        return self._attr2
