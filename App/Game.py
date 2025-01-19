import pygame
from Lava import Lava
from Spikes import Spikes
from Player import Player
from Camera import Camera
from Platform import Platform
from Enemy import Enemy, EnemyMovement
from Coin import Coin


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.world_width = 6000  # The width of the game world
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
            Platform(0, 550, 1900, 50),  # Ground platform
            Platform(900, 500, 50, 50),
            Platform(950, 500, 50, 50),
            Platform(950, 450, 50, 50),
            Platform(1000, 500, 50, 50),
            Platform(1000, 450, 50, 50),
            Platform(1000, 400, 50, 50),
            Platform(1300, 500, 50, 50),
            Platform(1500, 500, 50, 50),
            Platform(2000, 500, 5000, 100),  # Ground platform
        ]
        self.enemies = [
            Enemy(
                400, 500, 50, 50, EnemyMovement.HORIZONTAL, speed=2, bounds=(300, 600)
            ),
            # Enemy(
            #     1000, 450, 50, 50, EnemyMovement.VERTICAL, speed=2, bounds=(400, 500)
            # ),
        ]
        self.lava_pools = [Lava(1900, 575, 100, 25)]
        self.coins = [
            Coin(650, 500),
            Coin(1100, 200),
        ]

        self.total_coins_collected = 0

        self.spike_traps = [
            Spikes(1050, 530, 50, 20, 4),
            Spikes(1350, 530, 150, 20, 10),
        ]

        # Font and text for how to play
        self.font = pygame.font.SysFont("Comic Sans MS", 16)  # Default font, size 36
        self.text_color = (0, 0, 0)  # Black color
        self.how_to_play_text = [
            "def how_to_play():",
            '   """',
            "   1. Press the left and right arrow keys to move.",
            "   2. Press the space bar to jump.",
            "   3. Collect as many coins as you can.",
            "   4. Avoid the martlet and don't touch the lava or spikes!",
            '   """',
        ]
        self.text_rect = pygame.Rect(40, 50, 0, 0)  # Position in world coordinates

    def draw_world_text(self, screen, camera):
        """
        Draw text at a specific location in the game world.

        Args:
            screen (pygame.Surface): The game screen.
            camera (Camera): The camera object for world-to-screen translation.
        """
        y_offset = 0  # Vertical offset between text lines
        for line in self.how_to_play_text:
            # Render each line of text
            text_surface = self.font.render(line, True, self.text_color)

            # Adjust the position of the text to account for the camera
            text_position = self.text_rect.move(
                0, y_offset
            )  # Apply offset for each line

            # Apply the camera's transformation to the position directly
            screen_position = (
                text_position.x - camera.rect.x,
                text_position.y - camera.rect.y,
            )

            screen.blit(text_surface, screen_position)

            y_offset += 30  # Move down for the next line

    def start(self, mode="standard"):
        running = True
        while running:
            delta_time = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Drawing
            self.screen.fill((255, 255, 255))  # Sky blue

            # Update game objects
            self.player.update(delta_time, self.platforms, self.screen)

            self.player.update_animation()
            # self.player.apply_gravity(self.platforms)
            # self.player.check_platform_collision(self.platforms)

            # Update the camera
            self.camera.update(self.player)

            # Draw world-positioned text
            self.draw_world_text(self.screen, self.camera)

            self.player.draw(self.screen, self.camera)

            for platform in self.platforms:
                platform.draw(self.screen, self.camera)

            if mode == "standard":
                for enemy in self.enemies:
                    enemy.update()
                    if enemy.check_collision(self.player):
                        self.player.bounce_effect.start(self.player, self.screen)

                    enemy.draw(self.screen, self.camera)

                for lava in self.lava_pools:
                    if lava.check_collision(self.player):
                        self.player.bounce_effect.start(self.player, self.screen)
                    lava.draw(self.screen, self.camera)

                for spikes in self.spike_traps:
                    spikes.draw(self.screen, self.camera)
                    if spikes.check_collision(self.player):
                        self.player.bounce_effect.start(self.player, self.screen)

            for coin in self.coins:
                coin.draw(self.screen, self.camera)
                if coin.check_collision(self.player):
                    self.total_coins_collected += 1

            font = pygame.font.SysFont("Comic Sans MS", 18)
            coin_text = font.render(
                f"Samu's coins: {self.total_coins_collected}", True, (0, 0, 0)
            )  # White text
            self.screen.blit(coin_text, (630, 20))  # Position text at the top-right

            pygame.display.flip()
