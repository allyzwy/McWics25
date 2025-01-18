import pygame
from Entity import Entity


class Player(Entity):
    def __init__(self, x, y, width, height, world_width, world_height, image_path=None):
        """
        Initialize the player object.

        Args:
            x (int): Initial x-coordinate of the player.
            y (int): Initial y-coordinate of the player.
            width (int): Width of the player.
            height (int): Height of the player.
            world_width (int): Total width of the game world.
            world_height (int): Total height of the game world.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity_y = 0
        self.on_ground = False
        self.gravity = 0.8
        self.world_width = world_width
        self.world_height = world_height

        # Load image if provided, else None
        self.image = None
        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(
                self.image, (width, height)
            )  # Scale to fit rect

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            if self.rect.left < 0:  # Prevent moving past the left edge of the world
                self.rect.left = 0
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            if (
                self.rect.right > self.world_width
            ):  # Prevent moving past the right edge of the world
                self.rect.right = self.world_width
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -15

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Prevent falling below the world height
        if self.rect.bottom > self.world_height:
            self.rect.bottom = self.world_height
            self.velocity_y = 0
            self.on_ground = True

    def check_collision(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform) and self.velocity_y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True

    def draw(self, screen, camera):
        if self.image:
            screen.blit(self.image, camera.apply(self))
        else:
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(self))
