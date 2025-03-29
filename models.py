from random import random, randint


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
    # def buy_animal(self, animal):
    #     if self.money >= animal.price:
    #         self.animals.append(animal)
    #         self.money -= animal.price
    #         print(f"{self.name} купил {animal.name}")
    #     else:
    #         print("Недостаточно денег!")
    #
    # def buy_plant(self, plant):
    #     if self.money >= plant.price:
    #         self.plants.append(plant)
    #         self.money -= plant.price
    #         print(f"{self.name} посадил {plant.name}")
    #     else:
    #         print("Недостаточно денег!")
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
        """Собирает продукцию, но не начисляет деньги (только добавляет в инвентарь)"""
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
        if self.eggs == 0 and self.milk == 0:
            return ["Нет продукции для продажи"]

        egg_price = 10
        milk_price = 50

        total = (self.eggs * egg_price) + (self.milk * milk_price)
        sold_info = [
            f"Продано: {self.eggs} яиц и {self.milk} молока",
            f"Выручка: {total} денег"
        ]

        self.money += total
        self.eggs = 0
        self.milk = 0

        return sold_info


    def check_production(self):
        """Проверяет производство всех животных"""
        messages = []
        for animal in self.animals:
            if animal.product_count > 0:
                messages.append(
                    f"{animal.name} произвела {animal.product_count} {animal.product}!"
                )
        return messages

    def plant_seed(self):
        if self.seeds:
            seed = self.seeds.pop()
            seed.x, seed.y = self.x, self.y
            self.plants.append(seed)
            print(f"{self.name} посадил {seed.name}!")
        else:
            print("Нет семян для посадки!")





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

    def grow(self):
        self.age += 1

    def is_ripe(self):
        return self.age >= self.growth_time

    def sell(self):
        if self.is_ripe():
            print(f"{self.name} продан за {self.sell_price}!")
            return self.sell_price
        return 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


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
            self.production_amount = randint(1, 3)  # Количество яиц за кладку
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
        self.setup_production()  # Обновляем цикл для следующего производства
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