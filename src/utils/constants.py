"""
Константи та налаштування для гри.
Цей файл містить усі константи, які використовуються в грі.
"""

# Налаштування екрану
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "2D Doom - Pygame"
FPS = 60

# Розмір тайлів у грі
TILE_SIZE = 64

# Налаштування гравця
PLAYER_SPEED = 5.0
PLAYER_ROTATION_SPEED = 3.0
PLAYER_MAX_HEALTH = 100
PLAYER_MAX_ARMOR = 100
PLAYER_RADIUS = 20
PLAYER_START_WEAPONS = ["pistol", "shotgun"]  # Початкова зброя

# Налаштування ворогів
ENEMY_SPEEDS = {
    "zombie": 2.0,
    "imp": 3.0,
    "demon": 4.0,
    "cacodemon": 2.5
}
ENEMY_HEALTH = {
    "zombie": 30,
    "imp": 50,
    "demon": 80,
    "cacodemon": 100
}
ENEMY_DAMAGE = {
    "zombie": 5,
    "imp": 10,
    "demon": 15,
    "cacodemon": 20
}
ENEMY_ATTACK_RANGE = {
    "zombie": 50,
    "imp": 300,  # Може стріляти
    "demon": 60,
    "cacodemon": 350  # Може стріляти
}
ENEMY_SIGHT_RANGE = 500  # Відстань, на якій вороги бачать гравця
ENEMY_SPAWN_RATE = 0.01  # Ймовірність появи ворога за кадр

# Налаштування зброї
WEAPON_DAMAGE = {
    "pistol": 10,
    "shotgun": 25,
    "chaingun": 15,
    "rocket_launcher": 50
}
WEAPON_FIRE_RATE = {
    "pistol": 0.5,  # Секунди між пострілами
    "shotgun": 0.8,
    "chaingun": 0.1,
    "rocket_launcher": 1.2
}
WEAPON_RELOAD_TIME = {
    "pistol": 1.0,
    "shotgun": 1.5,
    "chaingun": 2.0,
    "rocket_launcher": 2.5
}
WEAPON_MAX_AMMO = {
    "pistol": 999,  # Необмежений боєзапас для пістолета
    "shotgun": 50,
    "chaingun": 200,
    "rocket_launcher": 20
}
WEAPON_BULLET_SPEED = 10.0

# Налаштування предметів
ITEM_PICKUP_RADIUS = 30
ITEM_EFFECTS = {
    "medkit_small": 25,
    "medkit_large": 50,
    "armor_shard": 5,
    "armor_vest": 50,
    "ammo_small": 10,
    "ammo_large": 25
}
ITEM_RESPAWN_TIME = 30  # Секунди до повторної появи предмета

# Налаштування звуку
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.7

# Налаштування інтерфейсу
INVENTORY_SLOTS = 10  # Кількість слотів в інвентарі
HUD_MARGIN = 20  # Відступ від країв екрану

# Кольори у форматі RGB
COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "purple": (255, 0, 255),
    "cyan": (0, 255, 255),
    "gray": (128, 128, 128),
    "dark_gray": (64, 64, 64),
    "light_gray": (192, 192, 192),
    "brown": (139, 69, 19),
    "dark_red": (139, 0, 0),
    "orange": (255, 165, 0),
    "highlight": (255, 215, 0),  # Золотий для виділення
    "transparent": (0, 0, 0, 0)
}

# Маски колізій
COLLISION_MASK = {
    "player": 0b0001,
    "enemy": 0b0010,
    "wall": 0b0100,
    "projectile": 0b1000,
    "item": 0b10000
}

# Налаштування ефектів
PARTICLE_LIFETIME = 0.5  # Секунди життя частинок
PARTICLE_SPEED = 3.0
FLASH_DURATION = 0.1  # Секунди для ефекту спалаху

# Налаштування фізики
GRAVITY = 0.0  # Відсутність гравітації в 2D Doom
FRICTION = 0.9  # Тертя для плавного гальмування

# Налаштування штучного інтелекту
AI_UPDATE_RATE = 5  # Оновлення штучного інтелекту кожні N кадрів
AI_ROAMING_DISTANCE = 200  # Відстань для випадкового переміщення ворогів
AI_PURSUIT_DISTANCE = 300  # Відстань для переслідування гравця

# Налаштування збереження гри
SAVE_GAME_SLOTS = 5  # Кількість слотів для збереження
AUTOSAVE_INTERVAL = 300  # Секунди між автозбереженнями

# Налаштування хвиль ворогів
WAVE_ENEMY_BASE_COUNT = 5  # Базова кількість ворогів у хвилі
WAVE_ENEMY_INCREMENT = 2  # Приріст ворогів з кожною хвилею
WAVE_BREAK_TIME = 15  # Секунди перерви між хвилями

# Налаштування складності
DIFFICULTY_MULTIPLIERS = {
    "easy": {"enemy_health": 0.75, "enemy_damage": 0.75, "enemy_speed": 0.75},
    "normal": {"enemy_health": 1.0, "enemy_damage": 1.0, "enemy_speed": 1.0},
    "hard": {"enemy_health": 1.25, "enemy_damage": 1.25, "enemy_speed": 1.25},
    "nightmare": {"enemy_health": 1.5, "enemy_damage": 1.5, "enemy_speed": 1.5}
}

# Налаштування досягнень
ACHIEVEMENTS = {
    "first_blood": "Перший убитий ворог",
    "rampage": "Вбито 10 ворогів за 30 секунд",
    "survivor": "Пройдено рівень без смертей",
    "collector": "Зібрано всі предмети на рівні",
    "speedrunner": "Пройдено рівень за 5 хвилин"
}

# Налаштування керування
DEFAULT_CONTROLS = {
    "move_up": "w",
    "move_down": "s",
    "move_left": "a",
    "move_right": "d",
    "shoot": "mouse1",
    "reload": "r",
    "interact": "e",
    "inventory": "tab",
    "weapon_1": "1",
    "weapon_2": "2",
    "weapon_3": "3",
    "weapon_4": "4",
    "pause": "escape"
}

# Шляхи до ресурсів
RESOURCE_PATHS = {
    "textures": "assets/textures/",
    "sounds": "assets/sounds/",
    "maps": "assets/maps/",
    "fonts": "assets/fonts/",
    "saves": "saves/"
}

# Додаткові налаштування гри
DEBUG_MODE = False  # Увімкнення/вимкнення режиму відлагодження
SHOW_FPS = True  # Показувати лічильник FPS
ENABLE_VSYNC = True  # Увімкнення/вимкнення вертикальної синхронізації