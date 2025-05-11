import pygame
from src.utils.constants import TILE_SIZE

class CollisionSystem:
    """Система для обробки зіткнень між об'єктами"""
    
    def __init__(self, map_data):
        """Ініціалізація системи зіткнень"""
        self.map_data = map_data
        self.collision_map = self._generate_collision_map()
        self.entities = []  # Список всіх сутностей для перевірки зіткнень
    
    def _generate_collision_map(self):
        """Генерація карти зіткнень на основі даних карти"""
        collision_map = []
        
        # Якщо в даних карти є спеціальне поле для зіткнень
        if "collision_layer" in self.map_data:
            return self.map_data["collision_layer"]
        
        # Інакше генеруємо з основної карти (припускаємо, що тайли > 0 є перешкодами)
        if "tiles" in self.map_data:
            for row in self.map_data["tiles"]:
                collision_row = []
                for tile in row:
                    # Тут логіка визначення, чи є тайл перешкодою
                    # Наприклад, якщо tile_id > 0, це стіна
                    is_wall = tile > 0
                    collision_row.append(1 if is_wall else 0)
                collision_map.append(collision_row)
        
        return collision_map
    
    def register_entity(self, entity):
        """Реєстрація сутності для перевірки зіткнень"""
        if entity not in self.entities:
            self.entities.append(entity)
    
    def unregister_entity(self, entity):
        """Видалення сутності з перевірки зіткнень"""
        if entity in self.entities:
            self.entities.remove(entity)
    
    def check_tile_collision(self, x, y, width, height):
        """Перевірка зіткнень з тайлами карти"""
        # Конвертація координат світу в координати тайлів
        tile_x1 = int(x // TILE_SIZE)
        tile_y1 = int(y // TILE_SIZE)
        tile_x2 = int((x + width) // TILE_SIZE)
        tile_y2 = int((y + height) // TILE_SIZE)
        
        # Перевірка меж карти
        if (tile_x1 < 0 or tile_y1 < 0 or 
            tile_x2 >= len(self.collision_map[0]) if self.collision_map else 0 or 
            tile_y2 >= len(self.collision_map) if self.collision_map else 0):
            return True  # За межами карти вважаємо зіткненням
        
        # Перевірка зіткнень з тайлами
        for ty in range(tile_y1, tile_y2 + 1):
            for tx in range(tile_x1, tile_x2 + 1):
                if (ty < len(self.collision_map) and 
                    tx < len(self.collision_map[ty]) and 
                    self.collision_map[ty][tx] == 1):
                    return True
        
        return False
    
    def check_entity_collision(self, entity1, entity2):
        """Перевірка зіткнень між двома сутностями"""
        # Створення прямокутників для перевірки зіткнень
        rect1 = pygame.Rect(entity1.x, entity1.y, entity1.width, entity1.height)
        rect2 = pygame.Rect(entity2.x, entity2.y, entity2.width, entity2.height)
        
        # Перевірка перетину прямокутників
        return rect1.colliderect(rect2)
    
    def resolve_movement(self, entity, delta_x, delta_y):
        """Вирішення зіткнень при русі"""
        # Спочатку намагаємося рухатися по осі X
        new_x = entity.x + delta_x
        if not self.check_tile_collision(new_x, entity.y, entity.width, entity.height):
            entity.x = new_x
        
        # Потім намагаємося рухатися по осі Y
        new_y = entity.y + delta_y
        if not self.check_tile_collision(entity.x, new_y, entity.width, entity.height):
            entity.y = new_y
        
        # Перевірка зіткнень з іншими сутностями
        for other in self.entities:
            if other is not entity and self.check_entity_collision(entity, other):
                # Викликаємо обробник зіткнень в обох сутностях
                entity.on_collision(other)
                other.on_collision(entity)
        
        return entity.x, entity.y