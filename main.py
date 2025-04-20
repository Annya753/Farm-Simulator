import pygame
import os
from models import Farmer, Plant, Animal
from store import Store
from time_manager import TimeManager
from message_handler import MessageHandler
from map import Map

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 654))
    pygame.display.set_caption("Симулятор фермы")
    clock = pygame.time.Clock()
    font_path = "PixelifySans-VariableFont_wght.ttf"
    message_font = pygame.font.Font(font_path, 32)
    status_font = pygame.font.Font(font_path, 19)

    asset_path = os.path.join(os.path.dirname(__file__), "assets")
    images = {
        "background1": pygame.image.load(os.path.join(asset_path, "background1.png")),
        "background2": pygame.image.load(os.path.join(asset_path, "background2.png")),
        "wheat": pygame.image.load(os.path.join(asset_path, "wheat.png")),
        "cow": pygame.image.load(os.path.join(asset_path, "cow.png")),
        "chicken": pygame.image.load(os.path.join(asset_path, "chicken.png")),
        "farmer": pygame.transform.scale(
        pygame.image.load(os.path.join(asset_path, "farmer.png")),
        (50, 60)
),
        "store": pygame.transform.scale(
        pygame.image.load(os.path.join(asset_path, "store.png")),
        (400, 400)
)
    }

    farmer = Farmer("Ivan", 250, 240)
    store = Store(images)
    time_manager = TimeManager()
    message_handler = MessageHandler()
    map = Map(screen, images, message_font, status_font)

    store_message = ""
    MESSAGE_DURATION = 120
    store_zone = pygame.Rect(650, 30, 100, 100)
    show_store = False
    running = True

    def check_collision(new_x, new_y):
        for plant in farmer.plants:
            if pygame.Rect(plant.x, plant.y, 50, 50).colliderect(new_x, new_y, 50, 50):
                return True
        for animal in farmer.animals:
            if pygame.Rect(animal.x, animal.y, 50, 50).colliderect(new_x, new_y, 50, 50):
                return True
        return False

    while running:
        map.draw(farmer, store, time_manager, show_store, store_message, message_handler)
        message_handler.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and store_zone.collidepoint(farmer.x, farmer.y):
                    show_store = not show_store
                    store_message = ""
                elif event.key == pygame.K_f:
                    if not farmer.animals:
                        message_handler.add_message("Нет животных для сбора", MESSAGE_DURATION)
                    else:
                        messages = farmer.collect_all_products()
                        message_handler.add_message("\n".join(messages), MESSAGE_DURATION)
                elif event.key == pygame.K_c:
                    message_handler.add_message(farmer.feed_all_chickens(), MESSAGE_DURATION)
                elif event.key == pygame.K_v:
                    message_handler.add_message(farmer.feed_all_cows(), MESSAGE_DURATION)
                elif event.key == pygame.K_w:
                    if farmer.plants:
                        message_handler.add_message(farmer.water_plant(0), MESSAGE_DURATION)
                    else:
                        message_handler.add_message("Нет растений для полива", MESSAGE_DURATION)
                elif event.key == pygame.K_h:
                    if farmer.plants:
                        for i, plant in enumerate(farmer.plants[:]):
                            if plant.is_ripe():
                                message_handler.add_message(farmer.harvest_plant(i), MESSAGE_DURATION)
                                break
                        else:
                            message_handler.add_message("Нет созревших растений", MESSAGE_DURATION)
                    else:
                        message_handler.add_message("Нет растений", MESSAGE_DURATION)
                elif event.key == pygame.K_s:
                    if farmer.plants:
                        message_handler.add_message("\n".join(farmer.check_plants_status()), MESSAGE_DURATION)
                    else:
                        message_handler.add_message("Нет растений", MESSAGE_DURATION)
                elif event.key == pygame.K_p:
                    if farmer.eggs == 0 and farmer.milk == 0 and farmer.wheat == 0:
                        message_handler.add_message("Нет продукции для продажи", MESSAGE_DURATION)
                    else:
                        old_money = farmer.money
                        messages = farmer.sell_products()
                        messages.append(f"Баланс: {old_money} → {farmer.money}")
                        message_handler.add_message("\n".join(messages), MESSAGE_DURATION)

            elif event.type == pygame.MOUSEBUTTONDOWN and show_store:
                result = store.handle_click(event.pos, farmer, map)
                if result is False:
                    show_store = False
                    store_message = ""
                elif result:
                    store_message = result
                    message_timer = MESSAGE_DURATION

            elif event.type == pygame.USEREVENT:
                store_message = ""

        keys = pygame.key.get_pressed()
        new_x, new_y = farmer.x, farmer.y
        if keys[pygame.K_UP]:
            new_y -= 5
        if keys[pygame.K_DOWN]:
            new_y += 5
        if keys[pygame.K_LEFT]:
            new_x -= 5
        if keys[pygame.K_RIGHT]:
            new_x += 5

        if not check_collision(new_x, new_y):
            farmer.x, farmer.y = new_x, new_y

        if show_store and not store_zone.collidepoint(farmer.x, farmer.y):
            show_store = False

        time_manager.advance_time(farmer)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
# z nen ghjcnj gbwliefhweon