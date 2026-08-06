import pytest

from stats.ivs import IVs


def test_iv_cannot_exceed_31():
    with pytest.raises(ValueError):
        IVs(
            hp=32,
            attack=0,
            defense=0,
            sp_attack=0,
            sp_defense=0,
            speed=0,
        )


def test_iv_cannot_be_negative():
    with pytest.raises(ValueError):
        IVs(
            hp=-1,
            attack=0,
            defense=0,
            sp_attack=0,
            sp_defense=0,
            speed=0,
        )
