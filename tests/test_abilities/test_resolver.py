import pytest

from abilities.intimidate import Intimidate
from abilities.low_hp_type_boost_ability import Blaze
from abilities.not_implemented_abilities import RoughSkin
from abilities.resolver import resolve_ability


@pytest.mark.parametrize(
    ("name", "ability_type"),
    [
        ("INTIMIDATE", Intimidate),
        ("BLAZE", Blaze),
        ("ROUGH_SKIN", RoughSkin),
    ],
)
def test_resolve_ability_returns_behavioral_implementation(name, ability_type):
    assert isinstance(resolve_ability(name), ability_type)


def test_resolve_ability_rejects_unknown_name():
    with pytest.raises(ValueError, match="No behavioral implementation"):
        resolve_ability("NOT_AN_ABILITY")
