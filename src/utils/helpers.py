"""
Допоміжні функції для гри.
Цей файл містить утилітарні функції, які використовуються в різних частинах гри.
"""

import os
import json
import math
import random
import pygame
from pygame.locals import *
import pickle
from datetime import datetime

from src.utils.constants import RESOURCE_PATHS, SCREEN_WIDTH, SCREEN_HEIGHT, COLORS


def load_image(filename, alpha=True):
    """
    Завантаження зображення з папки assets
    
    Args:
        filename: Шлях до файлу відносно папки assets
        alpha: Чи використовувати прозорість
        
    Returns:
        pygame.Surface: Завантажене зображення
    """
    # Перевірка наявності файлу
    full_path = os.path.join(RESOURCE_PATHS["textures"], filename)
    if not os.path.exists(full_path):
        # Створення заглушки, якщо файл не знайдено
        surface = pygame.Surface((64, 64))
        surface.fill(COLORS["purple"])  # Фіолетовий колір для відсутніх текстур
        pygame.draw.rect(surface, COLORS["black"], (0, 0, 64, 64), 1)
        text_font = pygame.font.Font(None, 12)
        text_surface = text_font.render("NO TEXTURE", True, COLORS["black"])
        surface.blit(text_surface, (10, 25))
        return surface
    
    try:
        image = pygame.image.load(full_path)
        if alpha:
            return image.convert_alpha()
        return image.convert()
    except pygame.error as e:
        print(f"Помилка завантаження зображення {filename}: {e}")
        # Створення заглушки у випадку помилки
        surface = pygame.Surface((64, 64))
        surface.fill(COLORS["red"])
        return surface


def load_sound(filename):
    """
    Завантаження звукового файлу з папки assets
    
    Args:
        filename: Шлях до файлу відносно папки assets
        
    Returns:
        pygame.mixer.Sound: Завантажений звук
    """
    full_path = os.path.join(RESOURCE_PATHS["sounds"], filename)
    if not os.path.exists(full_path):
        print(f"Звуковий файл не знайдено: {filename}")
        return None
    
    try:
        return pygame.mixer.Sound(full_path)
    except pygame.error as e:
        print(f"Помилка завантаження звуку {filename}: {e}")
        return None


def load_map(map_name):
    """
    Завантаження карти з файлу JSON
    
    Args:
        map_name: Назва файлу карти
        
    Returns:
        dict: Дані карти
    """
    full_path = os.path.join(RESOURCE_PATHS["maps"], f"{map_name}.json")
    if not os.path.exists(full_path):
        print(f"Файл карти не знайдено: {map_name}")
        return None
    
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            map_data = json.load(file)
        return map_data
    except json.JSONDecodeError as e:
        print(f"Помилка парсингу карти {map_name}: {e}")
        return None
    except Exception as e:
        print(f"Помилка завантаження карти {map_name}: {e}")
        return None


def distance(x1, y1, x2, y2):
    """
    Обчислення відстані між двома точками
    
    Args:
        x1, y1: Координати першої точки
        x2, y2: Координати другої точки
        
    Returns:
        float: Відстань між точками
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def angle_to_vector(angle):
    """
    Перетворення кута в вектор напрямку
    
    Args:
        angle: Кут у радіанах
        
    Returns:
        tuple: (dx, dy) нормалізований вектор напрямку
    """
    dx = math.cos(angle)
    dy = math.sin(angle)
    return (dx, dy)


def vector_to_angle(dx, dy):
    """
    Перетворення вектора напрямку в кут
    
    Args:
        dx, dy: Компоненти вектора
        
    Returns:
        float: Кут у радіанах
    """
    return math.atan2(dy, dx)


def normalize_vector(dx, dy):
    """
    Нормалізація вектора
    
    Args:
        dx, dy: Компоненти вектора
        
    Returns:
        tuple: (dx, dy) нормалізований вектор
    """
    length = math.sqrt(dx**2 + dy**2)
    if length == 0:
        return (0, 0)
    return (dx/length, dy/length)


def clamp(value, min_val, max_val):
    """
    Обмеження значення в заданому діапазоні
    
    Args:
        value: Значення для обмеження
        min_val: Мінімальне допустиме значення
        max_val: Максимальне допустиме значення
        
    Returns:
        Обмежене значення
    """
    return max(min_val, min(value, max_val))


def is_point_in_rect(point, rect):
    """
    Перевірка чи точка знаходиться всередині прямокутника
    
    Args:
        point: Кортеж (x, y)
        rect: Прямокутник pygame.Rect або кортеж (x, y, width, height)
        
    Returns:
        bool: True якщо точка в прямокутнику, False інакше
    """
    x, y = point
    if isinstance(rect, pygame.Rect):
        return rect.collidepoint(x, y)
    else:
        rx, ry, rw, rh = rect
        return rx <= x <= rx + rw and ry <= y <= ry + rh


def is_line_intersecting_line(line1, line2):
    """
    Перевірка перетину двох ліній
    
    Args:
        line1: Кортеж ((x1, y1), (x2, y2))
        line2: Кортеж ((x3, y3), (x4, y4))
        
    Returns:
        bool: True якщо лінії перетинаються, False інакше
    """
    (x1, y1), (x2, y2) = line1
    (x3, y3), (x4, y4) = line2
    
    # Обчислення детермінантів
    den = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if den == 0:
        return False  # Лінії паралельні
        
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den
    
    # Перевірка чи точка перетину знаходиться на обох відрізках
    return 0 <= ua <= 1 and 0 <= ub <= 1


def ray_cast(origin, angle, walls, max_distance=1000):
    """
    Простий рейкаст для виявлення зіткнень
    
    Args:
        origin: Початкова точка (x, y)
        angle: Кут променя в радіанах
        walls: Список стін - кожна стіна є відрізком ((x1, y1), (x2, y2))
        max_distance: Максимальна відстань променя
        
    Returns:
        tuple: (hit_point, distance, wall_hit) або None, якщо немає зіткнення
    """
    x, y = origin
    dx, dy = math.cos(angle), math.sin(angle)
    
    # Кінцева точка променя
    end_x = x + dx * max_distance
    end_y = y + dy * max_distance
    ray = ((x, y), (end_x, end_y))
    
    closest_hit = None
    closest_distance = float('inf')
    closest_wall = None
    
    for wall in walls:
        if is_line_intersecting_line(ray, wall):
            # Знаходження точки перетину
            (x1, y1), (x2, y2) = ray
            (x3, y3), (x4, y4) = wall
            
            den = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
            ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
            
            # Обчислення точки перетину
            hit_x = x1 + ua * (x2 - x1)
            hit_y = y1 + ua * (y2 - y1)
            
            # Обчислення відстані
            hit_distance = distance(x, y, hit_x, hit_y)
            
            if hit_distance < closest_distance:
                closest_hit = (hit_x, hit_y)
                closest_distance = hit_distance
                closest_wall = wall
    
    if closest_hit:
        return (closest_hit, closest_distance, closest_wall)
    return None


def create_rotation_matrix(angle):
    """
    Створення матриці повороту
    
    Args:
        angle: Кут повороту в радіанах
        
    Returns:
        tuple: ((cos, -sin), (sin, cos)) матриця повороту
    """
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    return ((cos_val, -sin_val), (sin_val, cos_val))


def rotate_point(point, origin, angle):
    """
    Обертання точки навколо початку координат
    
    Args:
        point: Точка (x, y) для обертання
        origin: Точка (ox, oy) - центр обертання
        angle: Кут у радіанах
        
    Returns:
        tuple: (x, y) обернута точка
    """
    x, y = point
    ox, oy = origin
    
    # Переміщення в систему координат з центром в origin
    tx = x - ox
    ty = y - oy
    
    # Створення матриці повороту
    rot_matrix = create_rotation_matrix(angle)
    
    # Множення на матрицю повороту
    rx = tx * rot_matrix[0][0] + ty * rot_matrix[0][1]
    ry = tx * rot_matrix[1][0] + ty * rot_matrix[1][1]
    
    # Повернення в початкову систему координат
    return (rx + ox, ry + oy)


def scale_surface(surface, scale_factor):
    """
    Масштабування поверхні Pygame
    
    Args:
        surface: Поверхня Pygame для масштабування
        scale_factor: Коефіцієнт масштабування
        
    Returns:
        pygame.Surface: Масштабована поверхня
    """
    width = int(surface.get_width() * scale_factor)
    height = int(surface.get_height() * scale_factor)
    return pygame.transform.scale(surface, (width, height))


def draw_text(surface, text, size, x, y, color=COLORS["white"], 
              align="left", font_name=None):
    """
    Відображення тексту на поверхні
    
    Args:
        surface: Поверхня для відображення
        text: Текст для відображення
        size: Розмір шрифту
        x, y: Координати для відображення
        color: Колір тексту (RGB)
        align: Вирівнювання тексту ("left", "center", "right")
        font_name: Назва шрифту (None для стандартного)
    """
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if align == "center":
        text_rect.centerx = x
        text_rect.y = y
    elif align == "right":
        text_rect.right = x
        text_rect.y = y
    else:  # left align
        text_rect.x = x
        text_rect.y = y
        
    surface.blit(text_surface, text_rect)


def create_health_bar(current, maximum, width, height, 
                     color_healthy=COLORS["green"], 
                     color_damaged=COLORS["yellow"], 
                     color_critical=COLORS["red"]):
    """
    Створення панелі здоров'я
    
    Args:
        current: Поточне значення здоров'я
        maximum: Максимальне значення здоров'я
        width: Ширина панелі
        height: Висота панелі
        color_healthy: Колір для високого рівня здоров'я
        color_damaged: Колір для середнього рівня здоров'я
        color_critical: Колір для низького рівня здоров'я
        
    Returns:
        pygame.Surface: Поверхня з панеллю здоров'я
    """
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Фон панелі
    pygame.draw.rect(surface, COLORS["dark_gray"], (0, 0, width, height))
    
    # Визначення відсотка здоров'я та кольору
    health_percent = current / maximum if maximum > 0 else 0
    health_width = int(width * health_percent)
    
    if health_percent > 0.7:
        color = color_healthy
    elif health_percent > 0.3:
        color = color_damaged
    else:
        color = color_critical
        
    # Заповнення панелі
    if health_width > 0:
        pygame.draw.rect(surface, color, (0, 0, health_width, height))
    
    # Рамка панелі
    pygame.draw.rect(surface, COLORS["black"], (0, 0, width, height), 1)
    
    return surface


def save_game(player, game_state, slot_number):
    """
    Збереження гри
    
    Args:
        player: Об'єкт гравця
        game_state: Стан гри
        slot_number: Номер слота для збереження
        
    Returns:
        bool: True якщо збереження успішне, False інакше
    """
    if not os.path.exists(RESOURCE_PATHS["saves"]):
        os.makedirs(RESOURCE_PATHS["saves"])
        
    save_data = {
        "player": player,
        "game_state": game_state,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        with open(f"{RESOURCE_PATHS['saves']}save_{slot_number}.pickle", "wb") as file:
            pickle.dump(save_data, file)
        return True
    except Exception as e:
        print(f"Помилка збереження гри: {e}")
        return False


def load_game(slot_number):
    """
    Завантаження гри зі збереження
    
    Args:
        slot_number: Номер слота для завантаження
        
    Returns:
        tuple: (player, game_state) або None у випадку помилки
    """
    save_path = f"{RESOURCE_PATHS['saves']}save_{slot_number}.pickle"
    
    if not os.path.exists(save_path):
        print(f"Збереження не знайдено: {save_path}")
        return None
    
    try:
        with open(save_path, "rb") as file:
            save_data = pickle.load(file)
        
        return (save_data["player"], save_data["game_state"])
    except Exception as e:
        print(f"Помилка завантаження гри: {e}")
        return None


def get_save_info():
    """
    Отримання інформації про збережені ігри
    
    Returns:
        list: Список даних про збереження
    """
    save_info = []
    
    if not os.path.exists(RESOURCE_PATHS["saves"]):
        return save_info
    
    for i in range(1, 6):  # Перевірка 5 слотів
        save_path = f"{RESOURCE_PATHS['saves']}save_{i}.pickle"
        
        if os.path.exists(save_path):
            try:
                with open(save_path, "rb") as file:
                    save_data = pickle.load(file)
                    
                save_info.append({
                    "slot": i,
                    "timestamp": save_data["timestamp"],
                    "player_health": save_data["player"].health,
                    "level": save_data["game_state"].current_level
                })
            except Exception as e:
                print(f"Помилка читання інформації про збереження: {e}")
    
    return save_info


def generate_random_id(length=8):
    """
    Генерація випадкового ідентифікатора
    
    Args:
        length: Довжина ідентифікатора
        
    Returns:
        str: Випадковий ідентифікатор
    """
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(chars) for _ in range(length))


def create_simple_particle_effect(position, color, count=10, speed=3.0, lifetime=0.5):
    """
    Створення простого ефекту частинок
    
    Args:
        position: Позиція (x, y) для створення частинок
        color: Колір частинок (RGB)
        count: Кількість частинок
        speed: Базова швидкість частинок
        lifetime: Час життя частинок у секундах
        
    Returns:
        list: Список частинок [(x, y, dx, dy, size, color, lifetime), ...]
    """
    particles = []
    x, y = position
    
    for _ in range(count):
        angle = random.uniform(0, 2 * math.pi)
        speed_factor = random.uniform(0.5, 1.5) * speed
        dx = math.cos(angle) * speed_factor
        dy = math.sin(angle) * speed_factor
        size = random.randint(2, 5)
        
        # Невелика варіація кольору
        r, g, b = color
        r = clamp(r + random.randint(-20, 20), 0, 255)
        g = clamp(g + random.randint(-20, 20), 0, 255)
        b = clamp(b + random.randint(-20, 20), 0, 255)
        
        particles.append((x, y, dx, dy, size, (r, g, b), lifetime))
    
    return particles


def create_explosion_effect(position, color, count=30, speed=5.0, lifetime=1.0):
    """
    Створення ефекту вибуху
    
    Args:
        position: Позиція (x, y) для створення вибуху
        color: Базовий колір частинок (RGB)
        count: Кількість частинок
        speed: Базова швидкість частинок
        lifetime: Час життя частинок у секундах
        
    Returns:
        list: Список частинок [(x, y, dx, dy, size, color, lifetime), ...]
    """
    return create_simple_particle_effect(position, color, count, speed, lifetime)


def update_particles(particles, dt):
    """
    Оновлення стану частинок
    
    Args:
        particles: Список частинок
        dt: Часовий крок
        
    Returns:
        list: Оновлений список частинок
    """
    new_particles = []
    
    for x, y, dx, dy, size, color, lifetime in particles:
        lifetime -= dt
        if lifetime > 0:
            x += dx
            y += dy
            size = max(1, size - dt)  # Зменшення розміру з часом
            new_particles.append((x, y, dx, dy, size, color, lifetime))
    
    return new_particles


def draw_particles(surface, particles):
    """
    Відображення частинок на екрані
    
    Args:
        surface: Поверхня для відображення
        particles: Список частинок
    """
    for x, y, _, _, size, color, _ in particles:
        pygame.draw.circle(surface, color, (int(x), int(y)), int(size))
        
        
def wrap_text(text, font, max_width):
    """
    Розрив тексту на кілька рядків щоб вмістити в задану ширину
    
    Args:
        text: Вхідний текст
        font: Шрифт Pygame
        max_width: Максимальна ширина тексту
        
    Returns:
        list: Список рядків тексту
    """
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines


def draw_text_box(surface, text, rect, font, text_color=COLORS["white"], 
                 bg_color=COLORS["dark_gray"], padding=5):
    """
    Відображення тексту в прямокутнику з автоматичним переносом
    
    Args:
        surface: Поверхня для відображення
        text: Текст для відображення
        rect: Прямокутник pygame.Rect для розміщення тексту
        font: Шрифт Pygame
        text_color: Колір тексту
        bg_color: Колір фону
        padding: Внутрішній відступ
    """
    # Малювання фону
    pygame.draw.rect(surface, bg_color, rect)
    pygame.draw.rect(surface, COLORS["black"], rect, 1)
    
    # Розрахунок доступної ширини
    available_width = rect.width - 2 * padding
    
    # Розбиття тексту на рядки
    lines = wrap_text(text, font, available_width)
    
    # Відображення кожного рядка
    line_height = font.get_height()
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.x = rect.x + padding
        text_rect.y = rect.y + padding + i * line_height
        surface.blit(text_surface, text_rect)