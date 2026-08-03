# stats.py

from dataclasses import dataclass

from stats.stat import Stat


@dataclass(slots=True, frozen=True)
class Stats:
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int

    def get(self, stat: Stat) -> int:
        match stat:
            case Stat.HP:
                return self.hp
            case Stat.ATTACK:
                return self.attack
            case Stat.DEFENSE:
                return self.defense
            case Stat.SP_ATTACK:
                return self.sp_attack
            case Stat.SP_DEFENSE:
                return self.sp_defense
            case Stat.SPEED:
                return self.speed
            case _:
                raise ValueError(f"Unknown stat: {stat.name}")
