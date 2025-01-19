import pygame
from BounceEffect import BounceLeft
from Entity import Entity
from enum import Enum
import os

ASSETS_PATH = os.path.join(".", "App", "assets")

STATIC_FRAME = os.path.join(ASSETS_PATH, "player", "static.PNG")
JUMP_FRAMES = [
    os.path.join(ASSETS_PATH, "player", "jump", f"{i}.PNG") for i in range(1, 9)
]
WALK_FRAMES = [
    os.path.join(ASSETS_PATH, "player", "walk", f"{i}.PNG") for i in range(1, 6)
]
HIT_FRAMES = [
    os.path.join(ASSETS_PATH, "player", "hit", f"{i}.PNG") for i in range(1, 7)
]


class PlayerState(Enum):
    STATIC = "static"
    WALK = "walk"
    JUMP = "jump"
    HIT = "hit"


class PlayerDirection(Enum):
    LEFT = "left"
    RIGHT = "right"


class Player(Entity):
    # Dictionary of animation states to image paths.
    animations = {
        PlayerState.STATIC: [STATIC_FRAME],
        PlayerState.JUMP: JUMP_FRAMES,
        PlayerState.WALK: WALK_FRAMES,
        PlayerState.HIT: HIT_FRAMES,
    }

    def __init__(self, x, y, width, height, world_width, world_height):
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

        self.width = width
        self.height = height

        # Preload and scale all animations
        self.animations = {
            state: self.load_frames(paths, (80 if state == PlayerState.HIT else height))
            for state, paths in Player.animations.items()
        }
        self.current_state = PlayerState.STATIC  # Default state
        self.current_frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 5  # How many 'ticks' before advancing animation frame

        self.direction = PlayerDirection.RIGHT  # Default direction

        # Example bounce effect (knockback or special effect)
        self.bounce_effect = BounceLeft(500, 200)

    def load_frames(self, paths, new_height):
        """
        Load and scale animation frames so heights match 'new_height' and widths scale proportionally.

        Args:
            paths (list of str): List of file paths for each animation frame.
            new_height (int): Desired new height of the frame.

        Returns:
            list of pygame.Surface: List of loaded/scaled images.
        """
        frames = [pygame.image.load(path) for path in paths]
        scaled = []
        for frame in frames:
            og_width, og_height = frame.get_size()
            new_width = int(og_width * (new_height / og_height))
            scaled_frame = pygame.transform.scale(frame, (new_width, new_height))
            scaled.append(scaled_frame)
        return scaled

    def _set_state(self, state):
        """
        Set the player's animation state, resetting frame index if the state changes.

        Args:
            state (PlayerState): The new animation state.
        """
        if state != self.current_state:
            self.current_state = state
            self.current_frame_index = 0  # Always reset to first frame on state change

    def update_animation(self):
        """
        Advances the current animation frame at a fixed rate (frame_delay).
        """
        self.frame_timer += 0.5
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(
                self.animations[self.current_state]
            )

    def update(self, delta_time, platforms):
        """
        Update the player's movement, collisions, and animation each frame.

        Args:
            delta_time (float): Time elapsed since the last frame (not used extensively here).
            platforms (list): A list of platform objects that have 'rect' attributes.
        """
        # If there is an active bounce/knockback effect, apply that logic:
        if self.bounce_effect.is_active():
            self.bounce_effect.update(delta_time)
            self._set_state(PlayerState.HIT)
            # Direction forced to right for demonstration, could also offset x here
            self.direction = PlayerDirection.RIGHT

            # If you want bounce to actually push the player, you could do something like:
            # knockback_x = self.bounce_effect.get_knockback_x()  # example method
            # self.rect.x += knockback_x
            # (Then handle collisions in X, etc.)
        else:
            # -- 1) Handle input to determine horizontal movement --
            keys = pygame.key.get_pressed()
            dx = 0

            if keys[pygame.K_LEFT]:
                dx = -5
                self.direction = PlayerDirection.LEFT
            elif keys[pygame.K_RIGHT]:
                dx = 5
                self.direction = PlayerDirection.RIGHT

            # Move horizontally first
            self.rect.x += dx

            # Check horizontal boundary collisions with world edges
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > self.world_width:
                self.rect.right = self.world_width

            # Now handle jumping:
            if keys[pygame.K_SPACE] and self.on_ground:
                self.velocity_y = -15  # Jump velocity

            # -- 2) Apply gravity and move vertically --
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

            # -- 3) Check collisions in the vertical direction --
            self.on_ground = False
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    # Check if we are falling onto the platform
                    if self.velocity_y > 0:
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.on_ground = True
                    # If we jumped into the underside of the platform
                    elif self.velocity_y < 0:
                        self.rect.top = platform.rect.bottom
                        self.velocity_y = 0

            # Ensure we don't go below the world "floor"
            if self.rect.bottom > self.world_height:
                self.rect.bottom = self.world_height
                self.velocity_y = 0
                self.on_ground = True

            # -- 4) Set the correct animation state --
            if not self.on_ground:
                self._set_state(PlayerState.JUMP)
            elif dx != 0:
                self._set_state(PlayerState.WALK)
            else:
                self._set_state(PlayerState.STATIC)

        # Update the player's animation (frame updates)
        self.update_animation()

    def draw(self, screen, camera):
        """
        Draw the player's current animation frame onto the screen.
        Flips the sprite horizontally if direction is LEFT.

        Args:
            screen (pygame.Surface): The main screen to draw onto.
            camera: A camera system that has an `apply(entity)` method which
                    returns the correct coordinates of the entity relative to the view.
        """
        current_frame = self.animations[self.current_state][self.current_frame_index]

        # Flip horizontally if facing LEFT
        if self.direction == PlayerDirection.LEFT:
            current_frame = pygame.transform.flip(current_frame, True, False)

        screen.blit(current_frame, camera.apply(self))
