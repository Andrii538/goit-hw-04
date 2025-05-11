import pygame
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED

class HUD:
    """Головний ігровий інтерфейс"""
    
    def __init__(self, player):
        """Ініціалізація HUD"""
        self.player = player
    
    def render(self, surface, renderer):
        """Рендеринг HUD"""
        # Відображення здоров'я
        self._render_health_bar(surface, renderer)
        
        # Відображення зброї та набоїв
        self._render_weapon_info(surface, renderer)
        
        # Мінікарта
        self._render_minimap(surface, renderer)
    
    def _render_health_bar(self, surface, renderer):
        """Відображення шкали здоров'я"""
        # Фон шкали здоров'я
        pygame.draw.rect(surface, (50, 50, 50), (20, SCREEN_HEIGHT - 40, 200, 20))
        
        # Заповнення відповідно до поточного здоров'я
        health_width = 200 * (self.player.health / self.player.max_health)
        health_color = (0, 255, 0)  # Зелений для здоров'я
        
        # Зміна кольору при низькому здоров'ї
        if self.player.health < self.player.max_health * 0.3:
            health_color = (255, 0, 0)  # Червоний для низького здоров'я
        elif self.player.health < self.player.max_health * 0.7:
            health_color = (255, 255, 0)  # Жовтий для середнього здоров'я
        
        pygame.draw.rect(surface, health_color, (20, SCREEN_HEIGHT - 40, health_width, 20))
        
        # Текст з точним значенням здоров'я
        health_text = f"Здоров'я: {int(self.player.health)}/{self.player.max_health}"
        renderer.draw_text(surface, health_text, "hud_small", (25, SCREEN_HEIGHT - 38), WHITE)
    
    def _render_weapon_info(self, surface, renderer):
        """Відображення інформації про зброю"""
        if self.player.current_weapon:
            # Іконка поточної зброї
            weapon_icon = f"weapon_icon_{self.player.current_weapon.type}"
            renderer.draw_texture(surface, weapon_icon, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 70))
            
            # Кількість набоїв
            ammo_text = f"{self.player.current_weapon.ammo}/{self.player.current_weapon.max_ammo}"
            renderer.draw_text(surface, ammo_text, "hud_medium", 
                           (SCREEN_WIDTH - 90, SCREEN_HEIGHT - 30), WHITE)
    
    def _render_minimap(self, surface, renderer):
        """Відображення мінікарти"""
        # Розмір та позиція мінікарти
        minimap_size = 150
        minimap_x = SCREEN_WIDTH - minimap_size - 10
        minimap_y = 10
        
        # Фон мінікарти
        pygame.draw.rect(surface, (0, 0, 0), (minimap_x, minimap_y, minimap_size, minimap_size))
        pygame.draw.rect(surface, (100, 100, 100), (minimap_x, minimap_y, minimap_size, minimap_size), 2)
        
        # TODO: Відображення карти, гравця та ворогів на мінікарті
        # В повній реалізації тут буде код для відображення спрощеної версії карти
        
        # Позиція гравця на мінікарті (просто як приклад)
        player_mini_x = minimap_x + minimap_size // 2
        player_mini_y = minimap_y + minimap_size // 2
        pygame.draw.circle(surface, (0, 255, 0), (player_mini_x, player_mini_y), 4)