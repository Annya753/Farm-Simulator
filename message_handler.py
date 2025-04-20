import pygame
import os

asset_path = os.path.join(os.path.dirname(__file__), "assets")

class MessageHandler:
    def __init__(self):
        self.current_message = None  # Текущее сообщение
        self.time_remaining = 0  # Время, оставшееся для отображения сообщения
        self.message_bg = pygame.image.load(os.path.join(asset_path, "message_handler.png"))  # Загружаем картинку для фона

    def add_message(self, message, duration=120):
        """Добавление нового сообщения, которое заменяет старое."""
        self.current_message = message
        self.time_remaining = duration

    def update(self):
        """Обновление состояния сообщения: уменьшение времени оставшегося для отображения."""
        if self.current_message:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.current_message = None  # Убираем сообщение после окончания времени

    def draw(self, screen, font, x_pos, y_pos):
        """Отрисовка текущего сообщения на экране."""
        if self.current_message:
            # Рисуем фон сообщения (картинку)
            screen.blit(self.message_bg, (200, 480))  # Отображаем картинку в нужной области

            # Отображаем текущее сообщение поверх картинки
            text_surface = font.render(self.current_message, True, (84, 28, 28))
            screen.blit(text_surface, (x_pos - text_surface.get_width() // 2, y_pos - text_surface.get_height() // 2))