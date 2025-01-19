from os import walk
import pygame
from Lava import Lava
from Spikes import Spikes
from Player import Player
from Camera import Camera
from Platform import Platform
from Enemy import Enemy, EnemyMovement
from Coin import Coin
from Flag import Flag


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.world_width = 6000  # The width of the game world
        self.world_height = 600  # The height of the game world

        self.camera = Camera(800, 600, self.world_width, self.world_height)

        self.player = Player(
            3900,
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
            Platform(2300, 375, 50, 50),
            Platform(2300, 375, 50, 50),
            Platform(2350, 375, 50, 50),
            Platform(2400, 375, 50, 50),
            Platform(2550, 325, 50, 50),
            Platform(2600, 325, 50, 50),
            Platform(2800, 255, 50, 50),
            Platform(3000, 300, 50, 200),
            Platform(3250, 350, 50, 150),
            Platform(3500, 400, 50, 100),
            Platform(4000, 450, 50, 50),
            Platform(4050, 450, 50, 50),
            Platform(4100, 450, 50, 50),
            Platform(4150, 450, 50, 50),
            Platform(4200, 450, 50, 50),
            Platform(4250, 450, 50, 50),
            Platform(4300, 450, 50, 50),
            Platform(4350, 450, 50, 50),
            Platform(4400, 450, 50, 50),
            Platform(4450, 450, 50, 50),
        ]
        self.enemies = [
            Enemy(
                400, 500, 50, 50, EnemyMovement.HORIZONTAL, speed=2, bounds=(300, 600)
            ),
            Enemy(
                2000,
                450,
                50,
                50,
                EnemyMovement.HORIZONTAL,
                speed=7,
                bounds=(2000, 2700),
            ),
            Enemy(
                3050,
                450,
                50,
                50,
                EnemyMovement.HORIZONTAL,
                speed=4,
                bounds=(3050, 3250),
            ),
            Enemy(
                3300,
                450,
                50,
                50,
                EnemyMovement.HORIZONTAL,
                speed=6,
                bounds=(3300, 3500),
            ),
            Enemy(
                4000,
                400,
                50,
                50,
                EnemyMovement.HORIZONTAL,
                speed=5,
                bounds=(4000, 4200),
            ),
            Enemy(
                4300,
                400,
                50,
                50,
                EnemyMovement.HORIZONTAL,
                speed=4,
                bounds=(4300, 4500),
            ),
        ]
        self.lava_pools = [
            Lava(1900, 575, 100, 25),
        ]
        self.coins = [
            Coin(650, 500),
            Coin(1100, 200),
            Coin(2800, 200),
            Coin(3125, 170),
            Coin(3375, 230),
        ]

        self.total_coins_collected = 0

        self.spike_traps = [
            Spikes(1050, 530, 50, 20, 4),
            Spikes(1350, 530, 150, 20, 10),
            Spikes(2550, 305, 30, 20, 3),
            Spikes(3620, 480, 100, 20, 5),
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

        # Load background music
        pygame.mixer.music.load("App/Sounds/Cute_Circus.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0)  # Play music indefinitely

        # Load sound effects for collision events
        self.lava_sound = pygame.mixer.Sound("App/Sounds/windows_startup.mp3")
        self.enemy_sound = pygame.mixer.Sound("App/Sounds/enemy_collide.mp3")
        self.spike_sound = pygame.mixer.Sound("App/Sounds/spikes_collide.mp3")
        self.coin_sound = pygame.mixer.Sound("App/Sounds/coin.mp3")
        self.resume_music = False  # Flag to track music resumption

        # Load flag
        self.flag = Flag(4000, 150, 70, 350, "App/assets/ending/samu_flag.png")

    def _end_game_sequence(self):
        """
        Gradually dims the screen to black and displays "FIN!"
        and the number of coins collected out of the total.
        """
        fade_surface = pygame.Surface(self.screen.get_size())
        fade_surface.fill((0, 0, 0))

        # We'll do a simple fade up to alpha=255
        for alpha in range(0, 256, 5):
            # Re-draw the last frame (so the current scene is visible under the fade)
            self.screen.blit(self.screen, (0, 0))

            # Set the alpha (opacity) of the fade overlay
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(60)

        # Once fully faded, show final text
        self.screen.fill((0, 0, 0))

        # Display the "FIN!" text
        font = pygame.font.SysFont("Comic Sans MS", 48)
        fin_text = font.render("FIN!", True, (255, 255, 255))
        fin_rect = fin_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(fin_text, fin_rect)

        # Display the coin summary
        coin_summary_text = font.render(
            f"Coins: {self.total_coins_collected}/{len(self.coins)}",
            True,
            (255, 255, 255),
        )
        coin_summary_rect = coin_summary_text.get_rect(
            center=(self.screen.get_width() // 2, 300)
        )
        self.screen.blit(coin_summary_text, coin_summary_rect)

        pygame.display.flip()

        pygame.time.wait(30000)  # 3-second pause

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

            self.screen.fill((255, 255, 255))

            self.player.update(delta_time, self.platforms, self.screen, self.camera)

            self.player.update_animation()

            self.camera.update(self.player)

            self.draw_world_text(self.screen, self.camera)

            self.player.draw(self.screen, self.camera)

            for platform in self.platforms:
                platform.draw(self.screen, self.camera)

            for enemy in self.enemies:
                enemy.update()
                if enemy.check_collision(self.player):
                    self.enemy_sound.play()
                    self.player.bounce_effect.start(self.player)
                enemy.draw(self.screen, self.camera)

            for lava in self.lava_pools:
                lava.draw(self.screen, self.camera)
                if lava.check_collision(self.player):
                    self.player.bounce_effect.start(
                        self.player,
                    )
                    if (
                        not self.lava_sound.get_num_channels()
                    ):  # Play sound only if not already playing
                        pygame.mixer.music.pause()  # Pause the background music
                        self.lava_sound.play()
                        self.resume_music = True  # Set flag to resume music

            if self.resume_music and not pygame.mixer.get_busy():
                pygame.mixer.music.unpause()
                self.resume_music = False

            for spikes in self.spike_traps:
                spikes.draw(self.screen, self.camera)
                if spikes.check_collision(self.player):
                    self.spike_sound.play()
                    self.player.bounce_effect.start(
                        self.player,
                    )

            for coin in self.coins:
                coin.draw(self.screen, self.camera)
                if coin.check_collision(self.player):
                    self.total_coins_collected += 1
                    self.coin_sound.play()

            font = pygame.font.SysFont("Comic Sans MS", 18)
            coin_text = font.render(
                f"Samu's coins: {self.total_coins_collected}", True, (0, 0, 0)
            )  # White text
            self.screen.blit(coin_text, (630, 20))  # Position text at the top-right

            # Draw the flag
            self.flag.draw(self.screen, self.camera)

            # Check collision with the flag
            if self.player.rect.colliderect(self.flag.rect):
                self._end_game_sequence()
                running = False

            pygame.display.flip()
