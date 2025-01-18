import pygame


class Game:
    def __init__(self):
        _ = pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.player = pygame.Rect(100, 500, 50, 50)
        self.velocity_y = 0
        self.on_ground = False
        self.gravity = 0.8

        self.platforms = [pygame.Rect(0, 550, 800, 50), pygame.Rect(300, 400, 200, 20)]

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.x -= 5
        if keys[pygame.K_RIGHT]:
            self.player.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -15

    def start(self):
        running = True
        while running:
            print(self.on_ground)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_movement()

            self.velocity_y += self.gravity
            self.player.y += self.velocity_y

            self.on_ground = False
            for platform in self.platforms:
                if self.player.colliderect(platform) and self.velocity_y > 0:
                    self.player.bottom = platform.top
                    self.velocity_y = 0
                    self.on_ground = True

            # Sky blue
            self.screen.fill((135, 206, 235))
            pygame.draw.rect(self.screen, (255, 0, 0), self.player)
            for platform in self.platforms:
                pygame.draw.rect(self.screen, (0, 255, 0), platform)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.start()
