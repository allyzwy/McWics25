import pygame
from player import Player


class Game:
    def __init__(self):
        _ = pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.player = Player(100, 500, 50, 50)
        self.platforms = [pygame.Rect(0, 550, 800, 50), pygame.Rect(300, 400, 200, 20)]

    def start(self):
        running = True
        while running:
            print(self.player.on_ground)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.player.move()
            self.player.apply_gravity()
            self.player.check_collision(self.platforms)

            # Drawing
            self.screen.fill((135, 206, 235))  # Sky blue
            pygame.draw.rect(self.screen, (255, 0, 0), self.player.rect)
            for platform in self.platforms:
                pygame.draw.rect(self.screen, (0, 255, 0), platform)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.start()
