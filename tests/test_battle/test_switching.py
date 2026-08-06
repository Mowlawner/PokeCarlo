from battle import BattleState
from battle.battle_context import BattleContext
from battle.battle_resolver import BattleResolver
from battle.stub_rng import StubRNG


def test_player_switching_works(garchomp, gyarados, opponent_garchomp):
    battle_state = BattleState(
        player_active=(garchomp,),
        opponent_active=(opponent_garchomp,),
    )
    battle_context = BattleContext(state=battle_state, rng=StubRNG())
    battle_resolver = BattleResolver(context=battle_context)
    battle_resolver.switch(
        outgoing=garchomp,
        incoming=gyarados,
    )

    assert battle_state.player_active == (gyarados,)


def test_opponent_switching_works(garchomp, opponent_garchomp, gyarados):
    battle_state = BattleState(
        player_active=(garchomp,), opponent_active=(opponent_garchomp,)
    )
    battle_context = BattleContext(state=battle_state, rng=StubRNG())
    battle_resolver = BattleResolver(context=battle_context)
    battle_resolver.switch(
        outgoing=opponent_garchomp,
        incoming=gyarados,
    )

    assert garchomp == opponent_garchomp
    assert garchomp is not opponent_garchomp
    assert battle_state.opponent_active == (gyarados,)
