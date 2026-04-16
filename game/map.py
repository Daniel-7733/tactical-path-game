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
    """This class represents the map on the screen."""
    def __init__(self, image_path: str, screen_width: int, screen_height: int) -> None:
        """
        Initialize the map.
        :param image_path: Add the image or map path (Address)
        :param screen_width: Screen width size
        :param screen_height: Screen height size
        :return: None
        """
        self.image: Surface = pygame.image.load(image_path).convert_alpha()
        self.image: Surface = pygame.transform.scale(self.image, (screen_width, screen_height))

        self.width: int = self.image.get_width()
        self.height: int = self.image.get_height()

        self.grid: list[list[int]] = self.generate_tile_grid()

    def draw(self, surface: Surface) -> None:
        """
        Draw the map on the screen.
        :param surface: surface to draw the map on (screen)
        :return: None
        """
        surface.blit(self.image, (0, 0))

    def is_road(self, color: tuple[int, int, int]) -> bool:
        """
        Return True if the sampled pixel matches the road color range.
        This currently assumes roads are bright yellow/beige pixels.
        :param color: accept color as RGB formated tuple
        :return: True or False
        """
        r, g, b = color
        # return r > 200 and g > 170 and b < 140 # Detect yellow road (tuned for your map)
        return r == 15 and g == 127 and b == 0 # River -> R=0, G=158, B=217... Land (green) R=15, G=127, B=0

    def generate_tile_grid(self) -> list[list[int]]:
        """
        Generate a grid from the map image.
        1 = walkable road
        0 = blocked tile
        :return: list[list[int]] -> full data map grid.
        """
        grid: list[list[int]] = []

        for y in range(0, self.height, TILE_SIZE):
            row: list[int] = []

            for x in range(0, self.width, TILE_SIZE):
                color: tuple[int, int, int] = self.image.get_at((x, y))[:3]

                if self.is_road(color):
                    row.append(1) # road
                else:
                    row.append(0) # block

            grid.append(row)

        return grid

    def draw_grid_debug(self, surface: Surface) -> None:
        """
        Draw the grid on the screen for debugging.
        :param surface: surface to draw the map on (screen)
        :return: None
        """
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 0:
                    color: tuple[int, int, int] = (255, 0, 0)  # blocked
                else:
                    color = (0, 255, 0)  # road

                pygame.draw.rect(
                    surface,
                    color,
                    (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    1
                )

    def is_tile_walkable(self, tiles_x: int, tiles_y: int) -> bool:
        """
        This function make a simple model to determine if the tile is walkable for the obj.

        (y) == (Rows)
         ↓
        [
        [0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0]
        ]
         → (x) == (Columns)

        So the current form of checking is grid[y][x] (grid[row][column])

        :param tiles_x: The size of title_x (like 10)
        :param tiles_y: The size of title_y (like 10)
        :return: True if tile

        """
        if 0 <= tiles_y < len(self.grid) and 0 <= tiles_x < len(self.grid[0]):
            return self.grid[tiles_y][tiles_x] == 1
        return False

    def print_color_under_mouse(self) -> None:
        """
        This is for debugging purposes.
        Print the RGBA color value under the mouse cursor.
        Useful for debugging map colors.
        """
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()

        try:
            pixel_color = self.image.get_at(mouse_pos)
            print(f"Pixel color at {mouse_pos}: {pixel_color}")

            red: int = pixel_color.r
            green: int = pixel_color.g
            blue: int = pixel_color.b
            alpha: int = pixel_color.a

            print(f"RGBA values: R={red}, G={green}, B={blue}, A={alpha}")

        except IndexError:
            print("Mouse is outside the image bounds.")

    def color_recognizer(self, surface: Surface, x_pos, y_pos) -> None:
        """
        This function will find the color of the pixel at the given coordinates.
        :param surface: surface to draw the map on (screen)
        :param x_pos: x position on screen
        :param y_pos: y position on screen
        :return: None
        """
        color_obj = surface.get_at((x_pos, y_pos)) # Get the color of a pixel at coordinates (x, y)

        red = color_obj.r
        green = color_obj.g
        blue = color_obj.b

        rgb_tuple = tuple(color_obj[:3]) # Convert to a simple (R, G, B) tuple
        print(f"On ({x_pos}, {y_pos}) point, RGB tuple: {rgb_tuple}")
        print(f"RGBA values: R={red}, G={green}, B={blue}")
