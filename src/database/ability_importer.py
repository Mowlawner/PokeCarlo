from __future__ import annotations

from typing import Any


class AbilityImporter:
    """
    Converts PokéAPI ability data into the database format.
    """

    def to_database_model(
        self,
        ability_data: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "ability_id": ability_data["id"],
            "ability_name": ability_data["name"].upper().replace("-", "_"),
            "display_name": self._get_english_name(
                ability_data["names"],
            ),
            "generation": ability_data["generation"]["name"]
            .upper()
            .replace(
                "-",
                "_",
            ),
        }

    def _get_english_name(
        self,
        names: list[dict[str, Any]],
    ) -> str:
        for entry in names:
            if entry["language"]["name"] == "en":
                return entry["name"]

        raise ValueError("Ability has no English name.")
