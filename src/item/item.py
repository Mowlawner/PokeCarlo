from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Item:
    """Static metadata for a Pokémon item."""

    name: str
    display_name: str
    id: int
    category: str
    attributes: tuple[str, ...]

    def __post_init__(self) -> None:
        if isinstance(self.id, bool) or not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("Item ID must be a positive integer.")

        for field_name in ("name", "display_name", "category"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Item {field_name} must be a non-empty string.")

        if not isinstance(self.attributes, tuple):
            raise TypeError("Item attributes must be a tuple.")
        if any(
            not isinstance(attribute, str) or not attribute.strip()
            for attribute in self.attributes
        ):
            raise ValueError("Item attributes must be non-empty strings.")
        if len(set(self.attributes)) != len(self.attributes):
            raise ValueError("Item attributes cannot contain duplicates.")
