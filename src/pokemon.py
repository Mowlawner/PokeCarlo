from dataclasses import dataclass

from abilities.ability import Ability
from abilities.resolver import resolve_ability
from pokemon_set import PokemonSet
from stats.stat_calculator import calculate_stats
from stats.stat_stages import StatStages
from stats.stats import Stats
from status_condition import StatusCondition


@dataclass(slots=True)
class Pokemon:
    pokemon_set: PokemonSet
    ability: Ability

    stats: Stats
    current_hp: int

    stat_stages: StatStages

    status: StatusCondition = StatusCondition.NONE

    # later
    # volatile_effects: ...

    @classmethod
    def from_set(
        cls,
        pokemon_set: PokemonSet,
    ) -> "Pokemon":
        calculated_stats = calculate_stats(
            base_stats=pokemon_set.species.base_stats,
            ivs=pokemon_set.ivs,
            evs=pokemon_set.evs,
            nature=pokemon_set.nature,
            level=pokemon_set.level,
        )
        runtime_ability = resolve_ability(pokemon_set.ability.name)

        return cls(
            pokemon_set=pokemon_set,
            ability=runtime_ability,
            stats=calculated_stats,
            current_hp=calculated_stats.hp,
            stat_stages=StatStages(),
        )

    @property
    def is_fainted(self) -> bool:
        return self.current_hp <= 0

    def take_damage(self, amount: int) -> None:
        self.current_hp = max(0, self.current_hp - amount)
