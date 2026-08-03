from battle import Action, BattleState
from battle_ai.ai import AI


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


def execute_move():
    pass


def check_faints():
    pass


def increment_turn():
    pass


def execute_turn(
    state: BattleState,
    player_action: Action,
    opponent_action: Action,
):
    determine_order()

    execute_move()

    check_faints()

    increment_turn()
