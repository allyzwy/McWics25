from Entity import Entity
from Camera import Camera
import pygame


class Platform(Entity):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color_fill = (255, 255, 255)  # Default fill color (white)
        self.color_outline = (0, 0, 0)  # Default outline color (black)

    def draw(self, screen, camera: Camera):
        """
        Draw the platform as a rectangle with a black outline and white filling.

        Args:
            screen: The pygame surface to draw on.
        """

        screen_rect = camera.apply(self)
        pygame.draw.rect(screen, self.color_fill, screen_rect)
        pygame.draw.rect(screen, self.color_outline, screen_rect, 2)
