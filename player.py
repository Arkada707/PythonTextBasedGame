class Player:
    def __init__(self, x, y):
        self.hp = 100
        self.mana = 50
        self.stamina = 100
        self.gold = 0
        self.level = 1
        self.experience = 0
        self.damage = 20
        self.x = x
        self.y = y

    def get_stats(self):
        return f"HP: {self.hp} | Mana: {self.mana} | Stamina: {self.stamina} | Gold: {self.gold} | Level: {self.level} | XP: {self.experience}"

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            return True  # Player is dead
        return False

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.hp += 20
        self.mana += 10
        self.stamina += 10
        self.damage += 5
        self.experience = 0

    def attack(self):
        return self.damage

    def move(self, dx, dy, grid_width, grid_height):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < grid_width and 0 <= new_y < grid_height:
            self.x = new_x
            self.y = new_y

    def add_gold(self, amount):
        self.gold += amount
