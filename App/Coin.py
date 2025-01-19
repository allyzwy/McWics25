from Entity import Entity
import pygame


class Coin(Entity):
    """
    Coins are collectible items placed at specific locations in the game.
    When a player collects a coin, it disappears, and the total coin count is updated.
    """

    def __init__(self, x, y, width=20, height=20):
        """
        Initialize the Coin object.

        Args:
            x (int): X-coordinate of the coin.
            y (int): Y-coordinate of the coin.
            width (int): Width of the coin.
            height (int): Height of the coin.
        """
        super().__init__(x, y, width, height)
        self.collected = False  # Tracks if the coin has been collected

    def draw(self, screen, camera):
        """
        Draw the coin on the screen.

        Args:
            screen (pygame.Surface): The game screen.
            camera (Camera): The camera object for world-to-screen translation.
        """
        if not self.collected:
            screen_rect = camera.apply(self)
            pygame.draw.ellipse(screen, (255, 215, 0), screen_rect)  # Gold color

    def check_collision(self, player):
        """
        Check if the player collides with the coin.

        Args:
            player (Player): The player object.

        Returns:
            bool: True if collision occurs, False otherwise.
        """
        if not self.collected and self.rect.colliderect(player.rect):
            self.collected = True
            return True
        return False
