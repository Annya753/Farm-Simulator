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
    images = {"carrot": {
        0: pygame.image.load(os.path.join(asset_path, "carrot1.png")),
        1: pygame.image.load(os.path.join(asset_path, "carrot2.png")),
        2: pygame.image.load(os.path.join(asset_path, "carrot3.png"))
    },
        "potato": {
        0: pygame.image.load(os.path.join(asset_path, "potato1.png")),
        1: pygame.image.load(os.path.join(asset_path, "potato2.png")),
        2: pygame.image.load(os.path.join(asset_path, "potato3.png"))
    },
        "onion": {
        0: pygame.image.load(os.path.join(asset_path, "onion1.png")),
        1: pygame.image.load(os.path.join(asset_path, "onion2.png")),
        2: pygame.image.load(os.path.join(asset_path, "onion3.png"))
    },
        "potato_card": pygame.image.load(os.path.join(asset_path, "potato.png")),
        "onion_card": pygame.image.load(os.path.join(asset_path, "onion.png")),
        "carrot_card": pygame.image.load(os.path.join(asset_path, "carrot.png")),
        "background1": pygame.image.load(os.path.join(asset_path, "background1.png")),
        "background2": pygame.image.load(os.path.join(asset_path, "background2.png")),
        "box": pygame.image.load(os.path.join(asset_path, "box.png")),
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
    time_manager = TimeManager()
    store = Store(images, time_manager)
    message_handler = MessageHandler()
    map = Map(screen, images, message_font, status_font)

    store_message = ""
    MESSAGE_DURATION = 30
    store_zone = pygame.Rect(650, 30, 100, 100)
    show_store = False
    running = True

    def check_collision(new_x, new_y):
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
                    messages = farmer.collect_products()
                    message_handler.add_message("\n".join(messages), MESSAGE_DURATION)

                elif event.key == pygame.K_c:
                    fed_count = 0
                    for animal in farmer.animals:
                        if animal.name.lower() == "курица" and animal.is_near(farmer):
                            if animal.feed():
                                fed_count += 1
                                message_handler.add_message("Курица накормлена", MESSAGE_DURATION)
                            else:
                                message_handler.add_message("Курица не голодна", MESSAGE_DURATION)
                    if fed_count == 0:
                        message_handler.add_message("Нет голодных кур рядом", MESSAGE_DURATION)

                elif event.key == pygame.K_a:
                    messages = farmer.check_animals_status()
                    message_handler.add_message("\n".join(messages), MESSAGE_DURATION)

                elif event.key == pygame.K_v:
                    fed_count = 0
                    for animal in farmer.animals:
                        if animal.name.lower() == "корова" and animal.is_near(farmer):
                            if animal.feed():
                                fed_count += 1
                                message_handler.add_message("Корова накормлена", MESSAGE_DURATION)
                            else:
                                message_handler.add_message("Корова не голодна", MESSAGE_DURATION)
                            break
                    if fed_count == 0:
                        message_handler.add_message("Нет голодных коров рядом", MESSAGE_DURATION)

                elif event.key == pygame.K_w:
                    watered = False
                    for i, plant in enumerate(farmer.plants):
                        if plant.is_near(farmer):
                            message = farmer.water_plant(i)
                            message_handler.add_message(message, MESSAGE_DURATION)
                            watered = True
                            break
                    if not watered:
                        message_handler.add_message("Подойдите ближе к растению", MESSAGE_DURATION)

                elif event.key == pygame.K_h:
                    harvested = False
                    for i, plant in enumerate(farmer.plants):
                        if plant.is_near(farmer):
                            message = farmer.harvest_plant(i)
                            message_handler.add_message(message, MESSAGE_DURATION)
                            harvested = True
                            break
                    if not harvested:
                        message_handler.add_message("Нет растений рядом", MESSAGE_DURATION)

                elif event.key == pygame.K_s:
                    messages = farmer.check_plants_status()
                    message_handler.add_message("\n".join(messages), MESSAGE_DURATION)

                elif event.key == pygame.K_p:
                    if map.box_rect.collidepoint(farmer.x, farmer.y):
                        total = farmer.sell_products()
                        if total > 0:
                            message_handler.add_message(f"Сумма продажи: {total}", MESSAGE_DURATION)
                        else:
                            message_handler.add_message("Нет продукции для продажи", MESSAGE_DURATION)
                    else:
                        message_handler.add_message("Идите к ящику для продажи", MESSAGE_DURATION)

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