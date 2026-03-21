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


class Unit:
    def __init__(self, x, y, direction, color) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color

        self.x_velocity = 0.5
        self.y_velocity = 0.5
        self.radius = 10

    def draw(self, surface) -> None:
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.x), int(self.y)),
            self.radius,
        )

    def move(self) -> None:
        self.x += self.x_velocity * self.direction
        self.y += self.y_velocity * self.direction
