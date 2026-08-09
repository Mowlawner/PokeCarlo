import pytest

from ability import Ability

_ABILITY_DATA = {
    "ROUGH_SKIN": (17, "Rough Skin"),
    "SAND_VEIL": (8, "Sand Veil"),
    "MOXIE": (153, "Moxie"),
    "INTIMIDATE": (22, "Intimidate"),
    "SAND_STREAM": (45, "Sand Stream"),
    "UNNERVE": (127, "Unnerve"),
}


def _static_ability(name: str) -> Ability:
    ability_id, display_name = _ABILITY_DATA[name]
    return Ability(
        name=name,
        display_name=display_name,
        id=ability_id,
        generation="GENERATION_III",
    )


@pytest.fixture
def rough_skin():
    return _static_ability("ROUGH_SKIN")


@pytest.fixture
def sand_veil():
    return _static_ability("SAND_VEIL")


@pytest.fixture
def moxie():
    return _static_ability("MOXIE")


@pytest.fixture
def intimidate():
    return _static_ability("INTIMIDATE")


@pytest.fixture
def sand_stream():
    return _static_ability("SAND_STREAM")


@pytest.fixture
def unnerve():
    return _static_ability("UNNERVE")
