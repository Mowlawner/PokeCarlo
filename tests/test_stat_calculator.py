from stats.base_stats import BaseStats
from stats.evs import EVs
from stats.ivs import IVs
from stats.nature import Nature
from stats.stat_calculator import calculate_hp, calculate_non_hp_stat, calculate_stats


def test_hp_calculation():
    assert (
        calculate_hp(
            base=108,
            iv=31,
            ev=4,
            level=50,
        )
        == 184
    )


def test_non_hp_calculation():
    assert (
        calculate_non_hp_stat(
            base=130,
            iv=31,
            ev=252,
            level=50,
            nature_modifier=1.0,
        )
        == 182
    )


def test_jolly_garchomp():
    base_stats = BaseStats(
        hp=108,
        attack=130,
        defense=95,
        sp_attack=80,
        sp_defense=85,
        speed=102,
    )

    ivs = IVs(
        hp=31,
        attack=31,
        defense=31,
        sp_attack=31,
        sp_defense=31,
        speed=31,
    )

    evs = EVs(
        hp=4,
        attack=252,
        defense=0,
        sp_attack=0,
        sp_defense=0,
        speed=252,
    )

    stats = calculate_stats(
        base_stats=base_stats,
        ivs=ivs,
        evs=evs,
        nature=Nature.JOLLY,
        level=50,
    )

    assert stats.hp == 184
    assert stats.attack == 182
    assert stats.defense == 115
    assert stats.sp_attack == 90
    assert stats.sp_defense == 105
    assert stats.speed == 169


def test_neutral_nature_does_not_modify_stat():
    assert (
        calculate_non_hp_stat(
            base=100,
            iv=31,
            ev=252,
            level=50,
            nature_modifier=1.0,
        )
        == 152
    )


def test_hindering_nature_reduces_stat():

    hindered = calculate_non_hp_stat(
        base=100,
        iv=31,
        ev=252,
        level=50,
        nature_modifier=0.9,
    )

    assert hindered == 136


def test_boosting_nature_increases_stat():

    boosted = calculate_non_hp_stat(
        base=100,
        iv=31,
        ev=252,
        level=50,
        nature_modifier=1.1,
    )

    assert boosted == 167


def test_no_investment_stat():
    assert (
        calculate_non_hp_stat(
            base=100,
            iv=0,
            ev=0,
            level=50,
            nature_modifier=1.0,
        )
        == 105
    )


def test_non_hp_stat_simple_case():
    assert (
        calculate_non_hp_stat(
            base=50,
            iv=0,
            ev=0,
            level=50,
            nature_modifier=1.0,
        )
        == 55
    )
