import math
from src.utils.constants import GRAVITY, FRICTION

class PhysicsSystem:
    """Система фізики для ігрових об'єктів"""
    
    def __init__(self, collision_system):
        """Ініціалізація системи фізики"""
        self.collision_system = collision_system
        self.gravity_enabled = False  # Увімкнення/вимкнення гравітації
    
    def update(self, entity, delta_time):
        """Оновлення фізики для сутності"""
        # Застосування гравітації, якщо вона ввімкнена
        if self.gravity_enabled and hasattr(entity, 'velocity_y'):
            entity.velocity_y += GRAVITY * delta_time
        
        # Застосування тертя
        if hasattr(entity, 'velocity_x') and hasattr(entity, 'velocity_y'):
            entity.velocity_x *= (1 - FRICTION * delta_time)
            entity.velocity_y *= (1 - FRICTION * delta_time)
            
            # Зупинка об'єкта, якщо швидкість дуже мала
            if abs(entity.velocity_x) < 0.1:
                entity.velocity_x = 0
            if abs(entity.velocity_y) < 0.1:
                entity.velocity_y = 0
            
            # Обмеження максимальної швидкості
            max_speed = getattr(entity, 'max_speed', 500)
            speed = math.sqrt(entity.velocity_x**2 + entity.velocity_y**2)
            if speed > max_speed:
                scale = max_speed / speed
                entity.velocity_x *= scale
                entity.velocity_y *= scale
        
        # Рух об'єкта з урахуванням зіткнень
        if hasattr(entity, 'velocity_x') and hasattr(entity, 'velocity_y'):
            # Обчислення нового положення
            new_x = entity.x + entity.velocity_x * delta_time
            new_y = entity.y + entity.velocity_y * delta_time
            
            # Перевірка і розв'язання зіткнень
            entity.x, entity.y = self.collision_system.resolve_movement(entity, 
                                                                       entity.velocity_x * delta_time, 
                                                                       entity.velocity_y * delta_time)
            
            # Якщо об'єкт стикнувся з перешкодою, скидаємо відповідну компоненту швидкості
            if entity.x != new_x:
                entity.velocity_x = 0
            if entity.y != new_y:
                entity.velocity_y = 0