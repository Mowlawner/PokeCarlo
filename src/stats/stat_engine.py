from enum import Enum, auto
from typing import TYPE_CHECKING

from battle.battle_context import BattleContext
from move import MoveCategory
from move.move_context import MoveContext
from stats.stat import Stat
from stats.stat_utils import get_stage, stage_multiplier
from status_condition import StatusCondition

if TYPE_CHECKING:
    from pokemon import Pokemon


class StatRole(Enum):
    OFFENSE = auto()
    DEFENSE = auto()


def get_effective_stat(
    pokemon: "Pokemon",
    stat: Stat,
    role: StatRole,
    battle_context: BattleContext,
    move_context: MoveContext | None = None,
) -> int:
    """
    Returns the Pokémon's effective value for the requested stat in the
    current battle state.

    This applies all modifiers that affect the stat at the moment it is
    queried, including (as implemented):

    - Stat stage modifiers
    - Status effects (e.g. burn)
    - Ability modifiers
    - Item modifiers
    - Field and battle effects

    The requested role determines whether offensive or defensive modifiers
    should be applied when they differ. For example, burn only affects a
    Pokémon's offensive Attack, while abilities such as Ice Scales modify
    defensive calculations.

    The optional MoveContext allows move-dependent effects (such as burn
    only affecting physical attacks) to be evaluated.
    """
    value = pokemon.stats.get(stat)

    # Apply stat stage modifier.
    stage = get_stage(pokemon.stat_stages, stat)
    value = int(value * stage_multiplier(stat, stage))

    if (
        role is StatRole.OFFENSE
        and stat is Stat.ATTACK
        and move_context is not None
        and move_context.move_type is MoveCategory.PHYSICAL
        and pokemon.status is StatusCondition.BURN
    ):
        value //= 2

    return value
