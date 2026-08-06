import pytest

from stats.evs import EVs


def test_ev_cannot_exceed_252():
    with pytest.raises(ValueError):
        EVs(
            hp=253,
            attack=0,
            defense=0,
            sp_attack=0,
            sp_defense=0,
            speed=0,
        )


def test_total_evs_cannot_exceed_510():
    with pytest.raises(ValueError):
        EVs(
            hp=252,
            attack=252,
            defense=252,
            sp_attack=0,
            sp_defense=0,
            speed=0,
        )
