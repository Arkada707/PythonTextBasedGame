class Tile:
    def __init__(self, type='empty', enemy=None):
        self.type = type
        self.enemy = enemy

    def is_empty(self):
        return self.type == 'empty' and self.enemy is None

    def is_exit(self):
        return self.type == 'exit'

    def is_ladder_up(self):
        return self.type == 'ladder_up'

    def is_ladder_down(self):
        return self.type == 'ladder_down'

    def is_dungeon_entrance(self):
        return self.type == 'dungeon_entrance'

    def is_enemy(self):
        return self.enemy is not None

    def set_enemy(self, enemy):
        self.enemy = enemy

    def remove_enemy(self):
        self.enemy = None
