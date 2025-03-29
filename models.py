from random import random, randint

from pyexpat.errors import messages


class Farmer:
    def __init__(self, name, x, y):
        self.name = name
        self.money = 1000
        self.animals = []
        self.plants = []
        self.seeds = []
        self.x = x
        self.y = y
        self.speed = 5
        self.eggs = 0
        self.milk = 0
        self.wheat = 0


    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def add_item(self, item):
        if type(item) is Animal:
            self.animals.append(item)
        if type(item) is Plant:
            self.plants.append(item)

    def feed_all_chickens(self):
        fed_count = 0
        for animal in self.animals:
            if animal.name.lower() == "курица":
                if animal.feed():
                    fed_count += 1
        return f"Накормлено кур: {fed_count}"

    def feed_all_cows(self):
        fed_count = 0
        for animal in self.animals:
            if animal.name.lower() == "корова":
                if animal.feed():
                    fed_count += 1
        return f"Накормлено коров: {fed_count}"

    def collect_all_products(self):
        """Собирает продукцию"""
        messages = []
        collected_eggs = 0
        collected_milk = 0

        for animal in self.animals:
            if animal.product_count > 0:
                if animal.product == "яйца":
                    self.eggs += animal.product_count
                    collected_eggs += animal.product_count
                elif animal.product == "молоко":
                    self.milk += animal.product_count
                    collected_milk += animal.product_count

                messages.append(f"Собрано: {animal.product_count} {animal.product}")
                animal.product_count = 0

        if collected_eggs or collected_milk:
            messages.append(f"Яиц: + {collected_eggs}, молока: + {collected_milk}")
        else:
            messages.append("Нет продукции для сбора")

        return messages

    def sell_products(self):
        if self.eggs == 0 and self.milk == 0 and self.wheat == 0:
            return ["Нет продукции для продажи"]

        egg_price = 10
        milk_price = 50
        wheat_price = 100

        total = (self.eggs * egg_price) + (self.milk * milk_price) +  (self.wheat * wheat_price)
        sold_items = [f"Продано: {self.eggs} яиц, {self.milk} молока, {self.wheat} пшеницы",
        f"Выручка: {total} денег"]

        self.eggs = 0
        self.milk = 0
        self.wheat = 0
        self.money += total

        return sold_items


    def check_production(self):
        """Проверяет производство всех животных"""
        messages = []
        for animal in self.animals:
            if animal.product_count > 0:
                messages.append(f"{animal.name} произвела {animal.product_count} {animal.product}!")
        return messages

    def plant_seed(self):
        messages = []
        if self.seeds:
            seed = self.seeds.pop()
            seed.x, seed.y = self.x, self.y
            self.plants.append(seed)
            messages.append(f"{self.name} посадил {seed.name}!")
        else:
            messages.append("Нет семян для посадки!")
        return messages

    def water_plant(self, plant_index):
        if 0 <= plant_index < len(self.plants):
            message = self.plants[plant_index].water()
            return message
        return "Нет растения с таким индексом"

    def harvest_plant(self, plant_index):
        if 0 <= plant_index < len(self.plants):
            plant = self.plants[plant_index]
            if plant.is_ripe():
                self.wheat += 1  # Увеличиваем количество пшеницы
                self.plants.pop(plant_index)
                return f"Собрана 1 {plant.name} (Всего: {self.wheat})"
            return f"{plant.name} еще не созрела"
        return "Нет растения с таким индексом"

    def check_plants_status(self):
        messages = []
        for i, plant in enumerate(self.plants):
            status = f"{i}: {plant.name} - "
            if plant.is_ripe():
                status += "Готова к сбору (нажми H)"
           # else:
           #     status += f"Стадия {plant.stage}/{len(plant.stages_images) - 1}"
                if not plant.watered:
                    status += " (Нужен полив - нажми W)"
            messages.append(status)
        return messages if messages else ["Нет растений"]





class Plant:
    def __init__(self, name, growth_time, price, sell_price, image, x, y):
        self.name = name
        self.growth_time = growth_time
        self.age = 0
        self.price = price
        self.sell_price = sell_price
        self.image = image
        self.x = x
        self.y = y
        self.watered = False  # Полито ли растение сегодня
        self.stage = 0
    #   self.stages_images = []

    def grow(self):
        if self.watered:
            self.age += 1
            self.watered = False  # Сбрасываем статус полива
            # Обновляем стадию роста
          # self.stage = min(self.age, len(self.stages_images)-1)
            return True
        return False

    def water(self):
        self.watered = True
        return f"{self.name} полита!"

    def is_ripe(self):
        return self.age >= self.growth_time

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

   # def draw(self, screen):
   #     # Рисуем текущую стадию роста
   #     current_image = self.stages_images[self.stage]
   #     screen.blit(current_image, (self.x, self.y))

    def sell(self):
        if self.is_ripe():
            print(f"{self.name} продан за {self.sell_price}!")
            return self.sell_price
        return 0


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



    def setup_production(self):
        if self.name.lower() == "курица":
            self.production_cycle = randint(1, 3)  # Дни между кладками
            self.production_amount = randint(1, 3)
        elif self.name.lower() == "корова":
            self.production_cycle = randint(2, 4)  # Дни между удоями
            self.production_amount = randint(1, 3)

    def update(self):
        if not self.hungry:
            self.production_timer += 1
            if self.production_timer >= self.production_cycle:
                self.produce()

    def produce(self):
        self.product_count += self.production_amount
        self.production_timer = 0
        self.setup_production()
        self.hungry = True  # После производства животное становится голодным
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