import pygame
import json
import os
from src.utils.constants import MAP_PATH

class Scene:
    """Базовий клас для всіх сцен гри"""
    
    def __init__(self, renderer):
        """Ініціалізація сцени"""
        self.renderer = renderer
        self.entities = []  # Список сутностей на сцені
    
    def load(self):
        """Завантаження ресурсів сцени"""
        pass
    
    def unload(self):
        """Вивантаження ресурсів сцени"""
        pass
    
    def handle_input(self, input_handler):
        """Обробка введення користувача"""
        pass
    
    def update(self, delta_time):
        """Оновлення стану сцени"""
        # Оновлення всіх сутностей
        for entity in self.entities:
            entity.update(delta_time)
    
    def render(self, surface):
        """Рендеринг сцени"""
        # Рендеринг всіх сутностей
        for entity in self.entities:
            entity.render(surface, self.renderer)


class GameplayScene(Scene):
    """Клас для ігрового процесу"""
    
    def __init__(self, renderer, map_name):
        """Ініціалізація ігрової сцени"""
        super().__init__(renderer)
        self.map_name = map_name
        self.map_data = None
        self.player = None
        self.enemies = []
        self.items = []
        self.camera_offset = [0, 0]
        self.collision_system = None
        self.ai_system = None
    
    def load(self):
        """Завантаження ресурсів сцени"""
        # Завантаження карти
        map_path = os.path.join(MAP_PATH, f"{self.map_name}.json")
        try:
            with open(map_path, 'r') as f:
                self.map_data = json.load(f)
        except FileNotFoundError:
            print(f"Помилка: Карта {map_path} не знайдена.")
            return False
        
        # TODO: Створення гравця, ворогів, предметів на основі даних карти
        from src.entities.player import Player
        from src.entities.enemy import Enemy
        from src.systems.collision import CollisionSystem
        from src.systems.ai import AISystem
        
        # Створення систем
        self.collision_system = CollisionSystem(self.map_data)
        self.ai_system = AISystem()
        
        # Створення гравця
        player_start = self.map_data.get("player_start", {"x": 100, "y": 100})
        self.player = Player(player_start["x"], player_start["y"])
        self.entities.append(self.player)
        
        # Створення ворогів
        for enemy_data in self.map_data.get("enemies", []):
            enemy = Enemy(enemy_data["x"], enemy_data["y"], enemy_data.get("type", "basic"))
            self.enemies.append(enemy)
            self.entities.append(enemy)
        
        # Назначення систем
        for enemy in self.enemies:
            enemy.set_ai_system(self.ai_system)
        
        self.player.set_collision_system(self.collision_system)
        for enemy in self.enemies:
            enemy.set_collision_system(self.collision_system)
        
        return True
    
    def handle_input(self, input_handler):
        """Обробка введення користувача"""
        # Передаємо керування гравцю
        if self.player:
            self.player.handle_input(input_handler)
    
    def update(self, delta_time):
        """Оновлення стану сцени"""
        # Оновлення систем
        if self.ai_system:
            self.ai_system.update(self.player, self.enemies, delta_time)
        
        # Оновлення сутностей
        super().update(delta_time)
        
        # Оновлення положення камери відносно гравця
        if self.player:
            from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT
            self.camera_offset[0] = self.player.x - SCREEN_WIDTH // 2
            self.camera_offset[1] = self.player.y - SCREEN_HEIGHT // 2
    
    def render(self, surface):
        """Рендеринг сцени"""
        # Рендеринг карти
        if self.map_data:
            self.renderer.draw_map(surface, self.map_data, self.camera_offset)
        
        # Рендеринг сутностей з урахуванням зміщення камери
        for entity in self.entities:
            pos_x = entity.x - self.camera_offset[0]
            pos_y = entity.y - self.camera_offset[1]
            entity.render(surface, self.renderer, (pos_x, pos_y))
        
        # Рендеринг інтерфейсу
        from src.ui.hud import HUD
        hud = HUD(self.player)
        hud.render(surface, self.renderer)


class MainMenuScene(Scene):
    """Клас для головного меню"""
    
    def __init__(self, renderer):
        """Ініціалізація сцени головного меню"""
        super().__init__(renderer)
        self.selected_option = 0
        self.options = ["Нова гра", "Налаштування", "Вихід"]
    
    def load(self):
        """Завантаження ресурсів сцени"""
        # Завантаження фонового зображення і шрифтів
        self.renderer.load_texture("menu_background", "assets/textures/menu_bg.png")
        self.renderer.load_font("menu_title", None, 48)  # Використовуємо стандартний шрифт
        self.renderer.load_font("menu_option", None, 24)
        return True
    
    def handle_input(self, input_handler):
        """Обробка введення користувача"""
        # Навігація по меню
        if input_handler.is_key_pressed("up"):
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif input_handler.is_key_pressed("down"):
            self.selected_option = (self.selected_option + 1) % len(self.options)
        
        # Вибір опції
        if input_handler.is_key_pressed("shoot"):
            if self.options[self.selected_option] == "Нова гра":
                # TODO: перехід до ігрової сцени
                pass
            elif self.options[self.selected_option] == "Налаштування":
                # TODO: перехід до сцени налаштувань
                pass
            elif self.options[self.selected_option] == "Вихід":
                pygame.quit()
                sys.exit()
    
    def render(self, surface):
        """Рендеринг сцени"""
        # Фон
        self.renderer.draw_texture(surface, "menu_background", (0, 0))
        
        # Заголовок
        from src.utils.constants import SCREEN_WIDTH, WHITE, RED
        self.renderer.draw_text(surface, "2D DOOM", "menu_title", 
                             (SCREEN_WIDTH // 2, 100), WHITE, True)
        
        # Опції меню
        for i, option in enumerate(self.options):
            color = RED if i == self.selected_option else WHITE
            self.renderer.draw_text(surface, option, "menu_option", 
                                 (SCREEN_WIDTH // 2, 250 + i * 50), color, True)


class SceneManager:
    """Керує сценами гри"""
    
    def __init__(self):
        """Ініціалізація менеджера сцен"""
        from src.engine.renderer import Renderer
        self.renderer = Renderer()
        self.scenes = {}
        self.current_scene = None
        
        # Реєстрація сцен
        self.register_scenes()
    
    def register_scenes(self):
        """Реєстрація доступних сцен"""
        self.scenes["main_menu"] = MainMenuScene(self.renderer)
        # Ігрові рівні будуть додаватись динамічно
    
    def load_scene(self, scene_name, **kwargs):
        """Завантаження сцени за ім'ям"""
        # Вивантаження поточної сцени, якщо вона є
        if self.current_scene:
            self.current_scene.unload()
        
        # Завантаження нової сцени
        if scene_name == "gameplay":
            # Спеціальна обробка ігрової сцени з картою
            map_name = kwargs.get("map_name", "level1")
            scene = GameplayScene(self.renderer, map_name)
            success = scene.load()
            if success:
                self.current_scene = scene
                return True
            return False
        elif scene_name in self.scenes:
            # Завантаження зареєстрованої сцени
            scene = self.scenes[scene_name]
            success = scene.load()
            if success:
                self.current_scene = scene
                return True
            return False
        else:
            print(f"Помилка: Сцена {scene_name} не знайдена.")
            return False