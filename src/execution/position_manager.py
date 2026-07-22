from __future__ import annotations

from typing import Optional

from src.domain.position import Position


class PositionManager:
    """
    Maintains current open position.
    """

    def __init__(self):

        self._position: Optional[Position] = None

    @property
    def current(self):

        return self._position

    @property
    def has_position(self):

        return self._position is not None

    def open(

        self,

        position: Position,

    ):

        self._position = position

    def close(self):

        self._position = None