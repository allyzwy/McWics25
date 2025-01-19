import pygame


class Entity:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)  # World position

    def draw(self, screen, camera):
        """Draw the entity on the screen relative to the camera."""
        screen_rect = camera.apply(self)  # Convert world to screen position
        pygame.draw.rect(screen, (255, 0, 0), screen_rect)
