from __future__ import annotations

from typing import Any


class SpeciesImporter:
    """
    Converts the PokéAPI /pokemon-species endpoint into
    species-level battle metadata.
    """

    def to_database_model(
        self,
        species_data: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "species_name": self._canonical_name(
                species_data["name"],
            ),
            "national_dex": species_data["id"],
            "gender_ratio": self._extract_gender_ratio(species_data),
            "capture_rate": species_data["capture_rate"],
            "growth_rate": self._extract_growth_rate(species_data),
            "is_legendary": species_data["is_legendary"],
            "is_mythical": species_data["is_mythical"],
            "is_baby": species_data["is_baby"],
            "hatch_cycles": species_data["hatch_counter"],
        }

    def _canonical_name(
            self,
            name: str,
    ) -> str:
        return name.upper().replace("-", "_")

    def _extract_gender_ratio(
        self,
        species_data: dict[str, Any],
    ) -> dict[str, float] | None:
        """
        Convert PokéAPI gender_rate into male/female probabilities.

        Returns None for genderless species.
        """

        gender_rate = species_data["gender_rate"]

        if gender_rate == -1:
            return None

        female = gender_rate / 8
        male = 1 - female

        return {
            "male": male,
            "female": female,
        }

    def _extract_growth_rate(
        self,
        species_data: dict[str, Any],
    ) -> str:
        return species_data["growth_rate"]["name"].upper().replace("-", "_")
