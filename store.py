from models import Animal, Plant
import pygame

class Store:
    def __init__(self, images):
        self.images = images
        self.items = [
            (Plant("Пшеница", 3, 50, 100, images["wheat"], 0, 0), pygame.Rect(200, 250, 150, 50), 5),
            (Animal("Корова", 700, "молоко", 50, images["cow"], 0, 0), pygame.Rect(200, 310, 150, 50), 3),
            (Animal("Курица", 300, "яйца", 10, images["chicken"], 0, 0), pygame.Rect(200, 370, 150, 50), 10)
        ]

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), (180, 230, 500, 220), border_radius=20)
        font = pygame.font.Font(None, 24)

        for item, rect, quantity in self.items:
            button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(button_surface, (0, 0, 0, 100), (0, 0, rect.width, rect.height), border_radius=10)
            screen.blit(button_surface, (rect.x, rect.y))
            text = font.render(f"{item.name} ({item.price})", True, (0, 0, 0))
            screen.blit(text, (rect.x + 10, rect.y + 10))

            quantity_text = font.render(f"Осталось: {quantity}", True, (0, 0, 0))
            screen.blit(quantity_text, (rect.x + 10, rect.y + 30))

    def handle_click(self, pos, farmer):
        for i, (item, rect, quantity) in enumerate(self.items):
            if rect.collidepoint(pos) and farmer.money >= item.price and quantity > 0:
                farmer.money -= item.price
                if isinstance(item, Plant):
                    x_position = 100 + len(farmer.plants) * 50
                    y_position = 500
                    farmer.add_item(
                        Plant(item.name, item.growth_time, item.price, item.sell_price, item.image, x_position,
                              y_position))
                elif isinstance(item, Animal):
                    if item.name.lower() == "корова":
                        x_position = 350 + len([a for a in farmer.animals if a.name.lower() == "корова"]) * 50
                        y_position = 500
                    elif item.name.lower() == "курица":
                        x_position = 600 + len([a for a in farmer.animals if a.name.lower() == "курица"]) * 50
                        y_position = 500
                    else:
                        continue
                    farmer.add_item(
                        Animal(item.name, item.price, item.product, item.product_price, item.image, x_position,
                               y_position))

                self.items[i] = (item, rect, quantity - 1)
