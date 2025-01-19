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
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity_y = 0
        self.on_ground = False
        self.gravity = 0.8
        self.world_width = world_width
        self.world_height = world_height

        self.width = width
        self.height = height

        # Preload and scale animations
        self.animations = {
            state: self.load_frames(paths, (80 if state == PlayerState.HIT else height))
            for state, paths in Player.animations.items()
        }
        self.current_state = PlayerState.STATIC
        self.current_frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 5

        self.direction = PlayerDirection.RIGHT
        self.bounce_effect = BounceLeft(500, 200)  # Example effect

    def load_frames(self, paths, new_height):
        frames = [pygame.image.load(path) for path in paths]
        scaled = []
        for frame in frames:
            og_width, og_height = frame.get_size()
            new_width = int(og_width * (new_height / og_height))
            scaled_frame = pygame.transform.scale(frame, (new_width, new_height))
            scaled.append(scaled_frame)
        return scaled

    def _set_state(self, state):
        if state != self.current_state:
            self.current_state = state
            self.current_frame_index = 0  # Reset frame

    def update_animation(self):
        self.frame_timer += 0.5
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(
                self.animations[self.current_state]
            )

    def update(self, delta_time, platforms):
        """
        Update player's movement, collisions (horizontal and vertical),
        and animation in a single method to avoid sinking or passing through.
        """
        if self.bounce_effect.is_active():
            # Bounce/knockback logic
            self.bounce_effect.update(delta_time)
            self._set_state(PlayerState.HIT)
            self.direction = PlayerDirection.RIGHT
            # If you want to apply knockback, do so before collision checks:
            #   knockback_x = some function of bounce_effect...
            #   self.rect.x += knockback_x
            #   (Then do collisions as normal.)
        else:
            # ---------------------------
            # 1) Handle Horizontal Input
            # ---------------------------
            dx = 0
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                dx = -5
                self.direction = PlayerDirection.LEFT
            elif keys[pygame.K_RIGHT]:
                dx = 5
                self.direction = PlayerDirection.RIGHT

            # Move horizontally
            self.rect.x += dx

            # World boundary check (horizontal)
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > self.world_width:
                self.rect.right = self.world_width

            # -------------------------------
            # 2) Check Horizontal Collisions
            # -------------------------------
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    # If moving right, push out on left side
                    if dx > 0:
                        self.rect.right = platform.rect.left
                    # If moving left, push out on right side
                    elif dx < 0:
                        self.rect.left = platform.rect.right

            # --------------------
            # 3) Vertical Movement
            # --------------------
            if keys[pygame.K_SPACE] and self.on_ground:
                self.velocity_y = -15

            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

            # -------------------------------
            # 4) Check Vertical Collisions
            # -------------------------------
            self.on_ground = False
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    # Falling down onto the platform
                    if self.velocity_y > 0:
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.on_ground = True
                    # Jumping up into the underside
                    elif self.velocity_y < 0:
                        self.rect.top = platform.rect.bottom
                        self.velocity_y = 0

            # World boundary (floor)
            if self.rect.bottom > self.world_height:
                self.rect.bottom = self.world_height
                self.velocity_y = 0
                self.on_ground = True

            # --------------------
            # 5) Update State
            # --------------------
            if not self.on_ground:
                self._set_state(PlayerState.JUMP)
            elif dx != 0:
                self._set_state(PlayerState.WALK)
            else:
                self._set_state(PlayerState.STATIC)

        # --------------------
        # 6) Animation
        # --------------------
        self.update_animation()

    def draw(self, screen, camera):
        current_frame = self.animations[self.current_state][self.current_frame_index]

        # Flip if facing LEFT
        if self.direction == PlayerDirection.LEFT:
            current_frame = pygame.transform.flip(current_frame, True, False)

        screen.blit(current_frame, camera.apply(self))
