import pygame
from models import Animal, Plant

class Store:
    def __init__(self, images, time_manager, font_path="PixelifySans-VariableFont_wght.ttf"):
        self.images = images
        self.time_manager = time_manager
        self.font_path = font_path
        self.last_click_time = 0
        self.close_btn_rect = pygame.Rect(640, 122, 30, 30)
        self._init_fonts()

        self.transition_start_day = None

        self.items = [
            {
                "type": "plant",
                "key": "potato_stage",
                "stage": "potato",
                "item": Plant(
                    "Картошка",
                    3,
                    50,
                    100,
                    images["potato"],
                    0,
                    0
                ),
                "card_image": images["potato_card"],
                "quantity": 5,
                "description": "Созревает за 3 дня. Продается за 100. Требует полива.",
            },
            {
                "type": "animal",
                "item": Animal("Корова", 700, "молоко", 50, images["cow"], 0, 0),
                "quantity": 3,
                "description": "Дает молоко. Цена: 50 за шт. Требует кормления."
            },
            {
                "type": "animal",
                "item": Animal("Курица", 300, "яйца", 10, images["chicken"], 0, 0),
                "quantity": 6,
                "description": "Несет яйца. Цена: 10 за шт. Требует кормления."
            }
        ]

    def _init_fonts(self):
        self.title_font = pygame.font.Font(self.font_path, 33)
        self.item_font = pygame.font.Font(self.font_path, 25)
        self.price_font = pygame.font.Font(self.font_path, 23)
        self.desc_font = pygame.font.Font(self.font_path, 19)

    def _wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines, current_line = [], []

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
        self._update_store_logic()

        s = pygame.Surface((1200, 654), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        screen.blit(s, (0, 0))

        screen_width, screen_height = screen.get_size()
        main_width, main_height = 520, 570
        main_x = (screen_width - main_width) // 2
        main_y = (screen_height - main_height) // 2
        main_rect = pygame.Rect(main_x, main_y, main_width, main_height)

        pygame.draw.rect(screen, (245, 235, 220), main_rect, border_radius=15)
        pygame.draw.rect(screen, (180, 150, 100), main_rect, 3, border_radius=15)

        self.close_btn_rect = pygame.Rect(main_x + main_width - 40, main_y + 20, 30, 30)

        title = self.title_font.render("ФЕРМЕРСКИЙ МАГАЗИН", True, (90, 60, 30))
        screen.blit(title, (main_x + main_width // 2 - title.get_width() // 2, main_y + 35))

        mouse_pos = pygame.mouse.get_pos()
        close_hover = self.close_btn_rect.collidepoint(mouse_pos)
        close_color = (220, 90, 90) if close_hover else (200, 80, 80)
        pygame.draw.rect(screen, close_color, self.close_btn_rect, border_radius=15)
        pygame.draw.rect(screen, (150, 50, 50), self.close_btn_rect, 2, border_radius=15)
        close_text = self.item_font.render("×", True, (255, 255, 255))
        screen.blit(close_text, (self.close_btn_rect.x + 7, self.close_btn_rect.y))

        for i, item_data in enumerate(self.items):
            self._draw_item(screen, i, item_data, farmer_money, mouse_pos, main_x, main_y)

    def _draw_item(self, screen, index, item_data, farmer_money, mouse_pos, main_x, main_y):
        item = item_data["item"]
        rect_x = main_x + 20
        rect_y = main_y + 90 + index * 160
        rect = pygame.Rect(rect_x, rect_y, 480, 150)
        item_data["rect"] = rect

        is_available = item_data["quantity"] > 0
        can_afford = farmer_money >= item.price
        hover = rect.collidepoint(mouse_pos) and is_available

        # Фон
        bg_color = (255, 252, 240) if hover else (250, 248, 235)
        if not is_available:
            bg_color = (230, 230, 230)
        elif not can_afford:
            bg_color = (240, 220, 220)

        pygame.draw.rect(screen, bg_color, rect, border_radius=12)
        pygame.draw.rect(screen, (200, 180, 160), rect, 2, border_radius=12)

        card_image = None
        if isinstance(item, Plant):
            card_image = item_data["card_image"]
        elif isinstance(item, Animal):
            card_image = item.image
        icon_rect = pygame.Rect(rect.x + 15, rect.y + 15, 50, 50)
        pygame.draw.rect(screen, (230, 220, 200), icon_rect, border_radius=8)
        pygame.draw.rect(screen, (190, 170, 140), icon_rect, 2, border_radius=8)
        screen.blit(pygame.transform.scale(card_image, (40, 40)), (rect.x + 20, rect.y + 20))

        text_x = rect.x + 80
        text_y = rect.y + 15

        name_text = self.item_font.render(item.name, True, (70, 50, 30))
        screen.blit(name_text, (text_x, text_y))

        price_color = (0, 150, 70) if can_afford else (200, 70, 50)
        price_text = self.price_font.render(f"{item.price}", True, price_color)
        screen.blit(price_text, (text_x, text_y + 30))

        avail_text = self.price_font.render(
            f"✓ В наличии ({item_data['quantity']})" if is_available else "✗ Нет в наличии",
            True,
            (0, 130, 0) if is_available else (150, 0, 0)
        )
        screen.blit(avail_text, (text_x, text_y + 55))

        desc_lines = self._wrap_text(item_data['description'], self.desc_font, 340)
        for i, line in enumerate(desc_lines[:2]):
            screen.blit(
                self.desc_font.render(line, True, (90, 80, 70)),
                (text_x, text_y + 80 + i * 20)
            )

        if hover:
            buy_rect = pygame.Rect(rect.x + rect.width - 110, rect.y + rect.height - 35, 100, 30)
            pygame.draw.rect(screen, (100, 180, 100), buy_rect, border_radius=15)
            pygame.draw.rect(screen, (50, 120, 50), buy_rect, 2, border_radius=15)
            buy_text = pygame.font.Font(None, 24).render("КУПИТЬ", True, (255, 255, 255))
            screen.blit(buy_text, (buy_rect.x + 17, buy_rect.y + 7))

        if item_data.get("waiting_update"):
            overlay = pygame.Surface((480, 150), pygame.SRCALPHA)
            overlay.fill((50, 50, 50, 180))
            screen.blit(overlay, (rect.x, rect.y))
            msg = self.item_font.render("Скоро обновится!", True, (255, 255, 255))
            screen.blit(msg, (rect.x + 120, rect.y + 55))

    def handle_click(self, pos, farmer, game_map):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_click_time < 300:
            return None
        self.last_click_time = current_time

        if self.close_btn_rect.collidepoint(pos):
            return False

        for item_data in self.items:
            if item_data.get('rect') and item_data['rect'].collidepoint(pos):
                item = item_data['item']
                if farmer.money < item.price:
                    return "Недостаточно денег"

                item_type = item_data["type"]
                item_data['quantity'] -= 1

                if item_data['quantity'] <= 0 and item_data.get("key") == "potato_stage":
                    item_data['waiting_update'] = True
                    self.transition_start_day = self.time_manager.day
                elif item_data['quantity'] <= 0 and item_data.get("key") == 'carrot_stage':
                    item_data['waiting_update'] = True
                    self.transition_start_day = self.time_manager.day

                if item_type == "plant":
                    sprite_key = item_data["key"].replace("_stage", "")
                    sprite_set = self.images[sprite_key]
                    max_per_row = 5
                    row = len(farmer.plants) // max_per_row
                    col = len(farmer.plants) % max_per_row

                    x = 280 + col * 70
                    y = 400 + row * 70

                    new_plant = Plant(
                        name=item.name,
                        growth_time=item.growth_time,
                        price=item.price,
                        sell_price=item.sell_price,
                        images_dict=sprite_set,
                        x=x,
                        y=y
                    )

                    farmer.money -= item.price
                    farmer.add_item(new_plant, game_map)
                    return f"{item.name} посажена!"

                elif item_type == "animal":
                    new_animal = Animal(
                        name=item.name,
                        price=item.price,
                        product=item.product,
                        product_price=item.product_price,
                        image=item.image,
                        x=100,
                        y=100
                    )

                    farmer.money -= item.price
                    farmer.add_item(new_animal, game_map)
                    return f"{item.name} куплен(a)!"

    def _update_store_logic(self):
        for item_data in self.items:
            if item_data.get("key") == "potato_stage" and item_data.get("waiting_update"):
                days_passed = self.time_manager.day - self.transition_start_day
                if item_data["stage"] == "potato" and days_passed >= 3:
                    item_data.update({
                        "item": Plant(
                            "Морковь",
                            4,
                            80,
                            150,
                            self.images["carrot"],
                            0,
                            0
                        ),
                        "card_image": self.images["carrot_card"],
                        "quantity": 5,
                        "description": "Созревает за 4 дня. Продается за 150. Требует полива.",
                        "stage": "carrot",
                        "key": "carrot_stage",
                        "waiting_update": False
                    })
            elif item_data.get("key") == "carrot_stage" and item_data.get("waiting_update"):
                days_passed = self.time_manager.day - self.transition_start_day
                if item_data["stage"] == "carrot" and days_passed >= 4:
                    item_data.update({
                    "item": Plant(
                        "Лук",
                        5,
                        120,
                        300,
                        self.images["onion"],
                        0,
                        0
                    ),
                    "card_image": self.images["onion_card"],
                    "quantity": 5,
                    "description": "Созревает за 5 дней. Продается за 300. Требует полива.",
                    "stage": "onion",
                    "key": "onion_stage",
                    "waiting_update": False
                })

    def _create_new_item(self, item, item_type):
        if item_type == "plant":
            return Plant(item.name, item.growth_time, item.price, item.sell_price, item.image, 0, 0)
        else:
            return Animal(item.name, item.price, item.product, item.product_price, item.image, 0, 0)