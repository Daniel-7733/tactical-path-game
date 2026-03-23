"""
                renderer.py
                    Owns:
                        drawing
                    Does not own:
                        path validation
                        range calculations
"""
import pygame
from data.settings import TILE_SIZE


def draw_midline(surface, screen_width: int, screen_height: int) -> None:
    """
    Draws the horizontal midline of the path
    :param screen_width: screen width size
    :param screen_height: screen height size
    :param surface: take surface.pygame (screen)
    :return: None
    """
    y: int = screen_height // 2
    pygame.draw.line(surface, (0, 0, 0), (0, y), (screen_width, y), 1)


def draw_tiles(surface, screen_width: int, screen_height: int) -> None:
    """
    Draws all the tiles on the screen.
    :param screen_width: screen width size
    :param screen_height: screen height size
    :param surface: take surface.pygame (screen)
    :return: None
    """
    for row in range(0, screen_height, TILE_SIZE):
        pygame.draw.line(surface, (0, 0, 0), (0, row), (screen_width, row), 1)

    for col in range(0, screen_width, TILE_SIZE):
        pygame.draw.line(surface, (0, 0, 0), (col, 0), (col, screen_height), 1)
