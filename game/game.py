"""
                game.py
                    Owns:
                        startup
                        loop
                        update/draw orchestration
                    Does not own:
                        unit logic
                        combat rules
                        map data
"""
import pygame
from game.units import Unit


class Game:
    def __init__(self) -> None:
        self.screen_width = 1500
        self.screen_height = 800
        self.sky_blue = (161, 255, 254)
        self.fps = 60

        self.red_team = Unit(100, 100, 1, (186, 13, 33))
        self.blue_team = Unit(500, 500, -1, (26, 7, 190))

    def draw_midline(self, surface, color=(0, 0, 0), width=1) -> None:
        y = self.screen_height // 2
        pygame.draw.line(surface, color, (0, y), (self.screen_width, y), width)

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("My Pygame Window")
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.red_team.move()
            self.blue_team.move()

            screen.fill(self.sky_blue)
            self.draw_midline(screen)
            self.red_team.draw(screen)
            self.blue_team.draw(screen)

            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()
