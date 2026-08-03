from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from move.move_category import MoveCategory
from stats.stat import Stat

if TYPE_CHECKING:
    from pokemon import Pokemon


@dataclass(frozen=True, slots=True)
class DamageEffect:
    attacking_stat: Stat | None = None
    defending_stat: Stat | None = None

    def apply(
        self,
        user: "Pokemon",
        targets: tuple["Pokemon", ...],
    ) -> None:
        # TODO:
        # for target in targets:
        #     damage = calculate_damage(
        #         user=user,
        #         target=target,
        #         attacking_stat=self.attacking_stat,
        #         defending_stat=self.defending_stat,
        #     )
        #
        #     target.current_hp -= damage
        pass


def resolve_defaults(
    effect: DamageEffect,
    category: MoveCategory,
) -> DamageEffect:
    if category is MoveCategory.PHYSICAL:
        default_attack = Stat.ATTACK
        default_defense = Stat.DEFENSE
    elif category is MoveCategory.SPECIAL:
        default_attack = Stat.SP_ATTACK
        default_defense = Stat.SP_DEFENSE
    else:
        # Status moves shouldn't have DamageEffects, but don't explode
        # if one accidentally gets created.
        return effect

    return replace(
        effect,
        attacking_stat=(
            effect.attacking_stat
            if effect.attacking_stat is not None
            else default_attack
        ),
        defending_stat=(
            effect.defending_stat
            if effect.defending_stat is not None
            else default_defense
        ),
    )
