from src.battle_ai.ai import AI
from src.battle_state import BattleState


def determine_order() -> list: ...


def execute(actions: list) -> None: ...


def apply_end_of_turn_effects() -> None: ...


def battle(ai1: AI, ai2: AI, battle_state: BattleState):
    while not battle_state.finished:
        ai1.choose_action(battle_state)
        ai2.choose_action(battle_state)

        order = determine_order()

        execute(order)

        apply_end_of_turn_effects()


"""
PSEUDO-CODE:
while both_alive:

    move1 = ai1.choose_move(...)

    move2 = ai2.choose_move(...)

    faster = compare_speed()

    faster attacks

    if defender fainted:
        break

    slower attacks

    turn += 1
"""
