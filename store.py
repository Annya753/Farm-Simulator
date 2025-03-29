import pygame
from models import Animal, Plant


class Store:
    def __init__(self, images):
        self.images = images
        self.items = [
            {
                "type": "plant",
                "item": Plant("Пшеница", 3, 50, 100, images["wheat"], 0, 0),
                "quantity": 5,
                "description": "Созревает за 3 дня. Продается за 100. Требует полива."
            },
            {
                "type": "animal",
                "item": Animal("Корова", 700, "молоко", 50, images["cow"], 0, 0),
                "quantity": 3,
                "description": "Дает молоко. Цена: 50 за шт. Требует кормления."  },
            {
                "type": "animal",
                "item": Animal("Курица", 300, "яйца", 10, images["chicken"], 0, 0),
                "quantity": 10,
                "description": "Несет яйца. Цена: 10 за шт. Требует кормления."       }
        ]
        self.last_click_time = 0
        self.close_btn_rect = pygame.Rect(640, 122, 30, 30)

        # Инициализация шрифтов
        self._init_fonts()

    def _init_fonts(self):
        """Инициализация шрифтов с обработкой ошибок"""
        try:
            self.title_font = pygame.font.Font(None, 36)
            self.item_font = pygame.font.Font(None, 28)
            self.price_font = pygame.font.Font(None, 26)
            self.desc_font = pygame.font.Font(None, 22)
        except:
            self.title_font = pygame.font.SysFont("arial", 36, bold=True)
            self.item_font = pygame.font.SysFont("arial", 28)
            self.price_font = pygame.font.SysFont("arial", 26)
            self.desc_font = pygame.font.SysFont("arial", 22)

    def _wrap_text(self, text, font, max_width):
        """Перенос текста на несколько строк"""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def draw(self, screen, farmer_money):
        s = pygame.Surface((800, 800), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        screen.blit(s, (0, 0))


        main_rect = pygame.Rect(170, 100, 520, 570)
        pygame.draw.rect(screen, (245, 235, 220), main_rect, border_radius=15)
        pygame.draw.rect(screen, (180, 150, 100), main_rect, 3, border_radius=15)


        title = self.title_font.render("ФЕРМЕРСКИЙ МАГАЗИН", True, (90, 60, 30))
        screen.blit(title, (400 - title.get_width() // 2 + 10, 135))

        # Кнопка закрытия с hover-эффектом
        mouse_pos = pygame.mouse.get_pos()
        close_hover = self.close_btn_rect.collidepoint(mouse_pos)
        close_color = (220, 90, 90) if close_hover else (200, 80, 80)
        pygame.draw.rect(screen, close_color, self.close_btn_rect, border_radius=15)
        pygame.draw.rect(screen, (150, 50, 50), self.close_btn_rect, 2, border_radius=15)
        close_text = self.item_font.render("×", True, (255, 255, 255))
        screen.blit(close_text, (650, 125))

        # Отрисовка товаров
        for i, item_data in enumerate(self.items):
            self._draw_item(screen, i, item_data, farmer_money, mouse_pos)

    def _draw_item(self, screen, index, item_data, farmer_money, mouse_pos):
        """Отрисовка карточки товара"""
        item = item_data["item"]
        rect = pygame.Rect(200, 190 + index * 160, 430, 150)
        item_data["rect"] = rect
        can_afford = farmer_money >= item.price
        is_available = item_data["quantity"] > 0
        hover = rect.collidepoint(mouse_pos) and is_available

        # Фон карточки
        bg_color = (255, 252, 240) if hover else (250, 248, 235)
        if not is_available:
            bg_color = (230, 230, 230)
        elif not can_afford:
            bg_color = (240, 220, 220)

        pygame.draw.rect(screen, bg_color, rect, border_radius=12)
        pygame.draw.rect(screen, (200, 180, 160), rect, 2, border_radius=12)

        # Иконка с рамкой
        icon_rect = pygame.Rect(rect.x + 15, rect.y + 15, 50, 50)
        pygame.draw.rect(screen, (230, 220, 200), icon_rect, border_radius=8)
        pygame.draw.rect(screen, (190, 170, 140), icon_rect, 2, border_radius=8)
        screen.blit(pygame.transform.scale(item.image, (40, 40)), (rect.x + 20, rect.y + 20))

        # Текстовая информация
        text_x = rect.x + 80
        text_y = rect.y + 15

        # Название и категория
        name_text = self.item_font.render(item.name, True, (70, 50, 30))
        screen.blit(name_text, (text_x, text_y))

        # Цена и наличие
        price_color = (0, 150, 70) if can_afford else (200, 70, 50)
        price_text = self.price_font.render(f"{item.price}", True, price_color)
        screen.blit(price_text, (text_x, text_y + 30))

        avail_text = self.price_font.render(
            f"✓ В наличии ({item_data['quantity']})" if is_available else "✗ Нет в наличии",
            True,
            (0, 130, 0) if is_available else (150, 0, 0)
        )
        screen.blit(avail_text, (text_x, text_y + 55))

        # Описание
        desc_lines = self._wrap_text(item_data['description'], self.desc_font, 340)
        for i, line in enumerate(desc_lines[:2]):
            screen.blit(
                self.desc_font.render(line, True, (90, 80, 70)),
                (text_x, text_y + 80 + i * 20)
            )

        # Кнопка "Купить" (при наведении)
        if hover:
            buy_rect = pygame.Rect(rect.x + rect.width - 110, rect.y + rect.height - 35, 100, 30)
            pygame.draw.rect(screen, (100, 180, 100), buy_rect, border_radius=15)
            pygame.draw.rect(screen, (50, 120, 50), buy_rect, 2, border_radius=15)
            buy_text = pygame.font.Font(None, 24).render("КУПИТЬ", True, (255, 255, 255))
            screen.blit(buy_text, (buy_rect.x + 17, buy_rect.y + 7))

    def handle_click(self, pos, farmer):
        current_time = pygame.time.get_ticks()

        # Защита от двойного клика
        if current_time - self.last_click_time < 300:
            return None
        self.last_click_time = current_time

        # Проверка кнопки закрытия
        if self.close_btn_rect.collidepoint(pos):
            return False

        # Обработка клика по товарам
        for item_data in self.items:
            if item_data.get('rect', None) and item_data['rect'].collidepoint(pos):
                item = item_data['item']

                if item_data['quantity'] <= 0:
                    return "Товар закончился!"

                if farmer.money < item.price:
                    return f"Не хватает {item.price - farmer.money}!"

                # Создаем новый экземпляр
                new_item = self._create_new_item(item, item_data['type'], farmer)
                farmer.add_item(new_item)
                farmer.money -= item.price
                item_data['quantity'] -= 1

                return f"Куплено: {item.name}!"

        return None

    def _create_new_item(self, item, item_type, farmer):
        """Создание нового экземпляра товара"""
        if item_type == 'plant':
            new_item = Plant(
                item.name, item.growth_time, item.price,
                item.sell_price, item.image, 0, 0
            )
            x_pos = 100 + len([p for p in farmer.plants if p.name == item.name]) * 60
            y_pos = 500
        else:
            new_item = Animal(
                item.name, item.price, item.product,
                item.product_price, item.image, 0, 0
            )
            if item.name == "Корова":
                x_pos = 350 + len([a for a in farmer.animals if a.name == "Корова"]) * 60
            else:
                x_pos = 600 + len([a for a in farmer.animals if a.name == "Курица"]) * 60
            y_pos = 500

        new_item.x, new_item.y = x_pos, y_pos
        return new_item