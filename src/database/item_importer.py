from __future__ import annotations

from typing import Any


class ItemImporter:
    """Converts PokéAPI item data into the generated database format."""

    def to_database_model(
        self,
        item_data: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "item_id": item_data["id"],
            "item_name": self._canonical_name(item_data["name"]),
            "display_name": self._get_english_name(item_data["names"]),
            "category": self._canonical_name(item_data["category"]["name"]),
            "attributes": sorted(
                self._canonical_name(attribute["name"])
                for attribute in item_data["attributes"]
            ),
        }

    def _get_english_name(
        self,
        names: list[dict[str, Any]],
    ) -> str:
        for entry in names:
            if entry["language"]["name"] == "en":
                return entry["name"]

        raise ValueError("Item has no English name.")

    def _canonical_name(self, name: str) -> str:
        return name.upper().replace("-", "_").replace(" ", "_")
