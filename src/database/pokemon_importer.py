from __future__ import annotations

from typing import Any


class PokemonImporter:
    """
    Converts the PokéAPI /pokemon endpoint into PokeCarlo form data.
    """

    def to_database_model(
        self,
        pokemon_data: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "pokemon_id": pokemon_data["id"],
            "species_name": self._canonical_name(
                pokemon_data["species"]["name"],
            ),
            "display_name": pokemon_data["name"].replace(
                "-",
                " ",
            ).title(),
            "types": self._extract_types(pokemon_data),
            "base_stats": self._extract_base_stats(pokemon_data),
            "abilities": self._extract_abilities(pokemon_data),
            "height": pokemon_data["height"],
            "weight": pokemon_data["weight"],
        }

    def _canonical_name(
        self,
        name: str,
    ) -> str:
        return name.upper().replace("-", "_")

    def _extract_types(
        self,
        pokemon_data: dict[str, Any],
    ) -> list[str]:
        return [
            self._canonical_name(entry["type"]["name"])
            for entry in sorted(
                pokemon_data["types"],
                key=lambda t: t["slot"],
            )
        ]

    def _extract_base_stats(
        self,
        pokemon_data: dict[str, Any],
    ) -> dict[str, int]:
        stat_name_map = {
            "hp": "hp",
            "attack": "attack",
            "defense": "defense",
            "special-attack": "sp_attack",
            "special-defense": "sp_defense",
            "speed": "speed",
        }

        return {
            stat_name_map[entry["stat"]["name"]]: entry["base_stat"]
            for entry in pokemon_data["stats"]
        }

    def _extract_abilities(
        self,
        pokemon_data: dict[str, Any],
    ) -> list[str]:
        return [
            self._canonical_name(entry["ability"]["name"])
            for entry in sorted(
                pokemon_data["abilities"],
                key=lambda a: a["slot"],
            )
        ]