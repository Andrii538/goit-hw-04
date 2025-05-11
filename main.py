import pygame
import sys
import os
from src.engine.game_loop import GameLoop
from src.engine.scene_manager import SceneManager
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE

def main():
    """Основна функція запуску гри"""
    # Ініціалізація Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Створення вікна
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    
    # Створення менеджера сцен
    scene_manager = SceneManager()
    
    # Створення ігрового циклу
    game = GameLoop(screen, scene_manager)
    
    # Запуск гри
    game.run()
    
    # Закриття гри
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
