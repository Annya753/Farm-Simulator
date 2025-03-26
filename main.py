import pygame
from models import Farmer, Plant, Animal
from store import Store
from time_manager import TimeManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Симулятор фермы")
    clock = pygame.time.Clock()

    images = {
        "background1": pygame.image.load(r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\background1.png"),
        "background2": pygame.image.load(r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\background2.png"),
        "wheat": pygame.image.load(r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\wheat.png"),
        "cow": pygame.image.load(r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\cow.png"),
        "chicken": pygame.image.load(r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\chicken.png"),
        "farmer": pygame.image.load(r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\farmer.png"),
        "store": pygame.image.load(r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\store.png")
    }

    farmer = Farmer("Ivan", 50, 50)
    store = Store(images)
    time_manager = TimeManager()
    store_zone = pygame.Rect(650, 30, 100, 100)
    show_store = False
    running = True

    while running:
        current_background = images["background1"] if time_manager.dayflag else images["background2"]
        screen.blit(current_background, (0, 0))
        screen.blit(images["store"], (650, 30))
        screen.blit(images["farmer"], (farmer.x, farmer.y))

        for plant in farmer.plants:
            screen.blit(plant.image, (plant.x, plant.y))
        for animal in farmer.animals:
            screen.blit(animal.image, (animal.x, animal.y))

        font = pygame.font.Font(None, 36)
        balance_text = font.render(f"Баланс: {farmer.money} | День: {time_manager.day}", True, (255, 255, 255))
        screen.blit(balance_text, (10, 10))

        status_font = pygame.font.Font(None, 24)
        time_of_day = "День" if time_manager.dayflag else "Ночь"
        day_time_text = status_font.render(f"{time_of_day}", True, (255, 255, 255))
        screen.blit(day_time_text, (10, 40))

        for i, animal in enumerate(farmer.animals):
            animal_status = "Накормлена" if not animal.hungry else "Голодна"
            status_text = status_font.render(f"{animal.name}: {animal_status}", True, (255, 255, 255))
            screen.blit(status_text, (10, 70 + 30 * i))

        if show_store:
            store.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and store_zone.collidepoint(farmer.x, farmer.y):
                    show_store = not show_store
                elif event.key == pygame.K_f:
                    # Проверяем, есть ли животные рядом с фермером, чтобы покормить
                    for animal in farmer.animals:
                        if abs(farmer.x - animal.x) < 50 and abs(farmer.y - animal.y) < 50:
                            animal.feed()
                            break

            elif event.type == pygame.MOUSEBUTTONDOWN and show_store:
                store.handle_click(event.pos, farmer)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            farmer.move(0, -1)
        if keys[pygame.K_DOWN]:
            farmer.move(0, 1)
        if keys[pygame.K_LEFT]:
            farmer.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            farmer.move(1, 0)

        if show_store and not store_zone.collidepoint(farmer.x, farmer.y):
            show_store = False

        time_manager.advance_time(farmer, time_manager.dayflag)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()