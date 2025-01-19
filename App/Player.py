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

        # Horizontal & vertical velocities
        self.velocity_x = 0
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

        # Example bounce/knockback effect class
        self.bounce_effect = BounceLeft(500, 200)

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
        Update player's movement, collisions, and animation in a single method.
        This handles normal input as well as bounce/knockback arcs.
        """
        # --------------------
        # 1) Check Bounce Effect
        # --------------------
        if self.bounce_effect.is_active():
            self.bounce_effect.update(delta_time)
            self._set_state(PlayerState.HIT)
            if not self.bounce_effect.is_active():
                self._set_state(PlayerState.STATIC)

            # Example logic: use velocity_x, velocity_y from bounce
            # Let's say bounce gives a "parabolic" knockback to the left
            # You can tweak these values or read them from bounce_effect's logic
            self.velocity_x = -8  # knockback to the left
            # If you want an upward initial kick:
            if self.on_ground:
                self.velocity_y = -15

            # Force direction to left (you can do right if you want)
            self.direction = PlayerDirection.LEFT

        else:
            # --------------------
            # 2) Normal Input
            # --------------------
            keys = pygame.key.get_pressed()

            # Reset horizontal velocity each frame (unless you want momentum)
            self.velocity_x = 0

            if keys[pygame.K_LEFT]:
                self.velocity_x = -5
                self.direction = PlayerDirection.LEFT
            elif keys[pygame.K_RIGHT]:
                self.velocity_x = 5
                self.direction = PlayerDirection.RIGHT

            if keys[pygame.K_SPACE] and self.on_ground:
                self.velocity_y = -15

        # ----------------------------
        # 3) Move and Collision in X
        # ----------------------------
        self.rect.x += self.velocity_x

        # World boundary check (horizontal)
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.world_width:
            self.rect.right = self.world_width

        # Check horizontal collisions
        if platforms:
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    # Moving right, push player out on the left side
                    if self.velocity_x > 0:
                        self.rect.right = platform.rect.left
                    # Moving left, push player out on the right side
                    elif self.velocity_x < 0:
                        self.rect.left = platform.rect.right

        # --------------------------------
        # 4) Move and Collision in Y
        # --------------------------------
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Reset on_ground until collisions prove otherwise
        self.on_ground = False

        # Check vertical collisions
        if platforms:
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

        # Check world floor
        if self.rect.bottom > self.world_height:
            self.rect.bottom = self.world_height
            self.velocity_y = 0
            self.on_ground = True

        # --------------------
        # 5) State & Animation
        # --------------------
        if self.current_state != PlayerState.HIT:
            # If we're in HIT state, we keep it until bounce_effect ends
            if not self.on_ground:
                self._set_state(PlayerState.JUMP)
            elif self.velocity_x != 0:
                self._set_state(PlayerState.WALK)
            else:
                self._set_state(PlayerState.STATIC)

        self.update_animation()

    def draw(self, screen, camera):
        current_frame = self.animations[self.current_state][self.current_frame_index]

        if (
            self.direction == PlayerDirection.LEFT
            and self.current_state == PlayerState.HIT
        ):
            print("here")
            current_frame = pygame.transform.flip(current_frame, True, False)

        # Flip if facing LEFT
        elif self.direction == PlayerDirection.LEFT:
            current_frame = pygame.transform.flip(current_frame, True, False)

        screen.blit(current_frame, camera.apply(self))
