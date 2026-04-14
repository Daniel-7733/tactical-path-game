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
from pygame import Surface, Rect, surface


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


        # This part is for unit to walk
        self.path: list[tuple[float, float]] = [] # list of target points
        self.path_index: int = 0 # which point we are currently moving toward
        self.can_move_by_command = False # permission to move

        self.bullets: list[dict[str, float]] = []

    def draw(self, surface: pygame.Surface) -> None:
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

    def display_rifleman(self, surface: pygame.Surface) -> None:
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

    # TODO: Bullets should have range. EX: 10 unit
    def draw_bullets(self, screen: Surface) -> None:
        """
        Draw all bullets on the screen.

        :param screen: Surface to draw on.
        :return: None
        """
        for bullet in self.bullets:
            pygame.draw.circle(
                screen,
                (255, 247, 10),
                (int(bullet["x"]), int(bullet["y"])),
                3,
            )

    def shoot(self) -> None:
        """
        Create a new bullet starting from the unit position.

        For now, the bullet will move to the right.

        :return: None
        """
        bullet: dict[str, float] = {
            "x": self.x,
            "y": self.y,
            "dx": 1,
            "dy": 0,
            "speed": 8,
        }
        self.bullets.append(bullet)

    def update_bullets(self) -> None:
        """
        Move all bullets forward.

        :return: None
        """
        for bullet in self.bullets:
            bullet["x"] += bullet["dx"] * bullet["speed"]
            bullet["y"] += bullet["dy"] * bullet["speed"]