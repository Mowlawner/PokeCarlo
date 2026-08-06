from battle import BattleContext, BattleResolver, BattleState, StubRNG
from battle.action import MoveAction, SwitchAction


def test_battle_resolver_applies_action(
    battle_resolver,
    garchomp,
    opponent_garchomp,
    earthquake,
):
    action = MoveAction(
        actor=garchomp,
        move=earthquake,
        # target=opponent_garchomp,
    )

    starting_hp = opponent_garchomp.current_hp

    battle_resolver.resolve_turn(
        actions=(action,),
    )

    assert opponent_garchomp.current_hp < starting_hp


def test_battle_resolver_applies_multiple_actions(
    battle_resolver,
    garchomp,
    opponent_garchomp,
    tackle,
):
    player_action = MoveAction(
        actor=garchomp,
        move=tackle,
        target=opponent_garchomp,
    )

    opponent_action = MoveAction(
        actor=opponent_garchomp,
        move=tackle,
        target=garchomp,
    )

    starting_hp = garchomp.current_hp
    opponent_starting_hp = opponent_garchomp.current_hp

    battle_resolver.resolve_turn(
        actions=(
            player_action,
            opponent_action,
        ),
    )

    assert garchomp.current_hp < starting_hp
    assert opponent_garchomp.current_hp < opponent_starting_hp


def test_battle_resolver_gets_next_action(
    battle_resolver,
    garchomp,
    opponent_garchomp,
    earthquake,
):
    first_action = MoveAction(
        actor=garchomp,
        move=earthquake,
        # target=opponent_garchomp,
    )

    second_action = MoveAction(
        actor=opponent_garchomp,
        move=earthquake,
        # target=garchomp,
    )

    assert (
        battle_resolver.get_next_action(
            actions=(first_action, second_action),
        )
        is first_action
    )


def test_fainted_pokemon_cannot_apply_action(
    battle_context,
    garchomp,
    opponent_garchomp,
    earthquake,
):
    garchomp.current_hp = 0

    action = MoveAction(
        actor=garchomp,
        move=earthquake,
        # target=opponent_garchomp,
    )

    starting_hp = opponent_garchomp.current_hp

    action.apply(battle_context)

    assert opponent_garchomp.current_hp == starting_hp


def test_get_next_action_uses_speed_when_priorities_are_equal(
    battle_resolver,
    garchomp,
    adamant_garchomp,
    tackle,
):
    faster_pokemon_action = MoveAction(
        actor=garchomp,
        move=tackle,
    )

    slower_pokemon_action = MoveAction(
        actor=adamant_garchomp,
        move=tackle,
    )

    next_action = battle_resolver.get_next_action(
        [
            slower_pokemon_action,
            faster_pokemon_action,
        ]
    )

    assert next_action is faster_pokemon_action


def test_fainted_pokemon_is_added_to_pending_switches(
    battle_resolver,
    garchomp,
):
    garchomp.current_hp = 0

    battle_resolver.handle_faints()

    assert battle_resolver.context.state.pending_switches == (garchomp,)


def test_fainted_pokemon_is_only_added_to_pending_switches_once(
    battle_resolver,
    garchomp,
):
    garchomp.current_hp = 0

    battle_resolver.handle_faints()
    battle_resolver.handle_faints()

    assert battle_resolver.context.state.pending_switches == (garchomp,)


def test_pending_switches_are_preserved_after_processing(
    battle_resolver,
    garchomp,
):
    garchomp.current_hp = 0

    battle_resolver.context.state.add_pending_switch(garchomp)

    assert battle_resolver.context.state.pending_switches == (garchomp,)

    battle_resolver.handle_pending_switches()

    assert battle_resolver.context.state.pending_switches == (garchomp,)


def test_switching_does_not_create_pending_switch(
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

    resolver = BattleResolver(context=battle_context)

    action = SwitchAction(
        actor=garchomp,
        incoming=gyarados,
    )

    resolver.resolve_turn(actions=(action,))

    assert battle_state.pending_switches == ()


def test_fainted_pokemon_does_not_execute_action(
    battle_context,
    garchomp,
    opponent_garchomp,
    earthquake,
):
    garchomp.current_hp = 0

    action = MoveAction(
        actor=garchomp,
        move=earthquake,
    )

    starting_hp = opponent_garchomp.current_hp

    action.apply(battle_context)

    assert opponent_garchomp.current_hp == starting_hp


def test_fainted_action_does_not_prevent_other_actions(
    battle_resolver,
    garchomp,
    opponent_garchomp,
    tackle,
):
    garchomp.current_hp = 0

    action = MoveAction(
        actor=garchomp,
        move=tackle,
        target=opponent_garchomp,
    )

    opponent_action = MoveAction(
        actor=opponent_garchomp,
        move=tackle,
        target=opponent_garchomp,
    )

    starting_hp = opponent_garchomp.current_hp

    battle_resolver.resolve_turn(
        actions=(
            action,
            opponent_action,
        ),
    )

    assert opponent_garchomp.current_hp < starting_hp


def test_fainted_pokemon_is_added_after_action_resolution(
    battle_resolver,
    garchomp,
):
    garchomp.current_hp = 0

    battle_resolver.resolve_turn(actions=())

    assert battle_resolver.context.state.pending_switches == (garchomp,)


def test_handle_faints_does_not_add_non_fainted_pokemon(
    battle_resolver,
    garchomp,
):
    battle_resolver.handle_faints()

    assert battle_resolver.context.state.pending_switches == ()


def test_switching_replaces_active_pokemon(
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

    resolver = BattleResolver(context=battle_context)

    action = SwitchAction(
        actor=garchomp,
        incoming=gyarados,
    )

    resolver.resolve_turn(actions=(action,))

    assert battle_state.player_active == (gyarados,)
    assert garchomp not in battle_state.player_active


def test_handle_pending_switches_does_nothing_without_pending_switches(
    battle_resolver,
):
    battle_resolver.handle_pending_switches()

    assert battle_resolver.context.state.pending_switches == ()
