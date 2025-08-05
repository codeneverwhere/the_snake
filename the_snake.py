"""Snake game module in Python using the Pygame library."""
from random import randint

import pygame

# Constants for the game field and grid sizes.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Initial position of the game objects.
INITIAL_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Movement directions:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Dictionary of valid turns.
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

# Set of keys used for turning.
TURN_KEYS = {key for key, _ in TURNS}

# Background color (black).
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Cell border color.
BORDER_COLOR = (93, 216, 228)

# Apple color.
APPLE_COLOR = (255, 0, 0)

# Snake color.
SNAKE_COLOR = (0, 255, 0)

# Snake movement speed (frames per second).
SPEED = 8

# Initialize the game window.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Set the game window title.
pygame.display.set_caption('Snake')

# Clock for controlling the game frame rate.
clock = pygame.time.Clock()


class GameObject:
    """Base class for all game objects."""

    def __init__(self, position=INITIAL_POSITION, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position, color=None, border=True):
        """Draws a single cell of the object."""
        if color is None:
            color = self.body_color
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        if border:
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Abstract method for drawing an object."""


class Apple(GameObject):
    """Class representing the apple."""

    def __init__(self, occupied_positions=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        if occupied_positions is None:
            occupied_positions = []
        self.position = self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Sets a random position for the apple."""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in occupied_positions:
                return position

    def draw(self):
        """Draws the apple."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Class representing the snake."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    def update_direction(self, new_direction):
        """Updates the snake's movement direction."""
        if new_direction:
            self.direction = new_direction

    def move(self):
        """Updates the snake's position."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head = (
            (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        self.last = self.positions.pop() if len(self.positions) > self.length \
            else None

    def draw(self):
        """Draws the snake."""
        self.draw_cell(self.get_head_position(), SNAKE_COLOR)

        # Erasing the last segment
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR, border=False)

    def get_head_position(self):
        """Returns the position of the snake's head."""
        return self.positions[0]

    def reset(self):
        """Resets the snake to its initial state."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Handles key presses."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key in TURN_KEYS:
                new_direction = TURNS.get((event.key, game_object.direction))
                game_object.update_direction(new_direction)


def main():
    """Main game function containing the game loop."""
    pygame.init()

    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    screen.fill(BOARD_BACKGROUND_COLOR)
    snake.draw()
    apple.draw()
    pygame.display.update()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)

        if len(snake.positions) != len(set(snake.positions)):
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.position = apple.randomize_position(snake.positions)
            apple.draw()
            snake.draw()
            pygame.display.update()

        snake.move()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
