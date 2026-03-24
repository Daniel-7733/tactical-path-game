"""
                units.py
                    This is for my units

-------------------- Don't forget this a collection group idea --------------------
                                Army
                                 └── has many Groups
                                Group
                                 └── has many Units

                                 *** In Code language ***

                                class Unit:
                                    pass

                                class Group:
                                    def __init__(self):
                                        self.units = []

                                class Army:
                                    def __init__(self):
                                        self.groups = []

-------------------- If I want to have hierarchy; This is perfect --------------------
                                class Unit:
                                    pass

                                class GroundUnit(Unit):
                                    pass

                                class AirUnit(Unit):
                                    pass

                                class NavyUnit(Unit):
                                    pass


                                *** Usage ***
                                class Rifleman(GroundUnit):
                                    pass

                                class Tank(GroundUnit):
                                    pass

                                class FighterJet(AirUnit):
                                    pass

                                class carrier(NavyUnit):
                                    pass

"""
import pygame
from pygame import Surface, Rect

from data.settings import TILE_SIZE
from game.map import Map


class Unit:
    """This class represents a unit; how it works"""
    def __init__(self, x, y, direction, color) -> None:
        """
        Initializer for Unit

        :param x: Position of unit on x-axis of screen
        :param y: Position of unit on y-axis of screen
        :param direction: this one give direction to the movement of unit (it is either 1 or -1)
        :param color: unit's color is RGB value in tuple form
        :return: None
        """
        self.x: float = x
        self.y: float = y
        self.direction: int = direction
        self.color: tuple[int, int, int] = color

        self.x_velocity: float = 0.5
        self.y_velocity: float = 0.5
        self.radius: int = 10

    def draw(self, surface) -> None:
        """
        Draw unit (circle) on screen
        :param surface: surface to draw the map on (screen)
        :return: None
        """
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.x), int(self.y)),
            self.radius,
        )

    def display_rifleman(self, surface) -> None:
        """
        Display rifleman on the screen
        :param surface: surface to draw the map on (screen)
        :return: None
        """
        load_rifleman_man: Surface = pygame.image.load("assets/images/Rifleman-friend.png").convert_alpha()
        rifleman_man_rect: Rect = load_rifleman_man.get_rect()
        rifleman_man_rect.x = int(self.x)
        rifleman_man_rect.y = int(self.y)

        resized_rifleman_man = pygame.transform.scale(load_rifleman_man, (10, 10))

        surface.blit(resized_rifleman_man, rifleman_man_rect) # instead of displaying the load_rifleman_man, I choose resized_rifleman_man because the resizing the img

    def move(self, game_map: Map) -> None:
        """
         This function force the unit to move on screen
         :param game_map: This argument accept Map class object
         :return: None
        """
        if self.can_move(game_map):
            self.x += self.x_velocity * self.direction
            self.y += self.y_velocity * self.direction

    def can_move(self, game_map: Map) -> bool:
        """
        This function check if the unit can move on screen.

        :param game_map: This argument accept Map class object
        :return: True if unit can move otherwise return False
        """
        # Calculation next x and y
        next_x: float = self.x + self.x_velocity * self.direction
        next_y: float = self.y + self.y_velocity * self.direction

        # Calculating the next Tile on both axes
        tile_x: int = int(next_x // TILE_SIZE)
        tile_y: int = int(next_y // TILE_SIZE)

        # This one check if the object stay inside bounds
        if 0 <= tile_y < len(game_map.grid) and 0 <= tile_x < len(game_map.grid[0]):
            return game_map.grid[tile_y][tile_x] == 1
        return False
