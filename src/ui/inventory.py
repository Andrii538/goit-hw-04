# import pygame
# from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

# class Inventory:
#     """Інвентар гравця"""
    
#     def __init__(self, player):
#         """Ініціалізація інвентаря"""
#         self.player = player
#         self.is_open = False
#         self.selected_slot = 0
#         self.slots = 6  # Кількість слотів для зброї/предметів
    
#     def toggle(self):
#         """Відкриття/закриття інвентаря"""
#         self.is_open = not self.is_open
    
#     def next_weapon(self):
#         """Вибір наступної зброї"""
#         if not self.player.weapons:
#             return
        
#         self.selected_slot = (self.selected_slot + 1) % len(self.player.weapons)
#         self.player.current_weapon = self.player.weapons[self.selected_slot]
    
#     def prev_weapon(self):
#         """Вибір попередньої зброї"""
#         if not self.player.weapons:
#             return
        
#         self.selected_slot = (self.selected_slot - 1) % len(self.player.weapons)
#         self.player.current_weapon = self.player.weapons[self.selected_slot]
    
#     def render(self, surface, renderer):
#         """Рендеринг інвентаря"""
#         # Якщо інвентар закритий, показуємо тільки панель швидкого доступу
#         if not self.is_open:
#             self._render_quickbar(surface, renderer)
#             return
        
#         # Повний інвентар
#         self._render_full_inventory(surface, renderer)
    
#     def _render_quickbar(self, surface, renderer):
#         """Відображення панелі швидкого доступу"""
#         slot_size = 50
#         slot_spacing = 10
#         start_x = (SCREEN_WIDTH - (slot_size * self.slots + slot_spacing * (self.slots - 1))) // 2
#         y = SCREEN_HEIGHT - slot_size - 10
        
#         for i in range(self.slots):
#             x = start_x + i * (slot_size + slot_spacing)
            
#             # Фон слота
#             bg_color = (70, 70, 70)
#             if i == self.selected_slot and self.player.weapons and i < len(self.player.weapons):
#                 bg_color = (120, 120, 120)  # Підсвічування обраного слота
            
#             pygame.draw.rect(surface, bg_color, (x, y, slot_size, slot_size))
#             pygame.draw.rect(surface, WHITE, (x, y, slot_size, slot_size), 2)
            
#             # Відображення зброї в слоті, якщо вона є
#             if self.player.weapons and i < len(self.player.weapons):
#                 weapon = self.player.weapons[i]
#                 weapon_icon = f"weapon_icon_{weapon.type}"
#                 renderer.draw_texture(surface, weapon_icon, (x + 5, y + 5), scale=0.8)
            
#             # Номер слота
#             slot_num = str(i + 1)
#             renderer.draw main.py


import pygame
from pygame.locals import *
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, INVENTORY_SLOTS
from src.utils.helpers import load_image


class Inventory:
    def __init__(self, player):
        """
        Ініціалізація інвентаря гравця
        
        Args:
            player: Об'єкт гравця, до якого прикріплений інвентар
        """
        self.player = player
        self.slots = [None] * INVENTORY_SLOTS
        self.active_slot = 0
        self.visible = False
        
        # Завантаження зображень і створення поверхонь для інвентаря
        self.background = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.background.fill(COLORS["dark_gray"])
        self.background.set_alpha(220)  # Напівпрозорість
        
        # Позиція інвентаря на екрані
        self.x = SCREEN_WIDTH // 4
        self.y = SCREEN_HEIGHT // 4
        
        # Створення слотів
        self.slot_width = 64
        self.slot_height = 64
        self.slot_spacing = 10
        
        # Завантаження зображень для предметів
        self.item_images = {
            "shotgun": load_image("textures/items/shotgun.png"),
            "pistol": load_image("textures/items/pistol.png"),
            "medkit": load_image("textures/items/medkit.png"),
            "ammo": load_image("textures/items/ammo.png"),
            "armor": load_image("textures/items/armor.png"),
        }
        
        # Звук перемикання слотів та використання предметів
        self.switch_sound = pygame.mixer.Sound("assets/sounds/inventory_switch.wav")
        self.use_sound = pygame.mixer.Sound("assets/sounds/item_use.wav")
    
    def add_item(self, item):
        """
        Додавання предмету в інвентар
        
        Args:
            item: Об'єкт предмету для додавання
            
        Returns:
            bool: True якщо предмет додано, False якщо інвентар повний
        """
        for i in range(INVENTORY_SLOTS):
            if self.slots[i] is None:
                self.slots[i] = item
                return True
                
        # Якщо предмет однаковий з існуючим, збільшуємо кількість
        for i in range(INVENTORY_SLOTS):
            if self.slots[i] and self.slots[i].name == item.name and self.slots[i].stackable:
                self.slots[i].quantity += item.quantity
                return True
                
        return False  # Інвентар повний
    
    def remove_item(self, slot_index):
        """
        Видалення предмету з інвентаря
        
        Args:
            slot_index: Індекс слота для видалення
        """
        if 0 <= slot_index < INVENTORY_SLOTS and self.slots[slot_index]:
            self.slots[slot_index] = None
    
    def use_item(self, slot_index=None):
        """
        Використання предмету з інвентаря
        
        Args:
            slot_index: Індекс слота (якщо None, використовується активний слот)
            
        Returns:
            bool: True якщо предмет використано, False якщо ні
        """
        if slot_index is None:
            slot_index = self.active_slot
            
        if 0 <= slot_index < INVENTORY_SLOTS and self.slots[slot_index]:
            item = self.slots[slot_index]
            
            # Застосування ефекту предмета
            result = item.use(self.player)
            
            if result:
                self.use_sound.play()
                
                # Видалення одноразових предметів після використання
                if item.consumable:
                    item.quantity -= 1
                    if item.quantity <= 0:
                        self.slots[slot_index] = None
                        
                return True
        
        return False
    
    def select_weapon(self, weapon_index):
        """
        Вибір зброї за індексом
        
        Args:
            weapon_index: Індекс зброї для вибору
        """
        for i, item in enumerate(self.slots):
            if item and item.type == "weapon" and item.weapon_index == weapon_index:
                self.active_slot = i
                self.switch_sound.play()
                self.player.current_weapon = item
                return True
        return False
    
    def next_slot(self):
        """Перехід до наступного слота"""
        self.active_slot = (self.active_slot + 1) % INVENTORY_SLOTS
        self.switch_sound.play()
    
    def prev_slot(self):
        """Перехід до попереднього слота"""
        self.active_slot = (self.active_slot - 1) % INVENTORY_SLOTS
        self.switch_sound.play()
    
    def toggle_visibility(self):
        """Перемикання видимості інвентаря"""
        self.visible = not self.visible
        
    def handle_event(self, event):
        """
        Обробка подій для інвентаря
        
        Args:
            event: Подія Pygame
        """
        if not self.visible:
            return
            
        # Використання предмету на клік миші
        if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Лівий клік
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Перевірка клацання по слоту
            for i in range(INVENTORY_SLOTS):
                slot_x = self.x + (i % 5) * (self.slot_width + self.slot_spacing)
                slot_y = self.y + (i // 5) * (self.slot_height + self.slot_spacing)
                
                slot_rect = pygame.Rect(slot_x, slot_y, self.slot_width, self.slot_height)
                if slot_rect.collidepoint(mouse_x, mouse_y):
                    self.active_slot = i
                    # Подвійний клік для використання
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        self.use_item(i)
        
        # Гарячі клавіші для інвентаря
        elif event.type == KEYDOWN:
            if event.key == K_1:
                self.select_weapon(0)
            elif event.key == K_2:
                self.select_weapon(1)
            elif event.key == K_3:
                self.select_weapon(2)
            elif event.key == K_4:
                self.select_weapon(3)
            elif event.key == K_q:
                self.prev_slot()
            elif event.key == K_e:
                self.next_slot()
            elif event.key == K_SPACE:
                self.use_item()
                
    def update(self):
        """Оновлення стану інвентаря"""
        pass  # Додаткова логіка оновлення, якщо потрібно
    
    def draw(self, surface):
        """
        Відображення інвентаря на екрані
        
        Args:
            surface: Поверхня Pygame для відображення
        """
        # Відображення миттєвого індикатора вибраної зброї (навіть коли інвентар не видимий)
        active_item = self.slots[self.active_slot]
        if active_item and active_item.type == "weapon":
            # Відображення поточної зброї у куті екрану
            item_icon = self.item_images.get(active_item.name)
            if item_icon:
                surface.blit(item_icon, (20, SCREEN_HEIGHT - 80))
                
            # Відображення поточного боєзапасу
            ammo_text = f"{active_item.current_ammo}/{active_item.max_ammo}"
            font = pygame.font.Font(None, 24)
            text_surface = font.render(ammo_text, True, COLORS["white"])
            surface.blit(text_surface, (80, SCREEN_HEIGHT - 70))
        
        # Якщо інвентар не видимий, не малюємо його
        if not self.visible:
            return
            
        # Малюємо фон інвентаря
        surface.blit(self.background, (self.x, self.y))
        
        # Заголовок інвентаря
        font = pygame.font.Font(None, 32)
        title = font.render("ІНВЕНТАР", True, COLORS["white"])
        surface.blit(title, (self.x + 20, self.y + 10))
        
        # Малюємо слоти інвентаря
        for i in range(INVENTORY_SLOTS):
            slot_x = self.x + 20 + (i % 5) * (self.slot_width + self.slot_spacing)
            slot_y = self.y + 50 + (i // 5) * (self.slot_height + self.slot_spacing)
            
            # Малюємо фон слота
            slot_color = COLORS["light_gray"]
            if i == self.active_slot:
                slot_color = COLORS["highlight"]
                
            pygame.draw.rect(surface, slot_color, 
                            (slot_x, slot_y, self.slot_width, self.slot_height))
            pygame.draw.rect(surface, COLORS["black"], 
                            (slot_x, slot_y, self.slot_width, self.slot_height), 2)
            
            # Якщо в слоті є предмет, малюємо його
            if self.slots[i]:
                item = self.slots[i]
                item_icon = self.item_images.get(item.name)
                
                if item_icon:
                    # Масштабування зображення, якщо потрібно
                    scaled_icon = pygame.transform.scale(
                        item_icon, (self.slot_width - 8, self.slot_height - 8))
                    surface.blit(scaled_icon, (slot_x + 4, slot_y + 4))
                
                # Відображаємо кількість, якщо більше одиниці
                if item.quantity > 1:
                    quantity_font = pygame.font.Font(None, 20)
                    quantity_text = quantity_font.render(str(item.quantity), True, COLORS["white"])
                    surface.blit(quantity_text, (slot_x + self.slot_width - 15, 
                                               slot_y + self.slot_height - 15))
            
            # Відображення номера слота (для гарячих клавіш)
            slot_num_font = pygame.font.Font(None, 18)
            slot_num = slot_num_font.render(str(i + 1), True, COLORS["dark_gray"])
            surface.blit(slot_num, (slot_x + 5, slot_y + 5))
        
        # Якщо є активний предмет, відображаємо додаткову інформацію про нього
        if self.slots[self.active_slot]:
            item = self.slots[self.active_slot]
            info_x = self.x + 20
            info_y = self.y + 50 + ((INVENTORY_SLOTS // 5) + 1) * (self.slot_height + self.slot_spacing)
            
            # Назва предмета
            item_font = pygame.font.Font(None, 28)
            item_name = item_font.render(item.display_name, True, COLORS["white"])
            surface.blit(item_name, (info_x, info_y))
            
            # Опис предмета
            desc_font = pygame.font.Font(None, 20)
            desc_text = desc_font.render(item.description, True, COLORS["light_gray"])
            surface.blit(desc_text, (info_x, info_y + 30))
            
            # Додаткова інформація про зброю
            if item.type == "weapon":
                ammo_text = f"Боєзапас: {item.current_ammo}/{item.max_ammo}"
                damage_text = f"Пошкодження: {item.damage}"
                
                ammo_surf = desc_font.render(ammo_text, True, COLORS["light_gray"])
                damage_surf = desc_font.render(damage_text, True, COLORS["light_gray"])
                
                surface.blit(ammo_surf, (info_x, info_y + 50))
                surface.blit(damage_surf, (info_x, info_y + 70))


class Item:
    """Базовий клас для ігрових предметів"""
    def __init__(self, name, item_type, quantity=1):
        self.name = name
        self.display_name = name.capitalize()
        self.type = item_type
        self.quantity = quantity
        self.consumable = False
        self.stackable = False
        self.description = "Предмет без опису"
        
    def use(self, player):
        """
        Використання предмету
        
        Args:
            player: Об'єкт гравця
            
        Returns:
            bool: True якщо предмет використано, False якщо ні
        """
        return False  # Базовий предмет не має дії


class Weapon(Item):
    """Клас для зброї"""
    def __init__(self, name, damage, max_ammo, current_ammo=None, weapon_index=0):
        super().__init__(name, "weapon")
        self.damage = damage
        self.max_ammo = max_ammo
        self.current_ammo = max_ammo if current_ammo is None else current_ammo
        self.weapon_index = weapon_index
        self.stackable = False
        self.consumable = False
        
        # Налаштування зброї
        if name == "pistol":
            self.display_name = "Пістолет"
            self.description = "Стандартна зброя. Невелика шкода, необмежений боєзапас."
            self.fire_rate = 0.5  # Швидкість стрільби (секунди між пострілами)
            self.reload_time = 1.0
            self.fire_sound = "assets/sounds/pistol_fire.wav"
        elif name == "shotgun":
            self.display_name = "Дробовик"
            self.description = "Потужна зброя ближнього бою."
            self.fire_rate = 0.8
            self.reload_time = 1.5
            self.fire_sound = "assets/sounds/shotgun_fire.wav"
        
    def use(self, player):
        """
        Використання зброї (постріл)
        
        Args:
            player: Об'єкт гравця
            
        Returns:
            bool: True якщо відбувся постріл, False якщо немає боєприпасів
        """
        # Перевірка на наявність патронів (для пістолета завжди дозволено)
        if self.name == "pistol" or self.current_ammo > 0:
            if self.name != "pistol":  # Зменшуємо патрони для всіх видів зброї крім пістолета
                self.current_ammo -= 1
            
            # Логіка пострілу буде в основному коді гравця
            return True
        return False
        
    def reload(self, ammo_count=None):
        """
        Перезарядка зброї
        
        Args:
            ammo_count: Кількість патронів для додавання (якщо None, то до максимуму)
            
        Returns:
            bool: True якщо перезарядка успішна, False якщо уже максимум
        """
        if ammo_count is None:
            if self.current_ammo < self.max_ammo:
                self.current_ammo = self.max_ammo
                return True
        else:
            if self.current_ammo < self.max_ammo:
                self.current_ammo = min(self.current_ammo + ammo_count, self.max_ammo)
                return True
        return False


class Consumable(Item):
    """Клас для витратних предметів"""
    def __init__(self, name, effect_value=0, quantity=1):
        super().__init__(name, "consumable", quantity)
        self.effect_value = effect_value
        self.consumable = True
        self.stackable = True
        
        # Налаштування різних типів предметів
        if name == "medkit":
            self.display_name = "Аптечка"
            self.description = f"Відновлює {effect_value} одиниць здоров'я."
        elif name == "ammo":
            self.display_name = "Боєприпаси"
            self.description = f"Додає {effect_value} патронів."
        elif name == "armor":
            self.display_name = "Броня"
            self.description = f"Додає {effect_value} одиниць броні."
    
    def use(self, player):
        """
        Використання витратного предмета
        
        Args:
            player: Об'єкт гравця
            
        Returns:
            bool: True якщо предмет використано, False якщо ні
        """
        if self.name == "medkit":
            if player.health < player.max_health:
                player.health = min(player.health + self.effect_value, player.max_health)
                return True
        elif self.name == "ammo":
            # Додавання патронів до активної зброї
            if player.current_weapon and player.current_weapon.current_ammo < player.current_weapon.max_ammo:
                player.current_weapon.reload(self.effect_value)
                return True
        elif self.name == "armor":
            if player.armor < player.max_armor:
                player.armor = min(player.armor + self.effect_value, player.max_armor)
                return True
        
        return False