import pygame
from player import Player
from camera import Camera
from entity import Entity
from enemy import Enemy, MOVEMENT


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        # Define world size
        self.world_width = 2000  # The width of the game world
        self.world_height = 600  # The height of the game world

        # Initialize player, platforms, and camera
        self.player = Player(100, 500, 50, 50)
        self.platforms = [
            Entity(0, 550, 2000, 50),  # Ground platform
            Entity(300, 400, 200, 20),
            Entity(600, 300, 200, 20),
            Entity(1200, 450, 300, 20),
        ]
        self.camera = Camera(800, 600, self.world_width, self.world_height)
        self.enemies = [
            Enemy(400, 500, 50, 50, MOVEMENT.HORIZONTAL, speed=3, bounds=(400, 800)),
            Enemy(1000, 450, 50, 50, MOVEMENT.VERTICAL, speed=2, bounds=(400, 500)),
        ]


    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update game objects
            self.player.move()
            self.player.apply_gravity()
            self.player.check_collision(self.platforms)

            # Update enemies
            for enemy in self.enemies:
                enemy.update()
                if enemy.check_collision(self.player):
                    print("Player hit by an enemy!")  # Replace with actual action logic

            # Update the camera
            self.camera.update(self.player)

            # Drawing
            self.screen.fill((135, 206, 235))  # Sky blue
            for platform in self.platforms:
                screen_rect = self.camera.apply(platform)
                pygame.draw.rect(
                    self.screen, (0, 255, 0), screen_rect
                )  # Draw platforms

            # Draw the player
            pygame.draw.rect(self.screen, (255, 0, 0), self.camera.apply(self.player))

            # Draw the enemy
            for enemy in self.enemies:
                pygame.draw.rect(self.screen, (255, 165, 0), self.camera.apply(enemy))  # Orange color

            pygame.display.flip()
            self.clock.tick(60)
