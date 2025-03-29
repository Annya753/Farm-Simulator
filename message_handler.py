import pygame


class MessageHandler:
    def __init__(self):
        self.message = ""
        self.show_message = False
        self.message_timer = 0
        self.FPS = 60

    def set_message(self, text, duration_seconds=2.0):
        self.message = str(text)
        self.show_message = True
        self.message_timer = int(duration_seconds * self.FPS)

    def update(self):
        if self.show_message and self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer <= 0:
                self.show_message = False

    def draw(self, screen, font):
        if self.show_message:
            # Прозрачный фон с желтым текстом
            text_surface = font.render(self.message, True, (255, 255, 0))  # Желтый цвет

            # Создаем полупрозрачную подложку
            bg_surface = pygame.Surface(
                (text_surface.get_width() + 20, text_surface.get_height() + 10),
                pygame.SRCALPHA
            )
            bg_surface.fill((0, 0, 0, 150))  # Черный с прозрачностью

            # Позиционирование
            x_pos = 400 - text_surface.get_width() // 2
            y_pos = 750 - text_surface.get_height()

            # Рисуем подложку и текст
            screen.blit(bg_surface, (x_pos - 10, y_pos - 5))
            screen.blit(text_surface, (x_pos, y_pos))