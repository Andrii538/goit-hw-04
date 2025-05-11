import math
import random
from src.utils.constants import ENEMY_VIEW_DISTANCE

class AISystem:
    """Система штучного інтелекту для ворогів"""
    
    def __init__(self):
        """Ініціалізація системи AI"""
        self.patrolling_enemies = []  # Вороги в режимі патрулювання
        self.chasing_enemies = []     # Вороги, що переслідують гравця
        self.attacking_enemies = []   # Вороги, що атакують гравця
        
        # Різні стани ворогів
        self.states = {
            "idle": self._update_idle,
            "patrol": self._update_patrol,
            "chase": self._update_chase,
            "attack": self._update_attack,
            "hurt": self._update_hurt,
            "dead": self._update_dead
        }
    
    def update(self, player, enemies, delta_time):
        """Оновлення AI всіх ворогів"""
        for enemy in enemies:
            if enemy.state == "dead":
                # Пропускаємо мертвих ворогів
                continue
            
            # Перевірка, чи бачить ворог гравця
            can_see_player = self._can_see_player(enemy, player)
            
            # Оновлення стану ворога на основі видимості гравця
            if enemy.state != "hurt" and enemy.state != "attack":
                if can_see_player:
                    distance_to_player = self._calculate_distance(enemy, player)
                    if distance_to_player < enemy.attack_range:
                        enemy.state = "attack"
                    else:
                        enemy.state = "chase"
                elif enemy.state == "chase":
                    # Якщо втратив гравця з виду, повертається до патрулювання
                    enemy.last_seen_player_pos = (player.x, player.y)
                    enemy.state = "patrol"
            
            # Оновлення поведінки відповідно до стану
            if enemy.state in self.states:
                self.states[enemy.state](enemy, player, delta_time)
    
    def _can_see_player(self, enemy, player):
        """Перевірка, чи бачить ворог гравця"""
        # Перевірка відстані
        distance = self._calculate_distance(enemy, player)
        if distance > ENEMY_VIEW_DISTANCE:
            return False
        
        # TODO: Додати перевірку прямої видимості (ray casting)
        # Це спрощена версія, яка перевіряє тільки відстань
        return True
    
    def _calculate_distance(self, entity1, entity2):
        """Розрахунок відстані між двома сутностями"""
        dx = entity1.x - entity2.x
        dy = entity1.y - entity2.y
        return math.sqrt(dx * dx + dy * dy)
    
    def _update_idle(self, enemy, player, delta_time):
        """Оновлення ворога в стані спокою"""
        # Періодично перемикатися на патрулювання
        enemy.idle_time += delta_time
        if enemy.idle_time > enemy.idle_duration:
            enemy.idle_time = 0
            enemy.state = "patrol"
    
    def _update_patrol(self, enemy, player, delta_time):
        """Оновлення ворога в стані патрулювання"""
        # Якщо немає точок патрулювання, то стоїмо на місці
        if not enemy.patrol_points:
            enemy.state = "idle"
            return
        
        # Рух до поточної точки патрулювання
        target_x, target_y = enemy.patrol_points[enemy.current_patrol_point]
        dx = target_x - enemy.x
        dy = target_y - enemy.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Якщо досягли точки, вибираємо наступну
        if distance < 5:  # Tolerance
            enemy.current_patrol_point = (enemy.current_patrol_point + 1) % len(enemy.patrol_points)
            enemy.idle_time = 0
            enemy.state = "idle"
            return
        
        # Рух до точки
        speed = enemy.speed * delta_time
        if distance > 0:
            enemy.x += (dx / distance) * speed
            enemy.y += (dy / distance) * speed
        
        # Встановлюємо напрямок погляду
        enemy.direction = math.atan2(dy, dx)
    
    def _update_chase(self, enemy, player, delta_time):
        """Оновлення ворога в стані переслідування"""
        # Розрахунок напрямку до гравця
        dx = player.x - enemy.x
        dy = player.y - enemy.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Рух до гравця
        if distance > enemy.attack_range:
            speed = enemy.speed * delta_time
            if distance > 0:
                enemy.x += (dx / distance) * speed
                enemy.y += (dy / distance) * speed
        else:
            enemy.state = "attack"
        
        # Встановлюємо напрямок погляду
        enemy.direction = math.atan2(dy, dx)
    
    def _update_attack(self, enemy, player, delta_time):
        """Оновлення ворога в стані атаки"""
        # Повертаємося до гравця
        dx = player.x - enemy.x
        dy = player.y - enemy.y
        enemy.direction = math.atan2(dy, dx)
        
        # Перевірка, чи можна атакувати
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > enemy.attack_range:
            enemy.state = "chase"
            return
        # Атака з певним кулдауном
        enemy.attack_cooldown -= delta_time
        if enemy.attack_cooldown <= 0:
            # Завдання шкоди гравцю
            player.take_damage(enemy.damage)
            # Скидання кулдауна
            enemy.attack_cooldown = enemy.attack_rate
    
    def _update_hurt(self, enemy, player, delta_time):
        """Оновлення ворога в стані отримання шкоди"""
        # Зменшення часу стану отримання шкоди
        enemy.hurt_time -= delta_time
        if enemy.hurt_time <= 0:
            # Повернення до переслідування, якщо гравець видимий
            if self._can_see_player(enemy, player):
                enemy.state = "chase"
            else:
                enemy.state = "patrol"
    
    def _update_dead(self, enemy, player, delta_time):
        """Оновлення ворога в стані смерті"""
        # Анімація смерті триває певний час
        enemy.death_time -= delta_time
        if enemy.death_time <= 0:
            # Позначаємо ворога для видалення
            enemy.should_remove = True