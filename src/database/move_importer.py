from __future__ import annotations

from typing import Any


class MoveImporter:
    """
    Converts the PokéAPI /move endpoint into PokeCarlo move data.
    """

    def __init__(self):
        self.TARGET_MAP = {
            "selected-pokemon": "SINGLE_TARGET",
            "all-other-pokemon": "ALL_OTHERS",
            "user": "SELF",
            "users-field": "USER_FIELD",
            "entire-field": "FIELD",
            "ally": "ALLY",
            "user-and-allies": "SELF_AND_ALLIES",
            "all-pokemon": "ALL_POKEMON",
            "random-opponent": "RANDOM_OPPONENT",
            "specific-move": "NONE",
            "opponents-field": "OPPONENT_FIELD",
        }

        self.CATEGORY_MAP = {
            "physical": "PHYSICAL",
            "special": "SPECIAL",
            "status": "STATUS",
        }

    def to_database_model(
        self,
        move_data: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "id": move_data["id"],
            "move_name": self._canonical_name(
                move_data["name"],
            ),
            "display_name": (move_data["name"].replace("-", " ").title()),
            "move_type": (move_data["type"]["name"].upper()),
            "category": self.CATEGORY_MAP.get(
                move_data["damage_class"]["name"],
                "UNKNOWN",
            ),
            "power": move_data.get("power"),
            "accuracy": move_data.get("accuracy"),
            "pp": move_data.get("pp"),
            "priority": move_data.get("priority", 0),
            "target": self.TARGET_MAP.get(
                move_data["target"]["name"],
                "UNKNOWN",
            ),
            "move_flags": [
                self._canonical_name(flag["name"])
                for flag in move_data.get("flags", [])
            ],
            "effects": [],
        }

    def _canonical_name(
        self,
        name: str,
    ) -> str:
        return name.upper().replace("-", "_")
