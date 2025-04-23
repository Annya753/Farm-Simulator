from random import random, randint
import pygame

class Animal:
    def __init__(self, name, price, product, product_price, image, x, y):
        self.name = name
        self.price = price
        self.hungry = True
        self.product = product
        self.product_price = product_price
        self.image = image
        self.x = x
        self.y = y
        self.production_timer = 0
        self.product_count = 0
        self.setup_production()
        self.direction = [random() * 2 - 1, random() * 2 - 1]  # Случайное направление
        self.move_timer = 0
        self.move_cooldown = randint(30, 100)
        self.speed = 0.5 if name.lower() == "корова" else 1.0
        self.pen_boundaries = None

    def set_pen_boundaries(self, walls):
        self.pen_boundaries = walls

    def setup_production(self):
        if self.name.lower() == "курица":
            self.production_cycle = randint(1, 3)
            self.production_amount = randint(1, 3)
        elif self.name.lower() == "корова":
            self.production_cycle = randint(2, 4)
            self.production_amount = randint(1, 3)

    def update(self, walls):
        self.move_timer += 1
        if self.move_timer >= self.move_cooldown:
            self.direction = [random() * 2 - 1, random() * 2 - 1]
            self.move_timer = 0
            self.move_cooldown = randint(30, 100)

        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed

        animal_rect = pygame.Rect(new_x, new_y, self.image.get_width(), self.image.get_height())
        can_move = True

        for wall in walls:
            if animal_rect.colliderect(wall.rect):
                can_move = False
                self.direction = [random() * 2 - 1, random() * 2 - 1]
                break

        if can_move:
            self.x = new_x
            self.y = new_y


    def produce(self):
        self.product_count += self.production_amount
        self.production_timer = 0
        self.setup_production()
        self.hungry = True
        print(f"{self.name} произвела {self.product_count} {self.product}!")

    def feed(self):
        if self.hungry:
            self.hungry = False
            print(f"{self.name} накормлены!")
            return True
        print(f"{self.name} уже не голодены!")
        return False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_near(self, farmer, radius=50):
        return abs(self.x - farmer.x) < radius and abs(self.y - farmer.y) < radius

    def next_day(self):
        if not self.hungry:
            self.production_timer += 1
            if self.production_timer >= self.production_cycle:
                self.produce()