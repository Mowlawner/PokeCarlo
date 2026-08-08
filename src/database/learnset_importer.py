from __future__ import annotations

from typing import Any


class LearnsetImporter:
    """
    Converts PokéAPI Pokémon move data into version-specific learnsets.
    """

    def to_database_model(
        self,
        pokemon_data: dict[str, Any],
        target_version_group: str,
    ) -> dict[str, Any]:
        return {
            "pokemon": pokemon_data["name"].upper(),
            "version_group": target_version_group.upper(),
            "moves": self._extract_moves(
                pokemon_data,
                target_version_group,
            ),
        }

    def _extract_moves(
        self,
        pokemon_data: dict[str, Any],
        target_version_group: str,
    ) -> list[str]:
        moves: set[str] = set()

        for move_entry in pokemon_data["moves"]:
            move_name = move_entry["move"]["name"].upper().replace("-", "_")

            for detail in move_entry["version_group_details"]:
                version_group = detail["version_group"]["name"]

                if version_group == target_version_group:
                    moves.add(move_name)

        return sorted(moves)
