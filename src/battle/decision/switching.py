from battle import BattleContext
from pokemon import Pokemon


def get_available_switches(
    *,
    battle_context: BattleContext,
    pokemon: Pokemon,
) -> tuple[Pokemon, ...]: ...
