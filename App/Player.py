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
    os.path.join(ASSETS_PATH, "player", "hit", f"{i}.PNG") for i in range(1, 8)
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

        # Load animations
        self.animations = {
            state: self.load_frames(paths, height)
            for state, paths in Player.animations.items()
        }
        self.current_state = PlayerState.STATIC  # Default state
        self.current_frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 5  # Frames per animation update

        self.direction = PlayerDirection.RIGHT  # Default direction

        self.bounce_effect = BounceLeft(500, 200)

    def load_frames(self, paths, new_height):
        """
        Load and scale animation frames.

        Args:
            paths (list of str): List of file paths to frames.
            width (int): Width to scale the frames to.
            height (int): Height to scale the frames to.

        Returns:
            list: List of loaded and scaled pygame surfaces.
        """
        frames = [pygame.image.load(path) for path in paths]
        new_width = int(self.width * (new_height / self.height))
        print(new_width, new_height)
        return [
            pygame.transform.scale(frame, (new_width, new_height)) for frame in frames
        ]

    def _set_state(self, state):
        """
        Set the player's animation state.

        Args:
            state (PlayerState): The new animation state.
        """

        if state != self.current_state:
            self.current_state = state
            self.current_frame_index = 0  # Reset to the first frame

    def update_animation(self):
        """
        Update the current frame of the animation based on the current state.
        """
        self.frame_timer += 0.5
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(
                self.animations[self.current_state]
            )

    def update(self, delta_time):

        if self.bounce_effect.is_active():
            self.bounce_effect.update(delta_time)
            self._set_state(PlayerState.HIT)
            self.direction = PlayerDirection.RIGHT

        else:
            keys = pygame.key.get_pressed()
            moving = False

            # Handle left and right movement
            if keys[pygame.K_LEFT]:
                self.rect.x -= 5
                if self.rect.left < 0:
                    self.rect.left = 0
                moving = True
                self.direction = PlayerDirection.LEFT

            if keys[pygame.K_RIGHT]:
                self.rect.x += 5
                if self.rect.right > self.world_width:
                    self.rect.right = self.world_width
                moving = True
                self.direction = PlayerDirection.RIGHT

            # Handle jumping
            if keys[pygame.K_SPACE] and self.on_ground:
                self.velocity_y = -15
                self._set_state(PlayerState.JUMP)

            # State transitions
            if not self.on_ground:
                self._set_state(PlayerState.JUMP)  # Airborne (jumping or falling)
            elif moving:
                self._set_state(PlayerState.WALK)  # Walking on ground
            else:
                self._set_state(PlayerState.STATIC)  # Standing idle

        self.update_animation()

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
            if (
                self.rect.colliderect(platform)
                and self.velocity_y >= 0
                and self.current_state != PlayerState.HIT
            ):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True

    def draw(self, screen, camera):
        current_frame = self.animations[self.current_state][self.current_frame_index]

        # Flip the frame if the direction is LEFT
        if self.direction == PlayerDirection.LEFT:
            current_frame = pygame.transform.flip(current_frame, True, False)

        screen.blit(current_frame, camera.apply(self))
