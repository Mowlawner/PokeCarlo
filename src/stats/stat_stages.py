from dataclasses import dataclass

from src.stats.stat import DEFAULT_STAGE


@dataclass(slots=True)
class StatStages:
    attack: int = DEFAULT_STAGE
    defense: int = DEFAULT_STAGE
    sp_attack: int = DEFAULT_STAGE
    sp_defense: int = DEFAULT_STAGE
    speed: int = DEFAULT_STAGE
    accuracy: int = DEFAULT_STAGE
    evasion: int = DEFAULT_STAGE
