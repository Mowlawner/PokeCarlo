from battle import BattleState
from battle.action import SwitchAction
from battle.battle_context import BattleContext
from battle.battle_resolver import BattleResolver
from battle.stub_rng import StubRNG


def test_player_switching_works(
    garchomp,
    gyarados,
    opponent_garchomp,
):
    battle_state = BattleState(
        player_active=(garchomp,),
        opponent_active=(opponent_garchomp,),
        player_party=(garchomp, gyarados),
    )
    battle_context = BattleContext(
        state=battle_state,
        rng=StubRNG(),
    )
    battle_resolver = BattleResolver(context=battle_context)

    action = SwitchAction(
        actor=garchomp,
        incoming=gyarados,
    )

    battle_resolver.resolve_turn(actions=(action,))

    assert battle_state.player_active == (gyarados,)


def test_opponent_switching_works(
    garchomp,
    opponent_garchomp,
    gyarados,
):
    battle_state = BattleState(
        player_active=(garchomp,),
        opponent_active=(opponent_garchomp,),
        opponent_party=(
            opponent_garchomp,
            gyarados,
        ),
    )
    battle_context = BattleContext(
        state=battle_state,
        rng=StubRNG(),
    )
    battle_resolver = BattleResolver(context=battle_context)

    action = SwitchAction(
        actor=opponent_garchomp,
        incoming=gyarados,
    )

    battle_resolver.resolve_turn(actions=(action,))

    assert battle_state.opponent_active == (gyarados,)


def test_switching_triggers_incoming_switch_in_ability(
    garchomp,
    gyarados,
    opponent_garchomp,
    monkeypatch,
):
    called = {}

    def on_switch_in(
        *,
        pokemon,
        battle_context,
    ):
        called["pokemon"] = pokemon
        called["battle_context"] = battle_context

    monkeypatch.setattr(
        gyarados.pokemon_set.ability,
        "on_switch_in",
        on_switch_in,
    )

    battle_state = BattleState(
        player_active=(garchomp,),
        opponent_active=(opponent_garchomp,),
        player_party=(garchomp, gyarados),
    )
    battle_context = BattleContext(
        state=battle_state,
        rng=StubRNG(),
    )
    battle_resolver = BattleResolver(context=battle_context)

    action = SwitchAction(
        actor=garchomp,
        incoming=gyarados,
    )

    battle_resolver.resolve_turn(actions=(action,))

    assert called["pokemon"] is gyarados
    assert called["battle_context"] is battle_context
