import os
import pygame
from Entity import Entity
from Camera import Camera
from OnHitEffect import OnHitEffect
from config import ASSETS_PATH

ON_HIT_IMAGE_PATH = os.path.join(ASSETS_PATH, "on_hit", "damage.PNG")


class BounceLeft(OnHitEffect):
    """
    On-hit effect that bounces the player in a parabolic trajectory and shows an image.
    """

    def __init__(self, bounce_distance=100, bounce_height=50, duration=1.0):
        """
        Initialize the Bounce effect.

        Args:
            bounce_distance (int): Total horizontal distance of the bounce.
            bounce_height (int): Maximum height of the bounce.
            duration (float): Total duration of the bounce in seconds.
        """
        self.bounce_distance = bounce_distance
        self.bounce_height = bounce_height
        self.duration = duration
        self.elapsed_time = 0  # Track progress over time
        self.active = False  # Indicates if the effect is active

        # Load the on-hit image
        self.on_hit_image = pygame.transform.scale(
            pygame.image.load(ON_HIT_IMAGE_PATH), (60, 60)
        )

        self.animation_time = 10
        self.current_animation_time = 0
        self.animation_active = False

    def start(self, player):
        """
        Start the bounce effect.

        Args:
            player: The player object to apply the bounce to.
        """
        self.active = True
        self.elapsed_time = 0
        self.player = player
        self.start_pos = player.rect.x, player.rect.y
        self.direction = -1  # Direction of the bounce (left in this case)

        self.animation_active = True

    def update(self, delta_time, screen, camera: Camera):
        """
        Update the bounce effect and display the on-hit image.

        Args:
            delta_time (float): Time elapsed since the last frame, in seconds.
            screen (pygame.Surface): The surface to render the effect.
        """
        if not self.active:
            return

        self.elapsed_time += delta_time
        t = self.elapsed_time / self.duration

        if t >= 1.0:
            # End the bounce
            self.active = False
            return

        # Calculate parabolic trajectory
        horizontal_offset = self.direction * self.bounce_distance * t
        vertical_offset = -4 * self.bounce_height * (t - 0.5) ** 2 + self.bounce_height

        # Update player's position
        self.player.rect.x = self.start_pos[0] + horizontal_offset
        self.player.rect.y = self.start_pos[1] - vertical_offset

        if self.animation_active:
            on_hit_pos = (
                self.start_pos[0] - self.on_hit_image.get_width() // 2,
                self.start_pos[1] - self.on_hit_image.get_height(),
            )

            on_hit_rect = Entity(
                on_hit_pos[0],
                on_hit_pos[1],
                self.on_hit_image.get_width(),
                self.on_hit_image.get_height(),
            )

            on_hit_screen_rect = camera.apply(on_hit_rect)

            screen.blit(self.on_hit_image, (on_hit_screen_rect.x, on_hit_screen_rect.y))

            self.current_animation_time += 1
            self.current_animation_time += 1

            if self.current_animation_time == self.animation_time:
                self.animation_active = False
                self.current_animation_time = 0

    def is_active(self):
        """
        Check if the bounce effect is still active.
        """
        return self.active
