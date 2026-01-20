from systems.data.storage import DataStorage


class AliveDataStorage(DataStorage):
    def __init__(self, max_life: int, life: int = None):
        self.max_life = max_life
        self.life = life if life is not None else max_life
        self.dead = False
        self.time_before_delete = 2.0
