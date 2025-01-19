import pygame


class Flag:
    def __init__(self, x, y, width, height, image_path):
        """
        Initialize the flag object.

        Args:
            x (int): The x-coordinate of the flag.
            y (int): The y-coordinate of the flag.
            width (int): The width of the flag.
            height (int): The height of the flag.
            image_path (str): Path to the flag image.
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))  # Resize flag
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen, camera):
        """
        Draw the flag on the screen.

        Args:
            screen (pygame.Surface): The game screen.
            camera (Camera): The camera object for world-to-screen translation.
        """
        screen.blit(self.image, camera.apply(self.rect))
