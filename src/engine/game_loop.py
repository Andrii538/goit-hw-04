import pygame
import sys
from src.engine.input_handler import InputHandler
from src.utils.constants import FPS, BLACK

class GameLoop:
    """Основний цикл гри, відповідає за оновлення стану та рендеринг"""
    
    def __init__(self, screen, scene_manager):
        """Ініціалізація ігрового циклу"""
        self.screen = screen
        self.scene_manager = scene_manager
        self.input_handler = InputHandler()
        self.clock = pygame.time.Clock()
        self.running = True
    
    def process_events(self):
        """Обробка подій Pygame"""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        
        # Оновлення стану введення
        self.input_handler.update(events)
        
        # Обробка введення у поточній сцені
        if self.scene_manager.current_scene:
            self.scene_manager.current_scene.handle_input(self.input_handler)
    
    def update(self):
        """Оновлення ігрового стану"""
        delta_time = self.clock.get_time() / 1000.0  # Переведення у секунди
        
        # Оновлення поточної сцени
        if self.scene_manager.current_scene:
            self.scene_manager.current_scene.update(delta_time)
    
    def render(self):
        """Рендеринг гри"""
        self.screen.fill(BLACK)  # Очищення екрану
        
        # Рендеринг поточної сцени
        if self.scene_manager.current_scene:
            self.scene_manager.current_scene.render(self.screen)
        
        pygame.display.flip()  # Оновлення екрану
    
    def run(self):
        """Запуск ігрового циклу"""
        # Загрузка початкової сцени
        self.scene_manager.load_scene("main_menu")
        
        # Головний цикл
        while self.running:
            self.process_events()
            self.update()
            self.render()
            self.clock.tick(FPS)