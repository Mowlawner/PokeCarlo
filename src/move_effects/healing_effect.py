from dataclasses import dataclass
from typing import TYPE_CHECKING

from battle.battle_context import BattleContext
from move.move_context import MoveContext
from move_effects.move_effect import HPRecovered, MoveEffectResult

if TYPE_CHECKING:
    from pokemon import Pokemon


@dataclass(frozen=True, slots=True)
class HealingEffect:
    healing_percent: int = 50
    aggregate_damage: bool = False

    def __post_init__(self):
        if not 0 <= self.healing_percent <= 100:
            raise ValueError("Healing percentage must be between 0 and 100.")

    def apply(
        self,
        user: "Pokemon",
        targets: tuple["Pokemon", ...],
        move_context: MoveContext,
        battle_context: BattleContext,
        prior_results: tuple[MoveEffectResult, ...] = (),
    ) -> MoveEffectResult:
        damage_records = tuple(
            damage for result in prior_results for damage in result.damage_dealt
        )
        if not damage_records:
            return MoveEffectResult(applied=False)

        if not self.aggregate_damage:
            damage_records = damage_records[:1]

        damage = sum(record.amount for record in damage_records)
        requested_healing = damage * self.healing_percent // 100
        actual_healing = user.restore_hp(requested_healing)

        return MoveEffectResult(
            applied=actual_healing > 0,
            hp_restored=(HPRecovered(target=user, amount=actual_healing),),
        )
