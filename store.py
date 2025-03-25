from models import Animal, Plant


class Store:
    def __init__(self, images):
        self.items = [
            Plant("Пшеница", 3, 50, 100),
            # Plant("Капуста", 5, 80, 160),
            Animal("Корова", 500, "молоко", 50),
            Animal("Курица", 100, "яйца", 10)
        ]

    # def buy_animal(self, farmer, animal_name):
    #     for animal in self.animals:
    #         if animal.name == animal_name:
    #             farmer.buy_animal(animal)
    #             return
    #     print("Животное не найдено!")
    #
    # def buy_plant(self, farmer, plant_name):
    #     for plant in self.plants:
    #         if plant.name == plant_name:
    #             farmer.buy_plant(plant)
    #             return
    #     print("Растение не найдено!")

    def buy_item(self, farmer, item):
        if farmer.money >= item.price:
            for i in self.items:
                if i.name == item.name:
                    farmer.money -= item.price
                    farmer.add_item(item)
                    print(f"{farmer.name} купил {item.name}")
                    return
        print("Элемент не найден!")

