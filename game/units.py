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
    def __init__(self, x, y, team, unit_type, health, speed, attack_range, damage) -> None:
        """
        Initializer for Unit
        :param x: Position of unit on x-axis of screen
        :param y: Position of unit on y-axis of screen

        :param team: Can be the color representing the team of the unit like red and blue
        :param unit_type: Unit type like rifleman unit
        :param health: amount of health that unit have
        :param speed: speed of unit like 20
        :param attack_range: how far can the unit hit like 10
        :param damage: the amount of damage that can be made like 20
        """
        self.x: float = x
        self.y: float = y
        self.team: str = team # Red \ Blue
        self.unit_type: str = unit_type # ex: rifleman
        self.health: int = health
        self.speed: int = speed
        self.attack_range: int = attack_range
        self.damage: int = damage
        self.x_velocity: float = 0.5
        self.y_velocity: float = 0.5
        self.direction: int = 1 # 1 or -1


    def draw(self, surface: Surface) -> None:
        """
        Draw unit (circle) on screen
        :param surface: surface to draw the map on (screen)
        :return: None
        """
        pygame.draw.circle(
            surface,
            (0, 0, 0),
            (int(self.x), int(self.y)),
            10,
        )

    def display_rifleman(self, surface: Surface) -> None:
        """
        Display rifleman on the screen
        :param surface: surface to draw the map on (screen)
        :return: None
        """
        load_rifleman_man: Surface = pygame.image.load("assets/images/Rifleman-friend.png").convert_alpha()
        rifleman_man_rect: Rect = load_rifleman_man.get_rect()
        rifleman_man_rect.x = int(self.x)
        rifleman_man_rect.y = int(self.y)

        resized_rifleman_man: Surface = pygame.transform.scale(load_rifleman_man, (10, 10))

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
        tile_x, tile_y = self.calculate_next_x_and_y_tile()
        return game_map.is_title_walkable(tile_x, tile_y)

    def find_next_x_and_y_coordination(self) -> tuple[float, float]:
        """
        Calculate Next x coordinate and y coordination
        :return: x and y coordination as tuple
        """
        next_x: float = self.x + self.x_velocity * self.direction
        next_y: float = self.y + self.y_velocity * self.direction
        return next_x, next_y

    def calculate_next_x_and_y_tile(self) -> tuple[int, int]:
        """
        Calculate Next x tile and y tile
        :return: x and y tile as tuple
        """
        next_x, next_y = self.find_next_x_and_y_coordination()
        tile_x: int = int(next_x // TILE_SIZE)
        tile_y: int = int(next_y // TILE_SIZE)
        return tile_x, tile_y

    # for big direction (up, down, left, right)
    def move_up(self) -> None:
        """Move the unit up"""
        self.x = 0
        self.y_velocity -= self.y_velocity

    def move_down(self) -> None:
        """Move the unit down"""
        self.x = 0
        self.y += self.y_velocity

    def move_left(self) -> None:
        """Move the unit left"""
        self.x -= self.x_velocity
        self.y_velocity = 0

    def move_right(self) -> None:
        """Move the unit right"""
        self.x += self.x_velocity
        self.y_velocity = 0