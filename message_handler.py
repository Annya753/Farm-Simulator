import pygame
import os

asset_path = os.path.join(os.path.dirname(__file__), "assets")

class MessageHandler:
    def __init__(self):
        self.current_message = None
        self.time_remaining = 0
        self.message_bg = pygame.image.load(os.path.join(asset_path, "message_handler.png"))

    def add_message(self, message, duration=120):
        self.current_message = message
        self.time_remaining = duration

    def update(self):
        if self.current_message:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.current_message = None

    def draw(self, screen, font, x_pos, y_pos):
        if self.current_message:
            screen.blit(self.message_bg, (200, 480))

            text_surface = font.render(self.current_message, True, (84, 28, 28))
            screen.blit(text_surface, (x_pos - text_surface.get_width() // 2, y_pos - text_surface.get_height() // 2))