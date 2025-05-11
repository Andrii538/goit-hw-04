import pygame

class InputHandler:
    """Обробник введення користувача"""
    
    def __init__(self):
        """Ініціалізація обробника введення"""
        # Словник для зберігання стану кнопок
        self.keys_pressed = {}
        
        # Стан миші
        self.mouse_position = (0, 0)
        self.mouse_buttons = [False, False, False]  # ЛКМ, Колесо, ПКМ
        
        # Мапа клавіш для зручного доступу
        self.key_map = {
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d,
            "shoot": pygame.K_SPACE,
            "reload": pygame.K_r,
            "use": pygame.K_e,
            "sprint": pygame.K_LSHIFT,
            "pause": pygame.K_ESCAPE
        }
    
    def update(self, events):
        """Оновлення стану введення"""
        # Оновлення стану клавіш
        self.keys_pressed = pygame.key.get_pressed()
        
        # Оновлення стану миші
        self.mouse_position = pygame.mouse.get_pos()
        self.mouse_buttons = pygame.mouse.get_pressed()
        
        # Додаткова обробка подій, якщо потрібно
        for event in events:
            pass  # Тут можна додати специфічну обробку (напр. одиночні натискання)
    
    def is_key_pressed(self, key_name):
        """Перевірка, чи натиснута певна клавіша"""
        if key_name in self.key_map:
            return self.keys_pressed[self.key_map[key_name]]
        return False
    
    def is_mouse_button_pressed(self, button_index):
        """Перевірка, чи натиснута кнопка миші"""
        if 0 <= button_index < 3:
            return self.mouse_buttons[button_index]
        return False
    
    def get_mouse_position(self):
        """Отримання позиції курсора миші"""
        return self.mouse_position