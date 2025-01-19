from Entity import Entity
import pygame


class Lava(Entity):
    """
    Lava is a red rectangle entity that is traversable by the player.
    If a player collides with the lava, report collision.
    """

    def __init__(self, x, y, width, height):
        """
        Initialize the Lava object.

        Args:
            x (int): X-coordinate of the lava.
            y (int): Y-coordinate of the lava.
            width (int): Width of the lava.
            height (int): Height of the lava.
        """
        super().__init__(x, y, width, height)

    def draw(self, screen, camera):
        """
        Draw the lava on the screen.

        Args:
            screen (pygame.Surface): The game screen.
            camera (Camera): The camera object for world-to-screen translation.
        """
        screen_rect = camera.apply(self)
        pygame.draw.rect(screen, (255, 0, 0), screen_rect)  # Draw red lava

    def check_collision(self, player):
        """
        Check if the player collides with the lava.

        Args:
            player (Player): The player object.

        Returns:
            bool: True if collision occurs, False otherwise.
        """
        return self.rect.colliderect(player.rect)
