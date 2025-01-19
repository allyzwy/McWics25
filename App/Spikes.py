from Entity import Entity
from enum import Enum
import pygame
from enum import Enum


class SpikesMode(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class SpikesDirection(Enum):
    LEFT = 1
    RIGHT = 2


class Spikes(Entity):
    """
    Spikes are a series of triangles that are traversable by the player.
    If a player collides with the spikes, report the collision.
    """

    def __init__(self, x, y, width, height, num_triangles=5):
        """
        Initialize the Spikes object.

        Args:
            x (int): X-coordinate of the spikes.
            y (int): Y-coordinate of the spikes.
            width (int): Width of the spikes.
            height (int): Height of the spikes.
            num_triangles (int): Number of triangles to draw within the spike area.
        """
        super().__init__(x, y, width, height)
        self.num_triangles = num_triangles
        # self.mode =
        # self.direction =

    def draw(self, screen, camera):
        """
        Draw the spikes on the screen.

        Args:
            screen (pygame.Surface): The game screen.
            camera (Camera): The camera object for world-to-screen translation.
        """
        screen_rect = camera.apply(self)

        # Calculate triangle width based on the total width of the spikes
        triangle_width = self.rect.width / self.num_triangles
        for i in range(self.num_triangles):
            # Calculate the points of each triangle
            base_x = screen_rect.x + i * triangle_width
            triangle_points = [
                (base_x, screen_rect.y + screen_rect.height),  # Bottom-left corner
                (base_x + triangle_width / 2, screen_rect.y),  # Tip of the triangle
                (
                    base_x + triangle_width,
                    screen_rect.y + screen_rect.height,
                ),  # Bottom-right corner
            ]
            pygame.draw.polygon(
                screen, (255, 0, 0), triangle_points
            )  # Draw red triangle

    def check_collision(self, player):
        """
        Check if the player collides with the spikes.

        Args:
            player (Player): The player object.

        Returns:
            bool: True if collision occurs, False otherwise.
        """
        return self.rect.colliderect(player.rect)
