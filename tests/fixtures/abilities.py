import pytest

from abilities.intimidate import INTIMIDATE
from abilities.not_implemented_abilities import (
    MOXIE,
    ROUGH_SKIN,
    SAND_STREAM,
    SAND_VEIL,
    UNNERVE,
)


@pytest.fixture
def rough_skin():
    return ROUGH_SKIN


@pytest.fixture
def sand_veil():
    return SAND_VEIL


@pytest.fixture
def moxie():
    return MOXIE


@pytest.fixture
def intimidate():
    return INTIMIDATE


@pytest.fixture
def sand_stream():
    return SAND_STREAM


@pytest.fixture
def unnerve():
    return UNNERVE
