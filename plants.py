class Plant:
    def __init__(self, name, growth_time, price, sell_price, images_dict, x, y):
        self.name = name
        self.growth_time = growth_time
        self.age = 0
        self.price = price
        self.sell_price = sell_price
        self.images_dict = images_dict
        self.x = x
        self.y = y
        self.watered = False
        self.stage = 0
        self.harvest_amount = 1

    def grow(self):
        if self.watered:
            self.age += 1
            self.watered = False
            max_stage = len(self.images_dict) - 1
            self.stage = min(self.age, max_stage)
            return True
        return False

    def water(self):
        self.watered = True
        return f"{self.name} полит(а)!"

    def is_ripe(self):
        return self.stage == len(self.images_dict) - 1

    def harvest(self):
        if self.is_ripe():
            self.age = 0
            self.stage = 0
            return self.harvest_amount
        return 0

    def draw(self, screen):
        screen.blit(self.images_dict[self.stage], (self.x, self.y))

    def is_near(self, farmer, max_dist=60):
        return ((abs(self.x - farmer.x) < max_dist) and
                (abs(self.y - farmer.y) < max_dist))