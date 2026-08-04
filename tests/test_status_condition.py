from battle.battle_context import BattleContext
from battle.stub_rng import StubRNG
from move import MoveCategory
from move.move_context import MoveContext
from pokemon_types import Type
from stats.stat import Stat
from stats.stat_engine import StatRole, get_effective_stat
from status_condition import StatusCondition


def test_pokemon_starts_without_status(garchomp):
    assert garchomp.status is StatusCondition.NONE


def test_pokemon_can_be_burned(garchomp):
    garchomp.status = StatusCondition.BURN

    assert garchomp.status is StatusCondition.BURN


def test_burn_halves_offensive_physical_attack(
    garchomp,
    battle_state,
):
    garchomp.status = StatusCondition.BURN

    value = get_effective_stat(
        pokemon=garchomp,
        stat=Stat.ATTACK,
        role=StatRole.OFFENSE,
        battle_context=BattleContext(
            battle_state,
            StubRNG(),
        ),
        move_context=MoveContext(
            move_type=Type.GROUND,
            move_category=MoveCategory.PHYSICAL,
        ),
    )

    assert value == garchomp.stats.attack // 2


def test_burn_does_not_halve_special_attack(
    garchomp,
    battle_state,
):
    garchomp.status = StatusCondition.BURN

    value = get_effective_stat(
        pokemon=garchomp,
        stat=Stat.SP_ATTACK,
        role=StatRole.OFFENSE,
        battle_context=BattleContext(
            battle_state,
            StubRNG(),
        ),
        move_context=MoveContext(
            move_type=Type.GROUND,
            move_category=MoveCategory.SPECIAL,
        ),
    )

    assert value == garchomp.stats.sp_attack


def test_burn_does_not_affect_defensive_stats(
    garchomp,
    battle_state,
):
    garchomp.status = StatusCondition.BURN

    value = get_effective_stat(
        pokemon=garchomp,
        stat=Stat.DEFENSE,
        role=StatRole.DEFENSE,
        battle_context=BattleContext(
            battle_state,
            StubRNG(),
        ),
    )

    assert value == garchomp.stats.defense


def test_burn_affects_body_press(
    garchomp,
    battle_state,
):
    garchomp.status = StatusCondition.BURN

    value = get_effective_stat(
        pokemon=garchomp,
        stat=Stat.DEFENSE,
        role=StatRole.OFFENSE,
        battle_context=BattleContext(
            battle_state,
            StubRNG(),
        ),
        move_context=MoveContext(
            move_type=Type.FIGHTING,
            move_category=MoveCategory.PHYSICAL,
        ),
    )

    assert value == garchomp.stats.defense // 2
