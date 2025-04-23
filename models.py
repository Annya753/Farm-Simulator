from random import random, randint
import pygame

class Farmer:
    def __init__(self, name, x, y):
        self.name = name
        self.money = 100000
        self.animals = []
        self.plants = []
        self.x = x
        self.y = y
        self.speed = 5
        self.eggs = 0
        self.milk = 0
        self.harvest = {}

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def add_item(self, item, game_map):
        if isinstance(item, Animal):
            (x, y), pen_boundaries = game_map.get_spawn_point(item.name)
            item.x, item.y = x, y
            item.set_pen_boundaries(pen_boundaries)
            self.animals.append(item)
        elif isinstance(item, Plant):
            self.plants.append(item)

    def feed_animal(self, animal):
        if animal.is_near(self):
            if animal.feed():
                return f"{animal.name} накормлена"
            else:
                return f"{animal.name} не голодна"
        else:
            return "Подойдите ближе к животному"

    def collect_products(self):
        for animal in self.animals:
            if animal.is_near(self) and animal.product_count > 0:
                amount = animal.product_count
                product = animal.product
                animal.product_count = 0
                if product == "яйца":
                    self.eggs += amount
                elif product == "молоко":
                    self.milk += amount
                return [f"Собрано {amount} {product} от {animal.name}"]

        return ["Нет готовой продукции рядом"]
    def check_animals_status(self):
        messages = []

        nearest_animal = None
        for animal in self.animals:
            if animal.is_near(self):
                nearest_animal = animal
                break

        if nearest_animal:
            status = f"{nearest_animal.name}: "
            if nearest_animal.hungry:
                status += "Голодна (C/V)"
            elif nearest_animal.product_count > 0:
                status += f"Готова продукция ({nearest_animal.product_count} {nearest_animal.product}) (F)"
            else:
                status += "Сыто, продукция в процессе"
            messages.append(status)
        elif self.animals:
            messages.append("Подойдите ближе к животному")
        else:
            messages.append("Нет животных на ферме")

        inventory = []
        if self.eggs:
            inventory.append(f"яиц: {self.eggs}")
        if self.milk:
            inventory.append(f"молока: {self.milk}")
        if inventory:
            messages.append("Склад: " + ", ".join(inventory))

        return messages

    def sell_products(self):
        total = 0

        if self.eggs > 0:
            total += self.eggs * 10
            self.eggs = 0

        if self.milk > 0:
            total += self.milk * 50
            self.milk = 0

        if self.harvest:
            for amount in self.harvest.values():
                total += amount * 100
            self.harvest = {}

        if total > 0:
            self.money += total
            return total
        return 0

    def water_plant(self, plant_index):
        if 0 <= plant_index < len(self.plants):
            return self.plants[plant_index].water()
        return "Нет растения с таким индексом"

    def harvest_plant(self, plant_index):
        if 0 <= plant_index < len(self.plants):
            plant = self.plants[plant_index]
            if plant.is_ripe():
                crop = plant.harvest()
                self.harvest[plant.name] = self.harvest.get(plant.name, 0) + crop
                return f"Собрано {crop} {plant.name} (Всего: {self.harvest[plant.name]})"
            return f"{plant.name} еще не созрела"
        return "Нет растения с таким индексом"

    def check_plants_status(self):
        messages = []

        nearest_plant = None
        for plant in self.plants:
            if plant.is_near(self):
                nearest_plant = plant
                break

        if nearest_plant:
            if nearest_plant.is_ripe():
                messages.append(f"{nearest_plant.name}: Готова к сбору (H)")
            elif not nearest_plant.watered:
                messages.append(f"{nearest_plant.name}: Нужен полив (W)")
            else:
                messages.append(f"{nearest_plant.name}: Растет (стадия {nearest_plant.stage + 1})")
        elif self.plants:
            messages.append("Подойдите ближе к растению")
        else:
            messages.append("Нет растений на поле")

        if self.harvest:
            harvest_info = "Урожай: " + ", ".join(
                f"{name}: {amount}" for name, amount in self.harvest.items()
            )
            messages.append(harvest_info)

        return messages


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