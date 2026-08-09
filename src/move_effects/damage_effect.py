from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from damage_calculator import calculate_damage
from move.move_category import MoveCategory
from move.move_context import MoveContext
from pokemon_types.type_chart import effectiveness
from stats.stat import Stat
from stats.stat_engine import StatRole, get_effective_stat

if TYPE_CHECKING:
    from battle.battle_context import BattleContext
    from pokemon import Pokemon


CRIT_CHANCE = 1 / 24


@dataclass(frozen=True, slots=True)
class DamageEffect:
    power: int
    attacking_stat: Stat | None = None
    defending_stat: Stat | None = None

    def __post_init__(self):
        if self.power < 0:
            raise ValueError("Move power cannot be negative.")

    def apply(
        self,
        user: "Pokemon",
        targets: tuple["Pokemon", ...],
        move_context: MoveContext,
        battle_context: "BattleContext",
    ) -> None:
        stab = 1.5 if move_context.move_type in user.pokemon_set.species.types else 1.0

        for target in targets:
            type_effectiveness = effectiveness(
                move_context.move_type, target.pokemon_set.species.types
            )

            is_critical = battle_context.rng.critical_roll() < CRIT_CHANCE

            damage = calculate_damage(
                level=user.pokemon_set.level,
                power=self.power,
                attack=get_effective_stat(
                    pokemon=user,
                    stat=self.attacking_stat,
                    role=StatRole.OFFENSE,
                    battle_context=battle_context,
                    move_context=move_context,
                ),
                defense=get_effective_stat(
                    pokemon=target,
                    stat=self.defending_stat,
                    role=StatRole.DEFENSE,
                    battle_context=battle_context,
                    move_context=move_context,
                ),
                stab=stab,
                effectiveness=type_effectiveness,
                random=battle_context.rng.damage_roll(),
                critical=is_critical,
            )

            damage = user.ability.modify_outgoing_damage(
                damage=damage,
                user=user,
                target=target,
                move_context=move_context,
                battle_context=battle_context,
            )

            damage = target.ability.modify_incoming_damage(
                damage=damage,
                user=user,
                target=target,
                move_context=move_context,
                battle_context=battle_context,
            )

            target.take_damage(damage)


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
