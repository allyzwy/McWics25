import os

import pygame

from Player import Player
from Camera import Camera
from Platform import Platform
from Enemy import Enemy, MOVEMENT

PLAYER_IMAGE_PATH = os.path.join(".", "App", "assets", "player", "static.png")


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.world_width = 2000  # The width of the game world
        self.world_height = 600  # The height of the game world

        self.camera = Camera(800, 600, self.world_width, self.world_height)

        self.player = Player(
            100,
            500,
            100,
            100,
            self.world_width,
            self.world_height,
            image_path=PLAYER_IMAGE_PATH,
        )
        self.platforms = [
            Platform(0, 550, 2000, 50),  # Ground platform
            Platform(300, 400, 200, 20),
            Platform(600, 300, 200, 20),
            Platform(1200, 450, 300, 20),
        ]
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
            self.screen.fill((255, 255, 255))  # Sky blue
            for platform in self.platforms:
                platform.draw(self.screen, self.camera)

            self.player.draw(self.screen, self.camera)

            # Draw the enemy
            for enemy in self.enemies:
                pygame.draw.rect(
                    self.screen, (255, 165, 0), self.camera.apply(enemy)
                )  # Orange color

            pygame.display.flip()
            self.clock.tick(60)
