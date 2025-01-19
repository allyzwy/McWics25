from codecs import latin_1_decode
import pygame

from BounceEffect import BounceLeft
from Player import Player
from Camera import Camera
from Platform import Platform
from Enemy import Enemy, EnemyMovement
from Lava import Lava
from Coin import Coin
from Spikes import Spikes


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
            800,
            50,
            110,
            self.world_width,
            self.world_height,
        )

        self.platforms = [
            Platform(0, 550, 2000, 50),  # Ground platform
            # Platform(300, 400, 200, 20),
            Platform(500, 500, 40, 150),
            Platform(600, 300, 200, 20),
            Platform(1200, 450, 300, 20),
        ]
        self.enemies = [
            Enemy(
                400, 500, 50, 50, EnemyMovement.HORIZONTAL, speed=3, bounds=(400, 800)
            ),
            Enemy(
                1000, 450, 50, 50, EnemyMovement.VERTICAL, speed=2, bounds=(400, 500)
            ),
        ]
        self.lava_pools = [
            Lava(820, 540, 120, 10),  # Example lava pool
        ]
        self.coins = [
            Coin(350, 500),
            Coin(750, 450),
            Coin(1300, 400),
        ]

        self.total_coins_collected = 0

        self.spike_traps = [
            Spikes(600, 540, 200, 10, num_triangles=10),  # Example spikes
            Spikes(1100, 540, 300, 10, num_triangles=15),
        ]

    def start(self, mode="standard"):

        running = True
        while running:
            delta_time = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update game objects
            self.player.update(delta_time, self.platforms)

            self.player.update_animation()
            # self.player.apply_gravity(self.platforms)
            # self.player.check_platform_collision(self.platforms)

            # Update the camera
            self.camera.update(self.player)

            # Drawing
            self.screen.fill((255, 255, 255))  # Sky blue

            self.player.draw(self.screen, self.camera)

            for platform in self.platforms:
                platform.draw(self.screen, self.camera)

            # Draw the enemy
            if mode == "standard":
                for enemy in self.enemies:
                    enemy.update()
                    if enemy.check_collision(self.player):
                        self.player.bounce_effect.start(self.player)

                    enemy.draw(self.screen, self.camera)

                # Draw lava
                for lava in self.lava_pools:
                    if lava.check_collision(self.player):
                        self.player.bounce_effect.start(self.player)
                    lava.draw(self.screen, self.camera)

                # Draw spikes and update
                for spikes in self.spike_traps:
                    spikes.draw(self.screen, self.camera)
                    if spikes.check_collision(self.player):
                        self.player.bounce_effect.start(self.player)

            # Draw coin and update coins
            for coin in self.coins:
                coin.draw(self.screen, self.camera)
                if coin.check_collision(self.player):
                    self.total_coins_collected += 1  # Update the total coin count
                    print(
                        f"Coins collected: {self.total_coins_collected}"
                    )  # Optional for debugging

            # Display total coins
            font = pygame.font.SysFont(None, 30)
            coin_text = font.render(
                f"Samu's coins: {self.total_coins_collected}", True, (0, 0, 0)
            )  # White text
            self.screen.blit(coin_text, (600, 20))  # Position text at the top-right

            pygame.display.flip()
