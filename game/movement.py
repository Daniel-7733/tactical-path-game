"""
                    Owns:
                        - movement logic
                        - movement along path
                        - collision / walkability checks
                        - path drawing helpers

                    Does not own:
                        - unit identity / stats storage
                        - timer text
                        - map generation
"""

import pygame
from game.map import Map
from data.settings import TILE_SIZE
import math

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.units import Unit



def try_move_to(unit: "Unit", next_x: float, next_y: float, game_map: Map) -> None:
    """
    Try to move the unit to a new position.

    This function checks whether the target tile is walkable.
    If it is walkable, it updates the unit position.

    :param unit: The unit object that is trying to move.
    :param next_x: The next x coordinate.
    :param next_y: The next y coordinate.
    :param game_map: The map object used to check walkability.
    :return: None
    """
    tile_x: int = int(next_x // TILE_SIZE)
    tile_y: int = int(next_y // TILE_SIZE)

    if game_map.is_tile_walkable(tile_x, tile_y):
        unit.x = next_x
        unit.y = next_y


def move_up(unit: "Unit", game_map: Map) -> None:
    """
    Move the unit upward.

    :param unit: The unit object that is moving.
    :param game_map: The map object used to check walkability.
    :return: None
    """
    try_move_to(unit, unit.x, unit.y - unit.speed, game_map)


def move_down(unit: "Unit", game_map: Map) -> None:
    """
    Move the unit downward.

    :param unit: The unit object that is moving.
    :param game_map: The map object used to check walkability.
    :return: None
    """
    try_move_to(unit, unit.x, unit.y + unit.speed, game_map)


def move_left(unit: "Unit", game_map: Map) -> None:
    """
    Move the unit to the left.

    :param unit: The unit object that is moving.
    :param game_map: The map object used to check walkability.
    :return: None
    """
    try_move_to(unit, unit.x - unit.speed, unit.y, game_map)


def move_right(unit: "Unit", game_map: Map) -> None:
    """
    Move the unit to the right.

    :param unit: The unit object that is moving.
    :param game_map: The map object used to check walkability.
    :return: None
    """
    try_move_to(unit, unit.x + unit.speed, unit.y, game_map)


def move_up_left(unit: "Unit", game_map: Map) -> None:
    """
    Move the unit diagonally up-left.

    :param unit: The unit object that is moving.
    :param game_map: The map object used to check walkability.
    :return: None
    """
    try_move_to(unit, unit.x - unit.speed, unit.y - unit.speed, game_map)


def move_up_right(unit: "Unit", game_map: Map) -> None:
    """
    Move the unit diagonally up-right.

    :param unit: The unit object that is moving.
    :param game_map: The map object used to check walkability.
    :return: None
    """
    try_move_to(unit, unit.x + unit.speed, unit.y - unit.speed, game_map)


def move_down_left(unit: "Unit", game_map: Map) -> None:
    """
    Move the unit diagonally down-left.

    :param unit: The unit object that is moving.
    :param game_map: The map object used to check walkability.
    :return: None
    """
    try_move_to(unit, unit.x - unit.speed, unit.y + unit.speed, game_map)


def move_down_right(unit: "Unit", game_map: Map) -> None:
    """
    Move the unit diagonally down-right.

    :param unit: The unit object that is moving.
    :param game_map: The map object used to check walkability.
    :return: None
    """
    try_move_to(unit, unit.x + unit.speed, unit.y + unit.speed, game_map)


def get_current_target(unit: "Unit") -> tuple[float, float] | None:
    """
    Get the current waypoint that the unit should move toward.

    :param unit: The unit object that stores the path and current path index.
    :return:
        - A tuple of (target_x, target_y) if a target exists.
        - None if the path is finished.
    """
    if unit.path_index >= len(unit.path):
        return None
    return unit.path[unit.path_index]


def is_close_to_target(unit: "Unit", target_x: float, target_y: float) -> bool:
    """
    Check whether the unit is close enough to the target point.

    This is used so the unit does not need to land on the exact pixel.
    Instead, if it is close enough, we treat the target as reached.

    :param unit: The unit object that is moving.
    :param target_x: Target x coordinate.
    :param target_y: Target y coordinate.
    :return: True if the unit is close enough to the target, otherwise False.
    """
    return abs(unit.x - target_x) <= unit.speed and abs(unit.y - target_y) <= unit.speed


def draw_path(unit: "Unit", surface: pygame.Surface) -> None:
    """
    Draw the full path as red connected lines.

    :param unit: The unit object that stores the path.
    :param surface: The surface to draw on.
    :return: None
    """
    if len(unit.path) > 1:
        pygame.draw.lines(surface, (255, 0, 0), False, unit.path, 3)


def draw_waypoints(unit: "Unit", surface: pygame.Surface) -> None:
    """
    Draw the waypoints of the path.

    Yellow dots = normal waypoints
    Green dot = current target waypoint

    :param unit: The unit object that stores the path and current path index.
    :param surface: The surface to draw on.
    :return: None
    """
    for i, (x, y) in enumerate(unit.path):
        color: tuple[int, int, int] = (255, 255, 0)

        if i == unit.path_index:
            color = (0, 255, 0)

        pygame.draw.circle(surface, color, (int(x), int(y)), 6)


def move_along_path(unit: "Unit", game_map: Map) -> None:
    """
    Move the unit toward the current waypoint in a straight direction.

    :param unit: The unit object that stores position, path, and movement permission.
    :param game_map: The map object used to check walkability.
    :return: None
    """
    if not unit.can_move_by_command:
        return

    target: tuple[float, float] | None = get_current_target(unit)
    if target is None:
        return

    target_x, target_y = target

    if is_close_to_target(unit, target_x, target_y):
        unit.x = target_x
        unit.y = target_y
        unit.path_index += 1
        return

    dx: float = target_x - unit.x
    dy: float = target_y - unit.y
    distance: float = math.hypot(dx, dy)

    if distance == 0:
        return

    dir_x: float = dx / distance
    dir_y: float = dy / distance

    next_x: float = unit.x + dir_x * unit.speed
    next_y: float = unit.y + dir_y * unit.speed

    try_move_to(unit, next_x, next_y, game_map)

