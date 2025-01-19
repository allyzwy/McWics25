from OnHitEffect import OnHitEffect


class BounceLeft(OnHitEffect):
    """
    On-hit effect that bounces the player in a parabolic trajectory.
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

    def start(self, player):
        """
        Start the bounce effect.

        Args:
            player: The player object to apply the bounce to.
            direction (int): Direction of the bounce (-1 for left, 1 for right).
        """
        self.active = True
        self.elapsed_time = 0
        self.player = player
        self.start_pos = player.rect.x, player.rect.y
        self.direction = -1

    def update(self, delta_time):
        """
        Update the bounce effect.

        Args:
            delta_time (float): Time elapsed since the last frame, in seconds.
        """
        if not self.active:
            return

        self.elapsed_time += delta_time
        t = self.elapsed_time / self.duration

        if t >= 1.0:
            # End the bounce
            self.active = False
            return

        # Parabolic trajectory
        horizontal_offset = self.direction * self.bounce_distance * t
        vertical_offset = -4 * self.bounce_height * (t - 0.5) ** 2 + self.bounce_height

        self.player.rect.x = self.start_pos[0] + horizontal_offset
        self.player.rect.y = self.start_pos[1] - vertical_offset

    def is_active(self):
        """
        Check if the bounce effect is still active.
        """
        return self.active
