import pygame
from src.utils.constants import TILE_SIZE

class Renderer:
    """Відповідає за рендеринг різних елементів гри"""
    
    def __init__(self):
        """Ініціалізація рендерера"""
        self.textures = {}  # Словник для зберігання текстур
        self.fonts = {}     # Словник для зберігання шрифтів
    
    def load_texture(self, name, path):
        """Завантаження текстури з файлу"""
        try:
            texture = pygame.image.load(path).convert_alpha()
            self.textures[name] = texture
            return True
        except pygame.error:
            print(f"Помилка завантаження текстури: {path}")
            return False
    
    def load_font(self, name, path, size):
        """Завантаження шрифту"""
        try:
            font = pygame.font.Font(path, size)
            self.fonts[name] = font
            return True
        except pygame.error:
            print(f"Помилка завантаження шрифту: {path}")
            # Використання стандартного шрифту, якщо не вдалося завантажити
            self.fonts[name] = pygame.font.SysFont("Arial", size)
            return False
    
    def draw_texture(self, surface, texture_name, position, scale=1.0, rotation=0):
        """Малювання текстури на поверхні"""
        if texture_name in self.textures:
            texture = self.textures[texture_name]
            
            # Масштабування, якщо потрібно
            if scale != 1.0:
                original_size = texture.get_size()
                new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
                texture = pygame.transform.scale(texture, new_size)
            
            # Поворот, якщо потрібно
            if rotation != 0:
                texture = pygame.transform.rotate(texture, rotation)
            
            # Малювання
            surface.blit(texture, position)
    
    def draw_text(self, surface, text, font_name, position, color, centered=False):
        """Малювання тексту на поверхні"""
        if font_name in self.fonts:
            font = self.fonts[font_name]
            text_surface = font.render(text, True, color)
            
            # Центрування тексту, якщо потрібно
            if centered:
                text_rect = text_surface.get_rect(center=position)
                surface.blit(text_surface, text_rect)
            else:
                surface.blit(text_surface, position)
    
    def draw_map(self, surface, tile_map, camera_offset=(0, 0)):
        """Малювання карти з плиток"""
        for y, row in enumerate(tile_map.data):
            for x, tile_id in enumerate(row):
                if tile_id > 0:  # 0 зазвичай означає порожню клітинку
                    # Обчислення позиції плитки з урахуванням зміщення камери
                    pos_x = x * TILE_SIZE - camera_offset[0]
                    pos_y = y * TILE_SIZE - camera_offset[1]
                    
                    # Перевірка видимості плитки на екрані (оптимізація)
                    if -TILE_SIZE <= pos_x < surface.get_width() and -TILE_SIZE <= pos_y < surface.get_height():
                        texture_name = f"tile_{tile_id}"
                        self.draw_texture(surface, texture_name, (pos_x, pos_y))