import pytest

from stats.stat import Stat
from stats.stat_utils import stage_multiplier


def test_attack_stage_positive():
    assert stage_multiplier(
        Stat.ATTACK,
        2,
    ) == pytest.approx(2.0)


def test_attack_stage_negative():
    assert stage_multiplier(
        Stat.ATTACK,
        -1,
    ) == pytest.approx(2 / 3)


def test_accuracy_stage_positive():
    assert stage_multiplier(
        Stat.ACCURACY,
        2,
    ) == pytest.approx(5 / 3)


def test_evasion_stage_negative():
    assert stage_multiplier(
        Stat.EVASION,
        -1,
    ) == pytest.approx(3 / 4)


def test_stage_multiplier_rejects_invalid_stage():
    with pytest.raises(ValueError):
        stage_multiplier(
            Stat.ATTACK,
            9,
        )
