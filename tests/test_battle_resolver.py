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
