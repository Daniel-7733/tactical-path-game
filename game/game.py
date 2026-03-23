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
from pygame import Surface
from pygame.time import Clock

from data.settings import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from game.units import Unit
from game.map import Map


class Game:
    """This class implements game logic"""
    def __init__(self) -> None:
        """
        Initialize game class
        :return: None
        """
        # Initializing the screen size
        self.screen_width: int = SCREEN_WIDTH
        self.screen_height: int = SCREEN_HEIGHT
        self.fps: int = FPS

        # Initializing units
        self.red_unit = Unit(100, 100, 1, (186, 13, 33))
        self.blue_unit = Unit(500, 470, -1, (26, 7, 190))

        # Initializing the Map class
        self.game_map: Map | None = None

    def run(self) -> None:
        """
        Main game loop
        :return: None
        """
        pygame.init()
        screen: Surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tactical Path Game")
        clock: Clock = pygame.time.Clock()

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

            self.blue_unit.move(self.game_map)

            # draw
            self.game_map.draw(screen)  # 1. draw background map first
            self.game_map.draw_grid_debug(screen)  # 2. draw debug grid on top
            self.blue_unit.draw(screen)  # 3. draw units on top

            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()