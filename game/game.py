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
from data.settings import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from game.units import Unit
from game.map import Map


class Game:
    def __init__(self) -> None:
        self.screen_width: int = SCREEN_WIDTH
        self.screen_height: int = SCREEN_HEIGHT
        self.fps: int = FPS

        self.red_unit = Unit(100, 100, 1, (186, 13, 33))
        self.blue_unit = Unit(500, 500, -1, (26, 7, 190))

        self.game_map: Map | None = None

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tactical Path Game")
        clock = pygame.time.Clock()

        self.game_map = Map(
            "assets/images/Map.png",
            self.screen_width,
            self.screen_height
        )

        running: bool = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.blue_unit.move()

            self.game_map.draw(screen)
            self.blue_unit.draw(screen)

            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()