import pytest

from battle import RNG, BattleContext, BattleResolver, BattleState


@pytest.fixture
def battle_state(
    garchomp,
    ally_garchomp,
    opponent_garchomp,
    second_opponent_garchomp,
) -> BattleState:
    return BattleState(
        player_active=(
            garchomp,
            ally_garchomp,
        ),
        opponent_active=(
            opponent_garchomp,
            second_opponent_garchomp,
        ),
    )


@pytest.fixture
def battle_context(battle_state: BattleState) -> BattleContext:
    return BattleContext(battle_state, rng=RNG(42))


@pytest.fixture
def battle_resolver(battle_context) -> BattleResolver:
    return BattleResolver(battle_context)
