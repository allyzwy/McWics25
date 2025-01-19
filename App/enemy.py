import pygame
from Entity import Entity
import os
from enum import Enum


ASSETS_PATH = os.path.join(".", "App", "assets")

MOVEMENT_FRAME_PATHS = [
    os.path.join(ASSETS_PATH, "enemy", f"{i}.PNG") for i in range(1, 3)
]


class EnemyMovement(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class EnemyDirection(Enum):
    LEFT = 1
    RIGHT = -1


class Enemy(Entity):

    FRAMES = [pygame.image.load(path) for path in MOVEMENT_FRAME_PATHS]

    def __init__(
        self,
        x,
        y,
        width,
        height,
        trajectory_type=EnemyMovement.HORIZONTAL,
        speed=2,
        bounds=None,
    ):
        """
        Initialize the enemy object.

        Args:
            x (int): Starting x-coordinate.
            y (int): Starting y-coordinate.
            width (int): Width of the enemy.
            height (int): Height of the enemy.
            trajectory_type (str): The type of movement ("horizontal", "vertical")
            speed (int): Speed of the enemy's movement.
            bounds (tuple): Bounds for the movement (e.g., (min_x, max_x) for horizontal).
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.trajectory_type = trajectory_type
        self.speed = speed
        self.bounds = bounds
        self.direction = EnemyDirection.LEFT

        self.current_frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 10

        # Scale frames to match the size of rect
        Enemy.FRAMES = [
            pygame.transform.scale(frame, (self.rect.width, self.rect.height))
            for frame in Enemy.FRAMES
        ]

    def update_animation(self):
        self.frame_timer += 0.5

        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0  # Reset the timer
            self.current_frame_index = (self.current_frame_index + 1) % len(
                Enemy.FRAMES
            )

    def _reverse_direction(self):
        if self.direction == EnemyDirection.LEFT:
            self.direction = EnemyDirection.RIGHT

        elif self.direction == EnemyDirection.RIGHT:
            self.direction = EnemyDirection.LEFT

    def update(self):
        if self.trajectory_type == EnemyMovement.HORIZONTAL:
            self.rect.x += self.speed * self.direction.value
            if self.bounds:
                if self.rect.left < self.bounds[0] or self.rect.right > self.bounds[1]:
                    self._reverse_direction()

        elif self.trajectory_type == EnemyMovement.VERTICAL:
            self.rect.y += self.speed * self.direction.value
            if self.bounds:
                if self.rect.top < self.bounds[0] or self.rect.bottom > self.bounds[1]:
                    self._reverse_direction()

        self.update_animation()

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)

    def draw(self, screen, camera):
        current_frame = Enemy.FRAMES[self.current_frame_index]

        # Flip the frame if the direction is LEFT
        if self.direction == EnemyDirection.LEFT:
            current_frame = pygame.transform.flip(current_frame, True, False)

        screen.blit(current_frame, camera.apply(self))
