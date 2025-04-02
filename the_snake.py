"""Модуль игры "Змейка" на Python с использованием библиотеки Pygame."""
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Начальная позиция обьектов
INITIAL_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Словарь допустимых поворотов
TURNS = {
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT
}

# Множество клавиш для поворота
TURN_KEYS = {key for key, _ in TURNS}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 8

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=INITIAL_POSITION, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position, color=None, border=True):
        """Отрисовывает одну ячейку объекта."""
        if color is None:
            color = self.body_color
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        if border:
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self, occupied_positions=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        if occupied_positions is None:
            occupied_positions = []
        self.position = self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Устанавливает случайную позицию яблока."""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in occupied_positions:
                return position

    def draw(self):
        """Отрисовывает яблоко."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        if new_direction:
            self.direction = new_direction

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head = (
            (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку."""
        for position in self.positions:
            self.draw_cell(position)

        self.draw_cell(self.positions[0], SNAKE_COLOR)

        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR, border=False)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key in TURN_KEYS:
                new_direction = TURNS.get((event.key, game_object.direction))
                game_object.update_direction(new_direction)


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    pygame.init()

    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        screen.fill(BOARD_BACKGROUND_COLOR)
        pygame.display.update()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)

        if len(snake.positions) != len(set(snake.positions)):
            screen.fill(BOARD_BACKGROUND_COLOR)
            pygame.display.update()
            snake.reset()

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
