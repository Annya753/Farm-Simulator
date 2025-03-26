from models import Animal, Plant
import pygame

class Store:
    def __init__(self, images):
        self.images = images
        self.items = [
            (Plant("Пшеница", 3, 50, 100, images["wheat"], 200, 300), pygame.Rect(100, 100, 150, 50)),
            (Animal("Корова", 700, "молоко", 50, images["cow"], 400, 300), pygame.Rect(100, 160, 150, 50)),
            (Animal("Курица", 300, "яйца", 10, images["chicken"], 600, 500), pygame.Rect(100, 220, 150, 50))
        ]

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), (80, 80, 200, 300))
        font = pygame.font.Font(None, 24)
        for item, rect in self.items:
            pygame.draw.rect(screen, (150, 150, 150), rect)
            text = font.render(f"{item.name} ({item.price})", True, (0, 0, 0))
            screen.blit(text, (rect.x + 10, rect.y + 10))

    def handle_click(self, pos, farmer):
        for item, rect in self.items:
            if rect.collidepoint(pos) and farmer.money >= item.price:
                farmer.money -= item.price
                if isinstance(item, Plant):
                    x_position = 100 + len(farmer.plants) * 50
                    y_position = 500
                    farmer.add_item(
                        Plant(item.name, item.growth_time, item.price, item.sell_price, item.image, x_position,
                              y_position))
                    print(f"Добавлена пшеница на ({x_position}, {y_position})")

                elif isinstance(item, Animal):
                    if item.name.lower() == "корова":
                        x_position = 350 + len([a for a in farmer.animals if a.name.lower() == "корова"]) * 50
                        y_position = 500
                    elif item.name.lower() == "курица":
                        x_position = 600 + len([a for a in farmer.animals if a.name.lower() == "курица"]) * 50
                        y_position = 500
                    else:
                        continue  # если что-то пошло не так, просто пропускаем

                    farmer.add_item(
                        Animal(item.name, item.price, item.product, item.product_price, item.image, x_position, y_position))
                    print(f"Добавлено животное: {item.name} на ({x_position}, {y_position})")