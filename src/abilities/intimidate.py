from typing import TYPE_CHECKING

from abilities.ability import Ability
from stats.stat import Stat
from stats.stat_utils import modify_stage

if TYPE_CHECKING:
    from battle.battle_context import BattleContext
    from pokemon import Pokemon


class Intimidate(Ability):
    name = "Intimidate"

    def on_switch_in(
        self,
        pokemon: "Pokemon",
        battle_context: "BattleContext",
    ) -> None:
        for opponent in battle_context.state.opponent_active:
            modify_stage(
                opponent.stat_stages,
                Stat.ATTACK,
                -1,
            )


INTIMIDATE = Intimidate()
