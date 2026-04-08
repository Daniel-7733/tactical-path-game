"""
                        path_manager.py

                        Owns:
                            - user-drawn path state
                            - mouse-based line creation
                            - path drawing helpers
                            - conversion from line segments to waypoints

                        Does not own:
                            - game loop
                            - unit movement
                            - map generation
"""

import math
import pygame


class PathManager:
    """
    Manage user-drawn path segments on the screen.

    This class stores:
        - whether the user is currently drawing
        - the starting position of the current line
        - all completed line segments
    """

    def __init__(self) -> None:
        """
        Initialize the path manager.

        :return: None
        """
        self.drawing: bool = False
        self.start_pos: tuple[int, int] | None = None
        self.lines: list[tuple[tuple[int, int], tuple[int, int]]] = []

    def handle_mouse_down(self, pos: tuple[int, int], button: int) -> None:
        """
        Start drawing a new path segment when the left mouse button is pressed.

        :param pos: Mouse position at the time of button press.
        :param button: Mouse button value from pygame event.
        :return: None
        """
        if button == 1:
            self.drawing = True
            self.start_pos = pos

    def handle_mouse_up(self, pos: tuple[int, int], button: int) -> None:
        """
        Finish drawing a path segment when the left mouse button is released.

        If a valid start position exists, save the line segment.

        :param pos: Mouse position at the time of button release.
        :param button: Mouse button value from pygame event.
        :return: None
        """
        if button == 1:
            self.drawing = False

            if self.start_pos is not None:
                self.lines.append((self.start_pos, pos))

            self.start_pos = None

    def clear(self) -> None:
        """
        Clear all drawn path segments.

        :return: None
        """
        self.lines.clear()
        self.drawing = False
        self.start_pos = None

    def draw_arrow(self, surface: pygame.Surface, color: tuple[int, int, int],
                   start: tuple[int, int], end: tuple[int, int]) -> None:
        """
        Draw a line with an arrow head.

        :param surface: Surface to draw on.
        :param color: RGB color of the arrow.
        :param start: Start point of the arrow.
        :param end: End point of the arrow.
        :return: None
        """
        pygame.draw.line(surface, color, start, end, 2)

        dx: int = end[0] - start[0]
        dy: int = end[1] - start[1]
        angle: float = math.atan2(dy, dx)

        size: int = 15
        spread: float = math.pi / 6

        p1: tuple[float, float] = (
            end[0] - size * math.cos(angle - spread),
            end[1] - size * math.sin(angle - spread),
        )
        p2: tuple[float, float] = (
            end[0] - size * math.cos(angle + spread),
            end[1] - size * math.sin(angle + spread),
        )

        pygame.draw.polygon(surface, color, [end, p1, p2])

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw all saved path segments and the currently active segment.

        Saved segments are drawn in white.
        The currently active segment is drawn in green.

        :param surface: Surface to draw on.
        :return: None
        """
        saved_color: tuple[int, int, int] = (255, 255, 255)
        active_color: tuple[int, int, int] = (0, 255, 0)

        for start, end in self.lines:
            pygame.draw.line(surface, saved_color, start, end, 2)
            self.draw_arrow(surface, saved_color, start, end)

        if self.drawing and self.start_pos is not None:
            mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
            pygame.draw.line(surface, active_color, self.start_pos, mouse_pos, 2)
            self.draw_arrow(surface, active_color, self.start_pos, mouse_pos)

    def lines_to_waypoints(self) -> list[tuple[int, int]]:
        """
        Convert stored line segments into waypoint points.

        Example:
            lines = [((10, 10), (50, 10)), ((50, 10), (50, 60))]
            result = [(10, 10), (50, 10), (50, 60)]

        :return: A list of waypoints in drawing order.
        """
        if not self.lines:
            return []

        waypoints: list[tuple[int, int]] = [self.lines[0][0]]

        for _, end in self.lines:
            waypoints.append(end)

        return waypoints
    