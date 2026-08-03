from battle import Action
from battle.action import ActionType


def test_battle_resolver_applies_action(
    battle_resolver,
    garchomp,
    opponent_garchomp,
    earthquake,
):
    action = Action(
        action=ActionType.MOVE,
        pokemon=garchomp,
        move=earthquake,
        target=opponent_garchomp,
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
    earthquake,
):
    player_action = Action(
        action=ActionType.MOVE,
        pokemon=garchomp,
        move=earthquake,
        target=opponent_garchomp,
    )

    opponent_action = Action(
        action=ActionType.MOVE,
        pokemon=opponent_garchomp,
        move=earthquake,
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
    first_action = Action(
        action=ActionType.MOVE,
        pokemon=garchomp,
        move=earthquake,
        target=opponent_garchomp,
    )

    second_action = Action(
        action=ActionType.MOVE,
        pokemon=opponent_garchomp,
        move=earthquake,
        target=garchomp,
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

    action = Action(
        action=ActionType.MOVE,
        pokemon=garchomp,
        move=earthquake,
        target=opponent_garchomp,
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
    faster_pokemon_action = Action(
        action=ActionType.MOVE,
        pokemon=garchomp,
        move=tackle,
        target=adamant_garchomp,
    )

    slower_pokemon_action = Action(
        action=ActionType.MOVE,
        pokemon=adamant_garchomp,
        move=tackle,
        target=garchomp,
    )

    next_action = battle_resolver.get_next_action(
        [
            slower_pokemon_action,
            faster_pokemon_action,
        ]
    )

    assert next_action is faster_pokemon_action
