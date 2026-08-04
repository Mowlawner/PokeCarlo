from battle.battle_context import BattleContext
from battle.stub_rng import StubRNG
from stats.stat import Stat
from stats.stat_engine import StatRole, get_effective_stat
from stats.stat_utils import modify_stage


def test_get_effective_stat_returns_base_stat_when_no_modifiers(
    garchomp,
    battle_state,
):
    value = get_effective_stat(
        pokemon=garchomp,
        stat=Stat.ATTACK,
        role=StatRole.OFFENSE,
        battle_context=BattleContext(
            battle_state,
            StubRNG(),
        ),
    )

    assert value == garchomp.stats.attack


def test_get_effective_stat_applies_positive_stat_stage(
    garchomp,
    battle_state,
):
    modify_stage(
        garchomp.stat_stages,
        Stat.ATTACK,
        2,
    )

    value = get_effective_stat(
        pokemon=garchomp,
        stat=Stat.ATTACK,
        role=StatRole.OFFENSE,
        battle_context=BattleContext(
            battle_state,
            StubRNG(),
        ),
    )

    assert value == int(garchomp.stats.attack * 2.0)


def test_get_effective_stat_applies_negative_stat_stage(
    garchomp,
    battle_state,
):
    modify_stage(
        garchomp.stat_stages,
        Stat.DEFENSE,
        -1,
    )

    value = get_effective_stat(
        pokemon=garchomp,
        stat=Stat.DEFENSE,
        role=StatRole.DEFENSE,
        battle_context=BattleContext(
            battle_state,
            StubRNG(),
        ),
    )

    assert value == int(garchomp.stats.defense * (2 / 3))


def test_get_effective_stat_uses_runtime_stat_stages(
    garchomp,
    battle_state,
):
    base_value = get_effective_stat(
        pokemon=garchomp,
        stat=Stat.SPEED,
        role=StatRole.OFFENSE,
        battle_context=BattleContext(
            battle_state,
            StubRNG(),
        ),
    )

    modify_stage(
        garchomp.stat_stages,
        Stat.SPEED,
        1,
    )

    boosted_value = get_effective_stat(
        pokemon=garchomp,
        stat=Stat.SPEED,
        role=StatRole.OFFENSE,
        battle_context=BattleContext(
            battle_state,
            StubRNG(),
        ),
    )

    assert boosted_value > base_value
