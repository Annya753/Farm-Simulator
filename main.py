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
        "background": pygame.image.load(r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\background.png"),
        "wheat": pygame.image.load(r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\wheat.png"),
     #  "cabbage": pygame.image.load("cabbage.png"),
        "cow": pygame.image.load(r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\cow.png"),
        "chicken": pygame.image.load(r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\chicken.png"),
        "farmer": pygame.image.load(r"C:\Users\belug\PycharmProjects\PythonProjectOursimulator\Farm-Simulator\farmer.png")
    }

    farmer = Farmer("Игрок 1", 50, 50)
    store = Store(images)
    time_manager = TimeManager()
    running = True

    while running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            farmer.move(0, -1)
        if keys[pygame.K_DOWN]:
            farmer.move(0, 1)
        if keys[pygame.K_LEFT]:
            farmer.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            farmer.move(1, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(images["background"], (0, 0))
        screen.blit(images["farmer"], (farmer.x, farmer.y))
        for plant in farmer.plants:
            screen.blit(plant.image, (plant.x, plant.y))
        for animal in farmer.animals:
            screen.blit(animal.image, (animal.x, animal.y))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
