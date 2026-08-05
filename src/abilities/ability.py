from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from battle.battle_context import BattleContext
    from move.move_context import MoveContext
    from pokemon import Pokemon
    from stats.stat import Stat
    from stats.stat_engine import StatRole


@dataclass(frozen=True, slots=True)
class Ability(ABC):
    name: str

    def on_switch_in(
        self,
        pokemon: "Pokemon",
        battle_context: "BattleContext",
    ) -> None:
        pass

    def modify_effective_stat(
        self,
        *,
        value: int,
        pokemon: "Pokemon",
        stat: "Stat",
        role: "StatRole",
        move_context: "MoveContext | None",
        battle_context: "BattleContext",
    ) -> int:
        return value

    def modify_outgoing_damage(
        self,
        *,
        damage: int,
        user: "Pokemon",
        target: "Pokemon",
        move_context: "MoveContext",
        battle_context: "BattleContext",
    ) -> int:
        return damage

    def modify_incoming_damage(
        self,
        *,
        damage: int,
        user: "Pokemon",
        target: "Pokemon",
        move_context: "MoveContext",
        battle_context: "BattleContext",
    ) -> int:
        return damage
