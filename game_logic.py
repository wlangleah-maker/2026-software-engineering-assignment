from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

DIRECTIONS = {"up", "down", "left", "right"}


@dataclass(frozen=True)
class Arrow:
    """A single grid arrow."""

    id: str
    row: int
    col: int
    direction: str

    def __post_init__(self) -> None:
        if self.direction not in DIRECTIONS:
            raise ValueError(f"Unknown direction: {self.direction}")
        if self.row < 0 or self.col < 0:
            raise ValueError("Arrow coordinates must be non-negative")


class GameModel:
    """Pure game rules, independent from Tkinter and suitable for unit tests."""

    def __init__(self, arrows: Sequence[Arrow], max_mistakes: int = 3) -> None:
        if max_mistakes <= 0:
            raise ValueError("max_mistakes must be positive")
        self._initial = tuple(arrows)
        self.max_mistakes = max_mistakes
        self.reset()

    def reset(self) -> None:
        self.arrows: dict[str, Arrow] = {arrow.id: arrow for arrow in self._initial}
        if len(self.arrows) != len(self._initial):
            raise ValueError("Arrow ids must be unique")
        self.mistakes_left = self.max_mistakes

    @property
    def remaining(self) -> int:
        return len(self.arrows)

    @property
    def won(self) -> bool:
        return self.remaining == 0

    @property
    def failed(self) -> bool:
        return self.mistakes_left <= 0 and not self.won

    def is_blocked(self, arrow_id: str) -> bool:
        arrow = self.arrows[arrow_id]
        for other in self.arrows.values():
            if other.id == arrow.id:
                continue
            if arrow.direction == "up" and other.col == arrow.col and other.row < arrow.row:
                return True
            if arrow.direction == "down" and other.col == arrow.col and other.row > arrow.row:
                return True
            if arrow.direction == "left" and other.row == arrow.row and other.col < arrow.col:
                return True
            if arrow.direction == "right" and other.row == arrow.row and other.col > arrow.col:
                return True
        return False

    def click(self, arrow_id: str) -> str:
        """Apply one click and return removed/blocked/won/failed/ignored."""
        if self.won or self.failed or arrow_id not in self.arrows:
            return "ignored"
        if self.is_blocked(arrow_id):
            self.mistakes_left -= 1
            return "failed" if self.failed else "blocked"
        del self.arrows[arrow_id]
        return "won" if self.won else "removed"


def find_solution(arrows: Iterable[Arrow]) -> list[str] | None:
    """Find a valid removal order with DFS; used to verify level solvability."""
    initial = tuple(arrows)

    def blocked(arrow: Arrow, remaining: tuple[Arrow, ...]) -> bool:
        for other in remaining:
            if other.id == arrow.id:
                continue
            if arrow.direction == "up" and other.col == arrow.col and other.row < arrow.row:
                return True
            if arrow.direction == "down" and other.col == arrow.col and other.row > arrow.row:
                return True
            if arrow.direction == "left" and other.row == arrow.row and other.col < arrow.col:
                return True
            if arrow.direction == "right" and other.row == arrow.row and other.col > arrow.col:
                return True
        return False

    def dfs(remaining: tuple[Arrow, ...]) -> list[str] | None:
        if not remaining:
            return []
        for arrow in remaining:
            if not blocked(arrow, remaining):
                rest = tuple(item for item in remaining if item.id != arrow.id)
                suffix = dfs(rest)
                if suffix is not None:
                    return [arrow.id, *suffix]
        return None

    return dfs(initial)
