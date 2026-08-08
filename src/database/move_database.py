from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

from move.move import Move
from move.move_category import MoveCategory
from move.targeting import MoveTarget
from pokemon_types import Type


class MoveDatabase:
    """
    A runtime database of all Pokémon moves, loaded from generated JSON files.
    """

    def __init__(self, moves: dict[str, Move]):
        self._moves = moves

    @classmethod
    def load(cls, directory_path: str | Path) -> MoveDatabase:
        """
        Loads all move JSON files from a directory and creates a MoveDatabase.
        """
        path = Path(directory_path)
        if not path.is_dir():
            raise ValueError(f"Path {directory_path} is not a directory.")

        moves = {}
        for json_file in path.glob("*.json"):
            with json_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                move = Move(
                    name=data["move_name"],
                    display_name=data["display_name"],
                    id=data["id"],
                    accuracy=data["accuracy"],
                    pp=data["pp"],
                    power=data["power"],
                    move_type=Type[data["move_type"]],
                    category=MoveCategory[data["category"]],
                    effects=(),  # Parsing gameplay behavior (effects) belongs elsewhere
                    move_flags=tuple(data["move_flags"]),
                    targeting=MoveTarget[data["target"]],
                    priority=data["priority"],
                )
                moves[move.name] = move

        return cls(moves)

    def get(self, name: str) -> Move:
        """
        Retrieves a move by its canonical name (e.g., "THUNDERBOLT").
        """
        return self._moves[name.upper().replace("-", "_")]

    def __len__(self) -> int:
        return len(self._moves)

    def __iter__(self) -> Iterator[Move]:
        return iter(self._moves.values())
