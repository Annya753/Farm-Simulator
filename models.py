from animals import Animal
from plants import Plant

class Farmer:
    def __init__(self, name, x, y):
        self.name = name
        self.money = 1000
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