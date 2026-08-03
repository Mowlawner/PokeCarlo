from dataclasses import dataclass, fields

MIN_EV = 0
MAX_EV_PER_STAT = 252
MAX_TOTAL_EV = 510


@dataclass(slots=True, frozen=True)
class EVs:
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int

    def __post_init__(self) -> None:
        total_ev = 0

        for field in fields(self):
            value = getattr(self, field.name)

            if not MIN_EV <= value <= MAX_EV_PER_STAT:
                raise ValueError(
                    f"{field.name} EV must be between {MIN_EV} and {MAX_EV_PER_STAT}, got {value}"
                )

            total_ev += value

        if total_ev > MAX_TOTAL_EV:
            raise ValueError(f"Total EVs cannot exceed {MAX_TOTAL_EV}, got {total_ev}")
