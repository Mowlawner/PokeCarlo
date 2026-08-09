from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any


class LearnsetDatabase:
    """A runtime database of canonical move names available to each form."""

    def __init__(self, learnsets: dict[str, frozenset[str]]):
        self._learnsets = learnsets

    @classmethod
    def load(cls, directory_path: str | Path) -> LearnsetDatabase:
        path = Path(directory_path)
        if not path.is_dir():
            raise ValueError(f"Path {directory_path} is not a directory.")

        learnsets: dict[str, frozenset[str]] = {}
        for json_file in path.glob("*.json"):
            try:
                with json_file.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                name, moves = cls._parse_learnset(data)
            except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid learnset data in {json_file}: {error}"
                ) from error

            if name in learnsets:
                raise ValueError(f"Duplicate learnset name {name!r} in {json_file}.")
            learnsets[name] = moves

        return cls(learnsets)

    @staticmethod
    def _parse_learnset(data: Any) -> tuple[str, frozenset[str]]:
        if not isinstance(data, dict):
            raise TypeError("expected a JSON object")

        name = _normalize_name(data["pokemon"])
        moves = data["moves"]
        if not isinstance(moves, list):
            raise TypeError("moves must be a list")

        return name, frozenset(_canonical_name(move) for move in moves)

    def get(self, name: str) -> frozenset[str]:
        return self._learnsets[_normalize_name(name)]

    def __len__(self) -> int:
        return len(self._learnsets)

    def __iter__(self) -> Iterator[frozenset[str]]:
        return iter(self._learnsets.values())


def _normalize_name(name: Any) -> str:
    return _canonical_name(name).replace(" ", "_")


def _canonical_name(name: Any) -> str:
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string")
    return name.upper().replace("-", "_")
