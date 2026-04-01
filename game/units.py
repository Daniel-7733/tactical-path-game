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
        self.team: str = team  # Red \ Blue
        self.unit_type: str = unit_type  # ex: rifleman
        self.health: int = health
        self.speed: float = speed
        self.attack_range: int = attack_range
        self.damage: int = damage
        self.x_velocity: float = 0.5
        self.y_velocity: float = 0.5
        self.direction: int = 1  # 1 or -1

        # This part is for unit to walk
        self.path: list[tuple[float, float]] = [] # list of target points
        self.path_index: int = 0 # which point we are currently moving toward
        self.can_move_by_command = False # permission to move

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

        surface.blit(resized_rifleman_man,
                     rifleman_man_rect)  # instead of displaying the load_rifleman_man, I choose resized_rifleman_man because the resizing the img

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

    # set up for movement
    def set_path(self, path: list[tuple[float, float]]) -> None:
        """
        give the unit a new path
        start from first waypoint

        :param path: a list of waypoints [(x,y)]
        :return: None
        """
        self.path = path
        self.path_index = 0

    def allow_movement(self) -> None:
        """
        Allow movement of the unit. Note -> this one will be used by user not by inner function.
        Example: user draw the attack line and then press the ready, then this function let the unit move.
        :return: None
        """
        self.can_move_by_command = True

    def stop_movement(self) -> None:
        """
        Allow movement of the unit. Note -> this one will be used by user not by inner function.
        Example: Won't let the unit move until user is ready
        :return: None
        """
        self.can_move_by_command = False

    def try_move_to(self, next_x: float, next_y: float, game_map: Map) -> None:
        """
        This function try to move the unit
        :param next_x: Add the next x coordinate
        :param next_y: Add the next y coordinate
        :param game_map: This argument accept Map class object
        :return: None
        """
        tile_x: int = int(next_x // TILE_SIZE)
        tile_y: int = int(next_y // TILE_SIZE)

        if game_map.is_tile_walkable(tile_x, tile_y):
            self.x = next_x
            self.y = next_y

    # for big direction (up, down, left, right)
    def move_up(self, game_map: Map) -> None:
        """
        Move the unit up
        :param game_map: This argument accept Map class object
        :return: None
        """
        self.try_move_to(self.x, self.y - self.speed, game_map)

    def move_down(self, game_map: Map) -> None:
        """
        Move the unit down
        :param game_map: This argument accept Map class object
        :return: None
        """
        self.try_move_to(self.x, self.y + self.speed, game_map)

    def move_left(self, game_map: Map) -> None:
        """
        Move the unit left
        :param game_map: This argument accept Map class object
        :return: None
        """
        self.try_move_to(self.x - self.speed, self.y, game_map)

    def move_right(self, game_map: Map) -> None:
        """
        Move the unit right
        :param game_map: This argument accept Map class object
        :return: None
        """
        self.try_move_to(self.x + self.speed, self.y, game_map)

    # for big diagonal direction (up-left, up-right, down-left, down-right)
    def move_up_left(self, game_map: Map) -> None:
        """
        Move the unit up and left
        :param game_map: This argument accept Map class object
        :return: None
        """
        self.try_move_to(self.x - self.speed, self.y - self.speed, game_map)

    def move_up_right(self, game_map: Map) -> None:
        """
        Move the unit up and right
        :param game_map: This argument accept Map class object
        :return: None
        """
        self.try_move_to(self.x + self.speed, self.y - self.speed, game_map)

    def move_down_left(self, game_map: Map) -> None:
        """
        Move the unit down and left
        :param game_map: This argument accept Map class object
        :return: None
        """
        self.try_move_to(self.x - self.speed, self.y + self.speed, game_map)

    def move_down_right(self, game_map: Map) -> None:
        """
        Move the unit down and right
        :param game_map: This argument accept Map class object
        :return: None
        """
        self.try_move_to(self.x + self.speed, self.y + self.speed, game_map)

    # unit will choose path to go
    def move_along_path(self, game_map: Map) -> None:
        """
        Move the unit along the path.
        :param game_map: This argument accept Map class object
        :return: None
        """

        # TODO: Fix this function:
        """ 
        This one is a fine function but its not good for my unit; it need more details or changes
        because my unit is not smart enough to walk and decide which direction is good to choose
        """
        if not self.can_move_by_command:
            return

        if self.path_index >= len(self.path):
            return

        target_x, target_y = self.path[self.path_index]
        close_enough: float = self.speed

        if abs(self.x - target_x) <= close_enough and abs(self.y - target_y) <= close_enough:
            self.x = target_x
            self.y = target_y
            self.path_index += 1
            return

        if abs(self.x - target_x) > close_enough:
            if self.x < target_x:
                self.move_right(game_map)
            else:
                self.move_left(game_map)
        elif abs(self.y - target_y) > close_enough:
            if self.y < target_y:
                self.move_down(game_map)
            else:
                self.move_up(game_map)
