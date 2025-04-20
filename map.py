import pygame
from random import randint

BROWN = (84, 28, 28)

class InvisibleWall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

class Map:
    def __init__(self, screen, images, message_font, status_font):
        self.screen = screen
        self.images = images
        self.message_font = message_font
        self.status_font = status_font
        self.walls = []
        self.create_pens()


    def create_pens(self):
        self.chicken_pen = (625, 370, 218, 262)
        self.cow_pen = (843, 370, 215, 262)

        self.walls = [
            InvisibleWall(625, 370, 20, 262),
            InvisibleWall(843, 370, 20, 262),
            InvisibleWall(1058, 370, 20, 262),
            InvisibleWall(625, 632, 433, 20),
            InvisibleWall(625, 370, 433, 20)
        ]

    def get_spawn_point(self, animal_type):
        """Возвращает случайную точку спавна и границы загона для животного с отступом"""
        if animal_type.lower() == "курица":
            # Задание диапазона по X и Y внутри загона с отступом
            # Отступ от границы загона, 10 пикселей
            min_x = self.chicken_pen[0] + 100  # Отступ от левой границы
            max_x = self.chicken_pen[0] + self.chicken_pen[2] - 100  # Отступ от правой границы
            min_y = self.chicken_pen[1] + 100  # Отступ от верхней границы
            max_y = self.chicken_pen[1] + self.chicken_pen[3] - 100  # Отступ от нижней границы

            # Генерация случайной позиции внутри этих границ
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            return (x, y), self.chicken_pen
        else:
            # Отступ для коровы
            min_x = self.cow_pen[0] + 100  # Отступ от левой границы
            max_x = self.cow_pen[0] + self.cow_pen[2] - 100  # Отступ от правой границы
            min_y = self.cow_pen[1] + 100  # Отступ от верхней границы
            max_y = self.cow_pen[1] + self.cow_pen[3] - 100  # Отступ от нижней границы

            # Генерация случайной позиции внутри этих границ
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            return (x, y), self.cow_pen

    def draw(self, farmer, store, time_manager, show_store, store_message, message_handler):
        screen = self.screen
        images = self.images

        # Фон: день/ночь
        current_background = images["background1"] if time_manager.dayflag else images["background2"]
        screen.blit(current_background, (0, 0))

        # Объекты на карте
        screen.blit(images["store"], (580, -90))
        screen.blit(images["farmer"], (farmer.x, farmer.y))

        for plant in farmer.plants:
            screen.blit(plant.image, (plant.x, plant.y))
        for animal in farmer.animals:
            screen.blit(animal.image, (animal.x, animal.y))
            animal.update(self.walls)

        # Интерфейс: ресурсы
        screen.blit(self.status_font.render(f"Баланс: {farmer.money}", True, BROWN), (20, 20))
        screen.blit(self.status_font.render(f"День: {time_manager.day}", True, BROWN), (20, 50))

        chicken_count = sum(1 for animal in farmer.animals if animal.name == "Курица")
        cow_count = sum(1 for animal in farmer.animals if animal.name == "Корова")

        any_hungry_chicken = any(animal.hungry for animal in farmer.animals if animal.name == "Курица")
        any_hungry_cow = any(animal.hungry for animal in farmer.animals if animal.name == "Корова")

        chicken_status = f"{chicken_count} ({'Г' if any_hungry_chicken else 'С'})"
        cow_status = f"{cow_count} ({'Г' if any_hungry_cow else 'С'})"

        screen.blit(self.status_font.render(f"Куры: {chicken_status}", True, BROWN), (20, 80))
        screen.blit(self.status_font.render(f"Коровы: {cow_status}", True, BROWN), (20, 110))
        screen.blit(self.status_font.render(f"Яиц: {farmer.eggs}", True, BROWN), (20, 140))
        screen.blit(self.status_font.render(f"Молока: {farmer.milk}", True, BROWN), (20, 170))
        screen.blit(self.status_font.render(f"Растений: {farmer.wheat}", True, BROWN), (20, 200))

        if show_store:
            store.draw(screen, farmer.money)
            if store_message:
                msg_surface = self.message_font.render(store_message, True, (255, 255, 0))
                screen.blit(msg_surface, (400 - msg_surface.get_width() // 2, 750))

            # Отображение сообщений через MessageHandler
        message_handler.draw(screen, self.message_font, 460, 570)