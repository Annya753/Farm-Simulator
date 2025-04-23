import pygame

class MainMenu:
    def __init__(self, screen, font_path):
        self.screen = screen
        self.font_large = pygame.font.Font(font_path, 72)
        self.font_medium = pygame.font.Font(font_path, 48)
        self.background = pygame.image.load("assets/farm_background.png")  # Добавьте свое изображение
        self.background = pygame.transform.scale(self.background, screen.get_size())
        self.title_color = (255, 215, 0)  # Золотой
        self.button_hover_color = (230, 230, 230)
        self.button_normal_color = (200, 200, 200)

        # Кнопки
        self.start_button = pygame.Rect(450, 300, 300, 80)
        self.quit_button = pygame.Rect(450, 400, 300, 80)

        # Текст
        self.title = self.font_large.render("Фермерский Симулятор", True, (255, 255, 255))
        self.start_text = self.font_medium.render("Новая игра", True, (0, 0, 0))
        self.quit_text = self.font_medium.render("Выход", True, (0, 0, 0))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title, (600 - self.title.get_width() // 2, 150))

        # Рисуем кнопки
        mouse_pos = pygame.mouse.get_pos()
        start_color = self.button_hover_color if self.start_button.collidepoint(mouse_pos) else self.button_normal_color
        quit_color = self.button_hover_color if self.quit_button.collidepoint(mouse_pos) else self.button_normal_color

        # Рисуем кнопки с учетом наведения
        pygame.draw.rect(self.screen, start_color, self.start_button, border_radius=10)
        pygame.draw.rect(self.screen, quit_color, self.quit_button, border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), self.start_button, 2, border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), self.quit_button, 2, border_radius=10)
        # Текст на кнопках
        self.screen.blit(self.start_text,
                         (self.start_button.x + self.start_button.width // 2 - self.start_text.get_width() // 2,
                          self.start_button.y + self.start_button.height // 2 - self.start_text.get_height() // 2))

        self.screen.blit(self.quit_text,
                         (self.quit_button.x + self.quit_button.width // 2 - self.quit_text.get_width() // 2,
                          self.quit_button.y + self.quit_button.height // 2 - self.quit_text.get_height() // 2))

    def handle_click(self, pos):
        if self.start_button.collidepoint(pos):
            return "start"
        elif self.quit_button.collidepoint(pos):
            return "quit"
        return None