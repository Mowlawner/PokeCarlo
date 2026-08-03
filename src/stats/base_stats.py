# basestats.py

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BaseStats:
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int

    @classmethod
    def from_json(cls, json_data):
        return BaseStats(
            hp=json_data["hp"],
            attack=json_data["attack"],
            defense=json_data["defense"],
            sp_attack=json_data["sp_attack"],
            sp_defense=json_data["sp_defense"],
            speed=json_data["speed"],
        )
