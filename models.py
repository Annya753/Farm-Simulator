class Farmer:
    def __init__(self, name):
        self.name = name
        self.money = 1000
        self.animals = []
        self.plants = []

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

    def add_item(self, item):
        if type(item) is Animal:
            self.animals.append(item)
        if type(item) is Plant:
            self.plants.append(item)

    def collect_harvest(self):
        earnings = 0
        for plant in self.plants:
            if plant.is_ripe():
                earnings += plant.sell()
                self.money += earnings
        print(f"{self.name} заработал {earnings} на урожае!")

    def feed_animals(self):
        for animal in self.animals:
            animal.feed()





class Plant:
    def __init__(self, name, growth_time, price, sell_price):
        self.name = name
        self.growth_time = growth_time
        self.age = 0
        self.price = price
        self.sell_price = sell_price

    def grow(self):
        self.age += 1

    def is_ripe(self):
        return self.age >= self.growth_time

    def sell(self):
        if self.is_ripe():
            print(f"{self.name} продан за {self.sell_price}!")
            return self.sell_price
        return 0






class Animal:
    def __init__(self, name, price, product, product_price):
        self.name = name
        self.price = price
        self.hungry = False
        self.product = product
        self.product_price = product_price

    def feed(self):
        self.hungry = False
        print(f"{self.name} накормлена!")

    def collect_product(self):
        if not self.hungry:
            print(f"Собрано {self.product}, продано за {self.product_price}")
            return self.product_price
        print(f"{self.name} голодна и не дает продукцию")
        return 0
