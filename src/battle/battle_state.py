from dataclasses import dataclass

from pokemon import Pokemon
from terrain import Terrain
from weather import Weather


@dataclass(slots=True)
class BattleState:
    player_active: Pokemon
    opponent_active: Pokemon

    turn_number: int = 1

    weather: Weather | None = None
    terrain: Terrain | None = None
