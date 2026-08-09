from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from item import Item


class ItemDatabase:
    """A runtime database loaded from generated item JSON files."""

    def __init__(self, items: dict[str, Item]):
        self._items = items

    @classmethod
    def load(cls, directory_path: str | Path) -> ItemDatabase:
        path = Path(directory_path)
        if not path.is_dir():
            raise ValueError(f"Path {directory_path} is not a directory.")

        items: dict[str, Item] = {}
        for json_file in path.glob("*.json"):
            try:
                with json_file.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                item = cls._parse_item(data)
            except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid item data in {json_file}: {error}"
                ) from error

            if item.name in items:
                raise ValueError(f"Duplicate item name {item.name!r} in {json_file}.")
            items[item.name] = item

        return cls(items)

    @staticmethod
    def _parse_item(data: Any) -> Item:
        if not isinstance(data, dict):
            raise TypeError("expected a JSON object")

        attributes = data["attributes"]
        if not isinstance(attributes, list):
            raise TypeError("attributes must be a list")

        return Item(
            name=data["item_name"],
            display_name=data["display_name"],
            id=data["item_id"],
            category=data["category"],
            attributes=tuple(attributes),
        )

    def get(self, name: str) -> Item:
        return self._items[_normalize_name(name)]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[Item]:
        return iter(self._items.values())


def _normalize_name(name: str) -> str:
    return name.upper().replace("-", "_").replace(" ", "_")
