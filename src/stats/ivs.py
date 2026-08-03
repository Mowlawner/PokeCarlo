from dataclasses import dataclass, fields

MIN_IV = 0
MAX_IV = 31


@dataclass(slots=True, frozen=True)
class IVs:
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int

    def __post_init__(self) -> None:
        for field in fields(self):
            value = getattr(self, field.name)

            if not MIN_IV <= value <= MAX_IV:
                raise ValueError(
                    f"{field.name} IV must be between {MIN_IV} and {MAX_IV}, got {value}"
                )
