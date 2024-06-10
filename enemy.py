class Enemy:
    def __init__(self, name, hp, damage, experience_reward):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.experience_reward = experience_reward

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            return True  # Enemy is dead
        return False

    def attack(self):
        return self.damage

    def get_stats(self):
        return f"{self.name} | HP: {self.hp}"
