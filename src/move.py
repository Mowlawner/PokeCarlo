from dataclasses import dataclass


@dataclass(slots=True)
class Move:
    name: str

    power: int

    accuracy: int

    move_type: str

    category: str

    priority: int = 0
