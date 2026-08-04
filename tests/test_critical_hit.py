from battle.battle_context import BattleContext
from battle.stub_rng import StubRNG


def test_critical_hit_deals_more_damage(
    garchomp,
    opponent_garchomp,
    earthquake,
    battle_state,
):
    normal_rng = StubRNG(
        accuracy_rolls=[0.0],
        critical_rolls=[1.0],
        damage_rolls=[1.0],
    )

    crit_rng = StubRNG(
        accuracy_rolls=[0.0],
        critical_rolls=[0.0],
        damage_rolls=[1.0],
    )

    opponent_garchomp.current_hp = opponent_garchomp.stats.hp

    earthquake.apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        battle_context=BattleContext(battle_state, normal_rng),
    )

    normal_damage = opponent_garchomp.stats.hp - opponent_garchomp.current_hp

    opponent_garchomp.current_hp = opponent_garchomp.stats.hp

    earthquake.apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        battle_context=BattleContext(battle_state, crit_rng),
    )

    crit_damage = opponent_garchomp.stats.hp - opponent_garchomp.current_hp

    assert crit_damage > normal_damage
