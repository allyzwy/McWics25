from Entity import Entity
import os
import pygame

ASSETS_PATH = os.path.join(".", "App", "assets")

COIN_IMAGE_PATH = os.path.join(ASSETS_PATH, "coin", "coin.PNG")


class Coin(Entity):
    """
    Coins are collectible items placed at specific locations in the game.
    When a player collects a coin, it disappears, and the total coin count is updated.
    """

    def __init__(self, x, y, width=35, height=35):
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
        self.image = pygame.transform.scale(
            pygame.image.load(COIN_IMAGE_PATH), (self.rect.width, self.rect.height)
        )

    def draw(self, screen, camera):
        """
        Draw the coin on the screen.

        Args:
            screen (pygame.Surface): The game screen.
            camera (Camera): The camera object for world-to-screen translation.
        """
        if not self.collected:
            screen.blit(self.image, camera.apply(self))

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
