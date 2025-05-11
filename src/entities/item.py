import pygame
import math

class Item:
    """Базовий клас для предметів, які можна підібрати"""
    
    def __init__(self, x, y, item_type="health"):
        """Ініціалізація предмета"""
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.type = item_type
        self.rotation = 0
        self.bob_offset = 0
        self.bob_speed = 2
        self.is_active = True
        self.collision_system = None
    
    def set_collision_system(self, collision_system):
        """Встановлення системи зіткнень"""
        self.collision_system = collision_system
        collision_system.register_entity(self)
    
    def update(self, delta_time):
        """Оновлення стану предмета"""
        if not self.is_active:
            return
        
        # Обертання предмета
        self.rotation += 90 * delta_time  # 90 градусів в секунду
        
        # Ефект "підскакування"
        self.bob_offset = 2 * math.sin(pygame.time.get_ticks() / 1000 * self.bob_speed)
    
    def pickup(self, player):
        """Підбір предмета гравцем"""
        if not self.is_active:
            return
        
        # Застосування ефекту предмета відповідно до типу
        if self.type == "health":
            player.heal(25)
        elif self.type == "ammo":
            if player.current_weapon:
                player.current_weapon.add_ammo(20)
        elif self.type == "weapon":
            # TODO: Додати логіку отримання нової зброї
            pass
        elif self.type == "armor":
            # TODO: Додати логіку бронювання
            pass
        
        # Деактивація предмета
        self.is_active = False
        if self.collision_system:
            self.collision_system.unregister_entity(self)
    
    def render(self, surface, renderer, position=None):
        """Рендеринг предмета"""
        if not self.is_active:
            return
        
        if position is None:
            position = (self.x, self.y)
        
        # Застосування ефекту "підскакування"
        position = (position[0], position[1] + self.bob_offset)
        
        # Вибір текстури відповідно до типу
        texture_name = f"item_{self.type}"
        
        # Відображення предмета з обертанням
        renderer.draw_texture(surface, texture_name, position, rotation=self.rotation)


class Weapon:
    """Клас зброї"""
    
    def __init__(self, weapon_type="pistol"):
        """Ініціалізація зброї"""
        self.type = weapon_type
        
        # Характеристики відповідно до типу зброї
        if weapon_type == "pistol":
            self.damage = 10
            self.fire_rate = 0.5  # Час між пострілами в секундах
            self.range = 500
            self.ammo = 30
            self.max_ammo = 100
        elif weapon_type == "shotgun":
            self.damage = 25
            self.fire_rate = 1.0
            self.range = 300
            self.ammo = 10
            self.max_ammo = 50
            self.pellets = 5  # Кількість куль в одному пострілі
        elif weapon_type == "rifle":
            self.damage = 15
            self.fire_rate = 0.2
            self.range = 700
            self.ammo = 50
            self.max_ammo = 200
        else:
            # За замовчуванням - пістолет
            self.damage = 10
            self.fire_rate = 0.5
            self.range = 500
            self.ammo = 30
            self.max_ammo = 100
        
        self.cooldown = 0
        self.owner = None  # Хто тримає зброю
    
    def set_owner(self, owner):
        """Встановлення власника зброї"""
        self.owner = owner
    
    def add_ammo(self, amount):
        """Додавання набоїв"""
        self.ammo += amount
        if self.ammo > self.max_ammo:
            self.ammo = self.max_ammo
    
    def fire(self):
        """Постріл зі зброї"""
        if self.ammo <= 0 or self.cooldown > 0:
            return False
        
        if self.type == "shotgun":
            # Дробовик стріляє кількома кулями
            for _ in range(self.pellets):
                # Додати розкид куль
                spread = random.uniform(-15, 15)
                self._create_bullet(spread)
        else:
            # Звичайна зброя
            self._create_bullet(0)
        
        # Зменшення кількості набоїв і встановлення кулдауна
        self.ammo -= 1
        self.cooldown = self.fire_rate
        
        # TODO: Додати звук пострілу
        
        return True
    
    def _create_bullet(self, angle_offset):
        """Створення кулі"""
        if self.owner:
            from src.entities.bullet import Bullet
            
            # Додавання зміщення до напрямку власника
            angle = self.owner.direction + math.radians(angle_offset)
            
            # Створення кулі перед власником
            start_x = self.owner.x + math.cos(angle) * 20
            start_y = self.owner.y + math.sin(angle) * 20
            
            # Додавання кулі до сцени
            bullet = Bullet(start_x, start_y, angle, self.damage, self.range, self.owner)
            
            # TODO: Додати кулю до ігрової сцени
    
    def update(self, delta_time):
        """Оновлення стану зброї"""
        # Зменшення кулдауна
        if self.cooldown > 0:
            self.cooldown -= delta_time
    
    def render(self, surface, renderer, position, direction):
        """Рендеринг зброї"""
        # Обчислення позиції відносно власника
        offset_x = math.cos(direction) * 15
        offset_y = math.sin(direction) * 15
        weapon_x = position[0] + offset_x
        weapon_y = position[1] + offset_y
        
        # Вибір текстури відповідно до типу
        texture_name = f"weapon_{self.type}"
        
        # Відображення зброї з поворотом відповідно до напрямку
        renderer.draw_texture(surface, texture_name, (weapon_x, weapon_y), rotation=-math.degrees(direction))