from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class EVs:
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int
