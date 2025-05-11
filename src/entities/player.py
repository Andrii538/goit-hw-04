import pygame
import math
from src.utils.constants import PLAYER_SPEED, PLAYER_HEALTH, PLAYER_ATTACK_RATE

class Player:
    """Клас гравця"""
    
    def __init__(self, x, y):
        """Ініціалізація гравця"""
        self.x = x
        self.y = y
        self.width = 32  # Ширина спрайту
        self.height = 32  # Висота спрайту
        self.direction = 0  # Кут напрямку (в радіанах)
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.attack_rate = PLAYER_ATTACK_RATE
        self.attack_cooldown = 0
        self.is_attacking = False
        self.weapons = []
        self.current_weapon = None
        self.collision_system = None
        self.animation_state = "idle"  # Стан анімації
        self.animation_frame = 0  # Кадр анімації
    
    def set_collision_system(self, collision_system):
        """Встановлення системи зіткнень"""
        self.collision_system = collision_system
        collision_system.register_entity(self)
    
    def handle_input(self, input_handler):
        """Обробка введення користувача"""
        # Рух гравця
        move_x = 0
        move_y = 0
        
        if input_handler.is_key_pressed("up"):
            move_y -= 1
        if input_handler.is_key_pressed("down"):
            move_y += 1
        if input_handler.is_key_pressed("left"):
            move_x -= 1
        if input_handler.is_key_pressed("right"):
            move_x += 1
        
        # Нормалізація вектора руху для однакової швидкості по діагоналі
        if move_x != 0 or move_y != 0:
            length = math.sqrt(move_x * move_x + move_y * move_y)
            move_x /= length
            move_y /= length
            self.animation_state = "run"
        else:
            self.animation_state = "idle"
        
        # Застосування швидкості
        if self.collision_system:
            self.collision_system.resolve_movement(self, move_x * self.speed, move_y * self.speed)
        else:
            self.x += move_x * self.speed
            self.y += move_y * self.speed
        
        # Обертання відповідно до положення миші
        mouse_pos = input_handler.get_mouse_position()
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        self.direction = math.atan2(dy, dx)
        
        # Стрільба
        if input_handler.is_mouse_button_pressed(0):  # ЛКМ
            self.attack()
    
    def attack(self):
        """Атака гравця"""
        if self.attack_cooldown <= 0 and self.current_weapon:
            self.is_attacking = True
            self.current_weapon.fire()
            self.attack_cooldown = self.attack_rate
    
    def update(self, delta_time):
        """Оновлення стану гравця"""
        # Оновлення кулдауна атаки
        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time
        
        # Оновлення анімації
        self.animation_frame += delta_time * 10  # 10 FPS для анімації
        self.animation_frame %= 4  # Припускаємо 4 кадри анімації
    
    def take_damage(self, amount):
        """Отримання шкоди"""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.die()
    
    def heal(self, amount):
        """Лікування"""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
    
    def die(self):
        """Смерть гравця"""
        # TODO: Реалізувати логіку смерті
        print("Гравець загинув!")
    
    def render(self, surface, renderer, position=None):
        """Рендеринг гравця"""
        if position is None:
            position = (self.x, self.y)
        
        # Вибір текстури відповідно до стану анімації
        texture_name = f"player_{self.animation_state}_{int(self.animation_frame)}"
        
        # Відображення гравця з поворотом відповідно до напрямку
        renderer.draw_texture(surface, texture_name, position, rotation=-math.degrees(self.direction))
        
        # Відображення зброї
        if self.current_weapon:
            self.current_weapon.render(surface, renderer, position, self.direction)
    
    def on_collision(self, other):
        """Обробка зіткнень з іншими об'єктами"""
        from src.entities.item import Item
        if isinstance(other, Item):
            other.pickup(self)