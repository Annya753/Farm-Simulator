import pygame
from models import Farmer, Plant, Animal
from store import Store
from time_manager import TimeManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Симулятор фермы")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

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
        print(f"🎮 Текущие животные на ферме: {[a.name for a in farmer.animals]}")

        balance_text = font.render(f"Баланс: {farmer.money}", True, (0, 0, 0))
        screen.blit(balance_text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and store_zone.collidepoint(farmer.x, farmer.y):
                    show_store = not show_store
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

        if show_store:
            store.draw(screen)

        time_manager.advance_time(farmer, time_manager.dayflag)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()