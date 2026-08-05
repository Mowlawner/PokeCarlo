from dataclasses import dataclass

from abilities.ability import Ability
from pokemon_types import Type


@dataclass(frozen=True, slots=True)
class LowHPTypeBoostAbility(Ability):
    """
    Boosts moves of a specific type by 50% when HP is at or below 1/3.
    """

    boost_type: Type

    def modify_outgoing_damage(
        self,
        *,
        damage: int,
        user,
        target,
        move_context,
        battle_context,
    ) -> int:
        if (
            user.current_hp <= user.stats.hp // 3
            and move_context.move_type is self.boost_type
        ):
            return int(damage * 1.5)

        return damage


TORRENT = LowHPTypeBoostAbility(
    name="Torrent",
    boost_type=Type.WATER,
)

OVERGROW = LowHPTypeBoostAbility(
    name="Overgrow",
    boost_type=Type.GRASS,
)

BLAZE = LowHPTypeBoostAbility(
    name="Blaze",
    boost_type=Type.FIRE,
)
