from abilities.ability import Ability
from abilities.intimidate import INTIMIDATE
from abilities.low_hp_type_boost_ability import BLAZE, OVERGROW, TORRENT
from abilities.not_implemented_abilities import (
    MOXIE,
    ROUGH_SKIN,
    SAND_STREAM,
    SAND_VEIL,
    UNNERVE,
)

_ABILITIES = {
    ability.name: ability
    for ability in (
        INTIMIDATE,
        TORRENT,
        OVERGROW,
        BLAZE,
        ROUGH_SKIN,
        SAND_VEIL,
        MOXIE,
        SAND_STREAM,
        UNNERVE,
    )
}


def resolve_ability(name: str) -> Ability:
    """Resolve a canonical name to its runtime behavioral ability."""
    try:
        return _ABILITIES[name]
    except KeyError as error:
        raise ValueError(
            f"No behavioral implementation for ability {name!r}."
        ) from error
