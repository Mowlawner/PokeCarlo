from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

from move.move import Move
from move.move_category import MoveCategory
from move.targeting import MoveTarget
from move_effects.damage_effect import DamageEffect
from move_effects.healing_effect import HealingEffect
from move_effects.stat_change_effect import StatChangeEffect
from pokemon_types import Type
from stats.stat import Stat


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
                category = MoveCategory[data["category"]]
                power = data["power"]
                effects = tuple(
                    cls._load_effect(effect_data)
                    for effect_data in data.get("effects", [])
                )

                # The first executable database slice supports ordinary
                # single-hit damaging moves. Specialized move behavior stays
                # out of the database loader until it has a dedicated effect.
                if (
                    power is not None
                    and not effects
                    and category
                    in (
                        MoveCategory.PHYSICAL,
                        MoveCategory.SPECIAL,
                    )
                ):
                    effects = (DamageEffect(power=power),)

                move = Move(
                    name=data["move_name"],
                    display_name=data["display_name"],
                    id=data["id"],
                    accuracy=data["accuracy"],
                    pp=data["pp"],
                    power=power,
                    move_type=Type[data["move_type"]],
                    category=category,
                    effects=effects,
                    move_flags=tuple(data["move_flags"]),
                    targeting=MoveTarget[data["target"]],
                    priority=data["priority"],
                )
                moves[move.name] = move

        return cls(moves)

    @staticmethod
    def _load_effect(effect_data: dict[str, object]):
        if effect_data["type"] == "stat_change":
            return StatChangeEffect(
                stat=Stat[effect_data["stat"]],
                stages=effect_data["stages"],
            )
        if effect_data["type"] == "damage":
            return DamageEffect(power=effect_data["power"])
        if effect_data["type"] == "heal_from_damage":
            return HealingEffect(
                healing_percent=effect_data.get("healing_percent", 50),
                aggregate_damage=effect_data.get("aggregate_damage", False),
            )

        raise ValueError(f"Unsupported move effect: {effect_data['type']}")

    def get(self, name: str) -> Move:
        """
        Retrieves a move by its canonical name (e.g., "THUNDERBOLT").
        """
        return self._moves[name.upper().replace("-", "_")]

    def __len__(self) -> int:
        return len(self._moves)

    def __iter__(self) -> Iterator[Move]:
        return iter(self._moves.values())
