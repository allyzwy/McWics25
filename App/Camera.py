import pygame


class Camera:
    def __init__(self, width, height, world_width, world_height):
        """
        Initialize the camera.

        Args:
            width (int): Width of the screen.
            height (int): Height of the screen.
            world_width (int): Width of the game world.
            world_height (int): Height of the game world.
        """
        self.rect = pygame.Rect(0, 0, width, height)  # Camera's viewport
        self.world_width = world_width
        self.world_height = world_height

    def apply(self, entity):
        """Convert an entity's world position to its screen position."""
        return entity.rect.move(-self.rect.x, -self.rect.y)

    def update(self, target):
        """Center the camera on the target (e.g., the player)."""
        self.rect.center = target.rect.center

        # Clamp the camera to the world boundaries
        self.rect.x = max(0, min(self.rect.x, self.world_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.world_height - self.rect.height))
