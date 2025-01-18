import pygame
from entity import Entity
from enum import Enum

class MOVEMENT(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class Enemy(Entity):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        trajectory_type=MOVEMENT.HORIZONTAL,
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
        self.direction = 1  # 1 for forward/right/down, -1 for backward/left/up


    def update(self):
        """Update the enemy's position based on its trajectory."""
        if self.trajectory_type == MOVEMENT.HORIZONTAL:
            self.rect.x += self.speed * self.direction
            if self.bounds:
                if self.rect.left < self.bounds[0] or self.rect.right > self.bounds[1]:
                    self.direction *= -1  # Reverse direction

        elif self.trajectory_type == MOVEMENT.VERTICAL:
            self.rect.y += self.speed * self.direction
            if self.bounds:
                if self.rect.top < self.bounds[0] or self.rect.bottom > self.bounds[1]:
                    self.direction *= -1  # Reverse direction


    def check_collision(self, player):
        """
        Check if the enemy collides with the player.

        Args:
            player (Player): The player object.

        Returns:
            bool: True if collision occurs, False otherwise.
        """
        return self.rect.colliderect(player.rect)