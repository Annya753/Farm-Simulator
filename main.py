import pygame
from models import Farmer, Plant, Animal
from store import Store
from time_manager import TimeManager
from message_handler import MessageHandler

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Симулятор фермы")
    clock = pygame.time.Clock()
    message_font = pygame.font.Font(None, 32)
    images = {
        "background1": pygame.image.load(
            r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\background1.png"),
        "background2": pygame.image.load(
            r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\background2.png"),
        "wheat": pygame.image.load(
            r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\wheat.png"),
        "cow": pygame.image.load(r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\cow.png"),
        "chicken": pygame.image.load(
            r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\chicken.png"),
        "farmer": pygame.image.load(
            r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\farmer.png"),
        "store": pygame.image.load(r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\store.png")
    }

    farmer = Farmer("Ivan", 50, 50)
    store = Store(images)
    time_manager = TimeManager()
    message_handler = MessageHandler()

    status_messages = []
    store_message = ""
    message_timer = 0
    MESSAGE_DURATION = 120

    store_zone = pygame.Rect(650, 30, 100, 100)
    show_store = False
    running = True

    status_font = pygame.font.Font(None, 24)

    def check_collision(new_x, new_y):
        for plant in farmer.plants:
            if pygame.Rect(plant.x, plant.y, 50, 50).colliderect(new_x, new_y, 50, 50):
                return True
        for animal in farmer.animals:
            if pygame.Rect(animal.x, animal.y, 50, 50).colliderect(new_x, new_y, 50, 50):
                return True
        return False

    while running:
        current_background = images["background1"] if time_manager.dayflag else images["background2"]
        screen.blit(current_background, (0, 0))
        screen.blit(images["store"], (650, 30))
        screen.blit(images["farmer"], (farmer.x, farmer.y))

        for plant in farmer.plants:
            screen.blit(plant.image, (plant.x, plant.y))
        for animal in farmer.animals:
            screen.blit(animal.image, (animal.x, animal.y))

            # Основная информация
        screen.blit(status_font.render(f"Баланс: {farmer.money}", True, (255, 255, 255)), (10, 10))
        screen.blit(status_font.render(f"День: {time_manager.day}", True, (255, 255, 255)), (10, 40))

        chicken_count = sum(1 for animal in farmer.animals if animal.name == "Курица")
        cow_count = sum(1 for animal in farmer.animals if animal.name == "Корова")

        any_hungry_chicken = any(animal.hungry for animal in farmer.animals if animal.name == "Курица")
        any_hungry_cow = any(animal.hungry for animal in farmer.animals if animal.name == "Корова")

        chicken_status = f"{chicken_count} ({'Голодны' if any_hungry_chicken else 'Сыты'})"
        cow_status = f"{cow_count} ({'Голодны' if any_hungry_cow else 'Сыты'})"

        screen.blit(status_font.render(f"Куры: {chicken_status}", True, (255, 255, 255)), (10, 70))
        screen.blit(status_font.render(f"Коровы: {cow_status}", True, (255, 255, 255)), (10, 100))
        screen.blit(status_font.render(f"Яиц: {farmer.eggs}", True, (255, 255, 255)), (10, 130))
        screen.blit(status_font.render(f"Молока: {farmer.milk}", True, (255, 255, 255)), (10, 160))

        if show_store:
            store.draw(screen, farmer.money)
            if store_message:
                msg_surface = message_font.render(store_message, True, (255, 255, 0))
                screen.blit(msg_surface, (400 - msg_surface.get_width() // 2, 750))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and store_zone.collidepoint(farmer.x, farmer.y):
                    show_store = not show_store
                    store_message = ""
                elif event.key == pygame.K_f:
                    if not farmer.animals:
                        status_messages = ["Нет животных для сбора"]
                    else:
                        collection_result = farmer.collect_all_products()
                        status_messages = collection_result
                    message_timer = MESSAGE_DURATION
                elif event.key == pygame.K_p:
                    if farmer.eggs == 0 and farmer.milk == 0:
                        status_messages = ["Нет продукции для продажи"]
                    else:
                        old_money = farmer.money
                        status_messages = farmer.sell_products()
                        status_messages.append(f"Баланс: {old_money} → {farmer.money}")
                    message_timer = MESSAGE_DURATION
                elif event.key == pygame.K_c:
                    status_messages = [farmer.feed_all_chickens()]
                    message_timer = MESSAGE_DURATION
                elif event.key == pygame.K_v:
                    status_messages = [farmer.feed_all_cows()]
                    message_timer = MESSAGE_DURATION
            elif event.type == pygame.MOUSEBUTTONDOWN and show_store:
                result = store.handle_click(event.pos, farmer)
                if result is False:
                    show_store = False
                    store_message = ""
                elif result:
                    store_message = result
                    message_timer = MESSAGE_DURATION
            elif event.type == pygame.USEREVENT:
                store_message = ""

            # Отображение статусных сообщений
        if message_timer > 0:
            message_bg = pygame.Surface((800, 100), pygame.SRCALPHA)
            message_bg.fill((0, 0, 0, 150))  # Полупрозрачный черный фон
            screen.blit(message_bg, (0, 700))
            for i, msg in enumerate(status_messages):
                text_surface = message_font.render(msg, True, (255, 255, 0))  # Желтый текст
                screen.blit(text_surface, (400 - text_surface.get_width() // 2, 750 - i * 30))

            message_timer -= 1
        else:
            status_messages = []

            # Управление фермером
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