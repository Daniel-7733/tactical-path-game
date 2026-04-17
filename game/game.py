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
from game.path_manager import PathManager
from game.units import Unit
from game.map import Map
from game import movement

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

        # Initializing font
        self.blackOpsOne_font_path = "assets/fonts/BlackOpsOne-Regular.ttf"


        # Initializing units
        self.red_rifleman = Unit(100, 100, "red", "rifleman", 100, 2, 80, 10)
        self.blue_rifleman = Unit(381, 380, "blue", "rifleman", 100, 2, 80, 10)
        # self.blue_rifleman.set_path(
        #     [
        #         (380, 396),
        #         (902, 396),
        #         (902, 324),
        #         (1031, 324),
        #         (1031, 234),
        #         (1230, 234),
        #         (1230, 304),
        #         (1335, 304),
        #     ]
        # )
        # Initializing the Map class
        self.game_map: Map | None = None
        self.path_manager = PathManager()

    def run(self) -> None:
        """
        Main game loop
        :return: None
        """
        pygame.init()
        screen: Surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tactical Path Game")
        clock: Clock = pygame.time.Clock()

        font = pygame.font.Font(self.blackOpsOne_font_path, 40)

        self.game_map = Map(
            "assets/images/MapSimpleLandRiver.png", # "assets/images/Map.png"
            self.screen_width,
            self.screen_height
        )

        running: bool = True

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.path_manager.handle_mouse_down(event.pos, event.button)

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.path_manager.handle_mouse_up(event.pos, event.button)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.blue_rifleman.shoot()

                    elif event.key == pygame.K_SPACE:
                        print("Space pressed")
                        waypoints = self.path_manager.lines_to_waypoints()

                        if waypoints:
                            self.blue_rifleman.set_path(waypoints)
                            self.blue_rifleman.allow_movement()
                            self.path_manager.clear()

                    elif event.key == pygame.K_c:
                        print("C pressed")
                        self.path_manager.clear()



            self.blue_rifleman.update_bullets()
            # draw
            self.game_map.draw(screen)  # 1. draw background map first
            self.path_manager.draw(screen)
            # self.game_map.draw_grid_debug(screen)  # 2. draw debug grid on top
            self.blue_rifleman.display_rifleman(screen) # 3. draw units on top
            self.blue_rifleman.draw_bullets(screen)

            self.blue_rifleman.allow_movement()
            movement.move_along_path(self.blue_rifleman, self.game_map)
            movement.draw_path(self.blue_rifleman, screen)
            movement.draw_waypoints(self.blue_rifleman, screen)

            # get the x and y
            x, y = pygame.mouse.get_pos()
            x_y_coordination = font.render(f"({x},{y})", True, (0, 0, 0))
            text_rect = x_y_coordination.get_rect()
            screen.blit(x_y_coordination, text_rect)
            # self.game_map.color_recognizer(screen, x, y)

            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()