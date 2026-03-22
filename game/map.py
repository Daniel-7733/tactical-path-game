"""
                map.py
                    Owns:
                        map layout
                        blocked areas
                        road positions
                    Does not own:
                        UI
                        timing
                        battle result
"""
import pygame
from pygame import Surface
from data.settings import TILE_SIZE


class Map:
    def __init__(self, image_path: str, screen_width: int, screen_height: int) -> None:
        self.image_path: str = image_path

        self.image: Surface = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))

        self.width: int = self.image.get_width()
        self.height: int = self.image.get_height()

        self.grid: list[list[int]] = self.generate_tile_grid()

    def draw(self, surface: Surface) -> None:
        """Draw the map on the screen."""
        surface.blit(self.image, (0, 0))

    def is_road(self, color: tuple[int, int, int]) -> bool:
        """
        Return True if the sampled pixel matches the road color range.
        This currently assumes roads are bright yellow/beige pixels.
        """
        r, g, b = color
        return r > 240 and g > 187 and b > 72


    def generate_tile_grid(self) -> list[list[int]]:
        """
        Generate a grid from the map image.
        0 = walkable road
        1 = blocked tile
        """
        grid: list[list[int]] = []

        for y in range(0, self.height, TILE_SIZE):
            row: list[int] = []

            for x in range(0, self.width, TILE_SIZE):
                color: tuple[int, int, int] = self.image.get_at((x, y))[:3]

                if self.is_road(color):
                    row.append(0)
                else:
                    row.append(1)

            grid.append(row)

        return grid


    def print_color_under_mouse(self) -> None:
        """
        Print the RGBA color value under the mouse cursor.
        Useful for debugging map colors.
        """
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()

        try:
            pixel_color = self.image.get_at(mouse_pos)
            print(f"Pixel color at {mouse_pos}: {pixel_color}")

            red = pixel_color.r
            green = pixel_color.g
            blue = pixel_color.b
            alpha = pixel_color.a

            print(f"RGBA values: R={red}, G={green}, B={blue}, A={alpha}")

        except IndexError:
            print("Mouse is outside the image bounds.")


