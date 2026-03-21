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
from data.settings import FPS
from game.units import Unit


class Game:
    def __init__(self) -> None:
        self.screen_width: int = 1500
        self.screen_height: int = 800
        self.fps = FPS
        self.test_map: str = "assets/images/test_map.png"

        self.red_team = Unit(100, 100, 1, (186, 13, 33))
        self.blue_team = Unit(500, 500, -1, (26, 7, 190))

    def draw_midline(self, surface, color: tuple[int, int, int]=(0, 0, 0), width: int  =1) -> None:
        y: int = self.screen_height // 2
        pygame.draw.line(surface, color, (0, y), (self.screen_width, y), width)

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tactical Path Game")
        test_map_bg = pygame.image.load(self.test_map).convert_alpha()
        test_map_bg = pygame.transform.scale(test_map_bg, (self.screen_width, self.screen_height))

        clock = pygame.time.Clock()

        running: bool = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.red_team.move()
            self.blue_team.move()

            screen.blit(test_map_bg, (0, 0))

            self.draw_midline(screen)
            self.red_team.draw(screen)
            self.blue_team.draw(screen)


            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()
