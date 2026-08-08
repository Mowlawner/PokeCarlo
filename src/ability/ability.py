from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Ability:
    name: str
    display_name: str
    id: int
    generation: str

    def __post_init__(self) -> None:
        if isinstance(self.id, bool) or not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("Ability ID must be a positive integer.")

        for field_name in ("name", "display_name", "generation"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Ability {field_name} must be a non-empty string.")
