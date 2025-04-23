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
        self.box_rect = pygame.Rect(505, 200, 70, 41)
        self.box_image = images["box"]


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
        if animal_type.lower() == "курица":
            min_x = self.chicken_pen[0] + 100
            max_x = self.chicken_pen[0] + self.chicken_pen[2] - 100
            min_y = self.chicken_pen[1] + 100
            max_y = self.chicken_pen[1] + self.chicken_pen[3] - 100

            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            return (x, y), self.chicken_pen
        else:

            min_x = self.cow_pen[0] + 100
            max_x = self.cow_pen[0] + self.cow_pen[2] - 100
            min_y = self.cow_pen[1] + 100
            max_y = self.cow_pen[1] + self.cow_pen[3] - 100

            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            return (x, y), self.cow_pen

    def draw(self, farmer, store, time_manager, show_store, store_message, message_handler):
        screen = self.screen
        images = self.images

        current_background = images["background1"] if time_manager.dayflag else images["background2"]
        screen.blit(current_background, (0, 0))

        for plant in farmer.plants:
            screen.blit(plant.images_dict[plant.stage], (plant.x, plant.y))
        screen.blit(images["store"], (580, -90))
        screen.blit(self.box_image, (self.box_rect.x, self.box_rect.y))
        box_highlight = self.box_rect.collidepoint(pygame.mouse.get_pos())
        if box_highlight:
            border_size = 3
            highlight_color = (255, 255, 255)

            pygame.draw.rect(
                screen,
                highlight_color,
                pygame.Rect(
                    self.box_rect.x - border_size,
                    self.box_rect.y - border_size,
                    self.box_rect.width + border_size * 2,
                    self.box_rect.height + border_size * 2
                ),
                border_size
            )

            hint_text = "Нажмите P для продажи"
            hint_surface = self.status_font.render(hint_text, True, (255, 255, 255))

            screen.blit(
                hint_surface,
                (self.box_rect.x + (self.box_rect.width // 2 - hint_surface.get_width() // 2),
                 self.box_rect.y - 30)
            )
        screen.blit(images["farmer"], (farmer.x, farmer.y))

        for animal in farmer.animals:
            screen.blit(animal.image, (animal.x, animal.y))
            animal.update(self.walls)

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
        screen.blit(self.status_font.render(f"Растений: {sum(farmer.harvest.values())}", True, BROWN), (20, 200))

        if show_store:
            store.draw(screen, farmer.money)
            if store_message:
                msg_surface = self.message_font.render(store_message, True, (255, 255, 0))
                screen.blit(msg_surface, (400 - msg_surface.get_width() // 2, 750))

        message_handler.draw(screen, self.message_font, 460, 570)