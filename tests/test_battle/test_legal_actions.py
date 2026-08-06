from battle import BattleContext, BattleState, StubRNG
from battle.action import MoveAction, SwitchAction
from battle.decision.legal_actions import get_legal_actions


def test_get_legal_actions_returns_moves(
    battle_context,
    garchomp,
):
    actions = get_legal_actions(
        battle_context=battle_context,
        pokemon=garchomp,
    )

    assert len(actions) == len(garchomp.pokemon_set.moves)
    assert all(isinstance(action, MoveAction) for action in actions)


def test_move_actions_reference_actor(
    battle_context,
    garchomp,
):
    actions = get_legal_actions(
        battle_context=battle_context,
        pokemon=garchomp,
    )

    for action in actions:
        assert action.actor is garchomp


def test_single_bench_pokemon_creates_single_switch_action(
    garchomp,
    gyarados,
):
    battle_state = BattleState(
        player_active=(garchomp,),
        opponent_active=(),
        player_party=(garchomp, gyarados),
        opponent_party=(),
    )

    battle_context = BattleContext(
        state=battle_state,
        rng=StubRNG(),
    )

    actions = get_legal_actions(
        battle_context=battle_context,
        pokemon=garchomp,
    )

    switch_actions = tuple(
        action for action in actions if isinstance(action, SwitchAction)
    )

    assert len(switch_actions) == 1
    assert switch_actions[0].incoming is gyarados


def test_multiple_bench_pokemon_create_multiple_switch_actions(
    garchomp,
    gyarados,
    tyranitar,
):
    battle_state = BattleState(
        player_active=(garchomp,),
        opponent_active=(),
        player_party=(garchomp, gyarados, tyranitar),
        opponent_party=(),
    )

    battle_context = BattleContext(
        state=battle_state,
        rng=StubRNG(),
    )

    actions = get_legal_actions(
        battle_context=battle_context,
        pokemon=garchomp,
    )

    switch_actions = tuple(
        action for action in actions if isinstance(action, SwitchAction)
    )

    assert len(switch_actions) == 2
    assert sum(action.incoming is gyarados for action in switch_actions) == 1
    assert sum(action.incoming is tyranitar for action in switch_actions) == 1


def test_no_bench_pokemon_creates_no_switch_actions(
    garchomp,
):
    battle_state = BattleState(
        player_active=(garchomp,),
        opponent_active=(),
        player_party=(garchomp,),
        opponent_party=(),
    )

    battle_context = BattleContext(
        state=battle_state,
        rng=StubRNG(),
    )

    actions = get_legal_actions(
        battle_context=battle_context,
        pokemon=garchomp,
    )

    assert not any(isinstance(action, SwitchAction) for action in actions)


def test_legal_actions_returns_moves_and_switches(
    garchomp,
    gyarados,
):
    battle_state = BattleState(
        player_active=(garchomp,),
        opponent_active=(),
        player_party=(garchomp, gyarados),
        opponent_party=(),
    )

    battle_context = BattleContext(
        state=battle_state,
        rng=StubRNG(),
    )

    actions = get_legal_actions(
        battle_context=battle_context,
        pokemon=garchomp,
    )

    move_actions = [action for action in actions if isinstance(action, MoveAction)]

    switch_actions = [action for action in actions if isinstance(action, SwitchAction)]

    assert len(move_actions) == len(garchomp.pokemon_set.moves)
    assert len(switch_actions) == 1


def test_switch_action_actor_is_the_active_pokemon(
    garchomp,
    gyarados,
):
    battle_state = BattleState(
        player_active=(garchomp,),
        opponent_active=(),
        player_party=(garchomp, gyarados),
        opponent_party=(),
    )

    battle_context = BattleContext(
        state=battle_state,
        rng=StubRNG(),
    )

    actions = get_legal_actions(
        battle_context=battle_context,
        pokemon=garchomp,
    )

    switch_actions = tuple(
        action for action in actions if isinstance(action, SwitchAction)
    )

    assert switch_actions[0].actor is garchomp


def test_opponent_receives_switch_actions_from_opponent_party(
    opponent_garchomp,
    gyarados,
):
    battle_state = BattleState(
        player_active=(),
        opponent_active=(opponent_garchomp,),
        player_party=(),
        opponent_party=(opponent_garchomp, gyarados),
    )

    battle_context = BattleContext(
        state=battle_state,
        rng=StubRNG(),
    )

    actions = get_legal_actions(
        battle_context=battle_context,
        pokemon=opponent_garchomp,
    )

    switch_actions = tuple(
        action for action in actions if isinstance(action, SwitchAction)
    )

    assert len(switch_actions) == 1
    assert switch_actions[0].incoming is gyarados
    assert switch_actions[0].actor is opponent_garchomp


def test_switch_actions_do_not_include_active_teammates(
    garchomp,
    gyarados,
    tyranitar,
):
    battle_state = BattleState(
        player_active=(garchomp, gyarados),
        opponent_active=(),
        player_party=(garchomp, gyarados, tyranitar),
        opponent_party=(),
    )

    battle_context = BattleContext(
        state=battle_state,
        rng=StubRNG(),
    )

    actions = get_legal_actions(
        battle_context=battle_context,
        pokemon=garchomp,
    )

    switch_actions = tuple(
        action for action in actions if isinstance(action, SwitchAction)
    )

    assert len(switch_actions) == 1
    assert switch_actions[0].incoming is tyranitar
