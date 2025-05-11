import pygame
import math
import random
from src.utils.constants import ENEMY_HEALTH, ENEMY_SPEED, ENEMY_DAMAGE, ENEMY_ATTACK_RATE

class Enemy:
    """Клас ворога"""
    
    def __init__(self, x, y, enemy_type="basic"):
        """Ініціалізація ворога"""
        self.x = x
        self.y = y
        self.width = 32  # Ширина спрайту
        self.height = 32  # Висота спрайту
        self.type = enemy_type
        self.direction = 0  # Кут напрямку (в радіанах)
        
        # Характеристики відповідно до типу
        if enemy_type == "basic":
            self.health = ENEMY_HEALTH
            self.speed = ENEMY_SPEED
            self.damage = ENEMY_DAMAGE
            self.attack_range = 50
            self.attack_rate = ENEMY_ATTACK_RATE
        elif enemy_type == "fast":
            self.health = ENEMY_HEALTH * 0.7
            self.speed = ENEMY_SPEED * 1.5
            self.damage = ENEMY_DAMAGE * 0.8
            self.attack_range = 40
            self.attack_rate = ENEMY_ATTACK_RATE * 0.7
        elif enemy_type == "heavy":
            self.health = ENEMY_HEALTH * 2
            self.speed = ENEMY_SPEED * 0.7
            self.damage = ENEMY_DAMAGE * 1.5
            self.attack_range = 60
            self.attack_rate = ENEMY_ATTACK_RATE * 1.3
        else:
            # За замовчуванням - базовий ворог
            self.health = ENEMY_HEALTH
            self.speed = ENEMY_SPEED
            self.damage = ENEMY_DAMAGE
            self.attack_range = 50
            self.attack_rate = ENEMY_ATTACK_RATE
        
        self.max_health = self.health
        self.state = "idle"  # Початковий стан
        self.ai_system = None
        self.collision_system = None
        
        # Патрулювання
        self.patrol_points = []
        self.current_patrol_point = 0
        self.generate_patrol_points()
        
        # Таймери для різних станів
        self.idle_time = 0
        self.idle_duration = random.uniform(1.0, 3.0)
        self.attack_cooldown = 0
        self.hurt_time = 0
        self.death_time = 2.0  # Час анімації смерті
        
        # Для AI
        self.last_seen_player_pos = None
        self.should_remove = False
        
        # Анімація
        self.animation_frame = 0
    
    def generate_patrol_points(self):
        """Генерація точок патрулювання"""
        # В реальній грі це може бути визначено в даних рівня
        # Тут ми просто створюємо кілька точок навколо початкової позиції
        radius = random.uniform(50, 150)
        num_points = random.randint(2, 5)
        
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            px = self.x + radius * math.cos(angle)
            py = self.y + radius * math.sin(angle)
            self.patrol_points.append((px, py))
    
    def set_ai_system(self, ai_system):
        """Встановлення системи AI"""
        self.ai_system = ai_system
    
    def set_collision_system(self, collision_system):
        """Встановлення системи зіткнень"""
        self.collision_system = collision_system
        collision_system.register_entity(self)
    
    def take_damage(self, amount):
        """Отримання шкоди"""
        self.health -= amount
        if self.health <= 0:
            self.die()
        else:
            # Перехід до стану отримання шкоди
            self.state = "hurt"
            self.hurt_time = 0.3  # 300 мс стану отримання шкоди
    
    def die(self):
        """Смерть ворога"""
        self.state = "dead"
        self.health = 0
        # Якщо є система зіткнень, відключаємо зіткнення
        if self.collision_system:
            self.collision_system.unregister_entity(self)
    
    def update(self, delta_time):
        """Оновлення стану ворога"""
        # Оновлення анімації
        self.animation_frame += delta_time * 8
        self.animation_frame %= 4  # Припускаємо 4 кадри анімації
    
    def render(self, surface, renderer, position=None):
        """Рендеринг ворога"""
        if position is None:
            position = (self.x, self.y)
        
        # Вибір текстури відповідно до типу і стану
        texture_name = f"enemy_{self.type}_{self.state}_{int(self.animation_frame)}"
        
        # Відображення ворога з поворотом відповідно до напрямку
        renderer.draw_texture(surface, texture_name, position, rotation=-math.degrees(self.direction))
        
        # Відображення шкали здоров'я
        health_width = 30 * (self.health / self.max_health)
        pygame.draw.rect(surface, (255, 0, 0), (position[0] - 15, position[1] - 20, 30, 5))
        pygame.draw.rect(surface, (0, 255, 0), (position[0] - 15, position[1] - 20, health_width, 5))
    
    def on_collision(self, other):
        """Обробка зіткнень з іншими об'єктами"""
        from src.entities.player import Player
        # Реакція на зіткнення з гравцем
        if isinstance(other, Player) and self.state != "dead":
            # Можна додати додаткову логіку при контакті з гравцем
            pass