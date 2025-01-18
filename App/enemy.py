class MOVEMENT(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Enemy(Entity):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        trajectory_type=MOVEMENT.HORIZONTAL,
        speed=2,
        bounds=None,
    ):
        """
        Initialize the enemy object.

        Args:
            x (int): Starting x-coordinate.
            y (int): Starting y-coordinate.
            width (int): Width of the enemy.
            height (int): Height of the enemy.
            trajectory_type (str): The type of movement ("horizontal", "vertical")
            speed (int): Speed of the enemy's movement.
            bounds (tuple): Bounds for the movement (e.g., (min_x, max_x) for horizontal).
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.trajectory_type = trajectory_type
        self.speed = speed
        self.bounds = bounds
        self.direction = 1  # 1 for forward/right/down, -1 for backward/left/up
        self.angle = 0  # For circular movement (optional)
