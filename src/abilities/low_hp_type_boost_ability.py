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


@dataclass(frozen=True, slots=True)
class Torrent(LowHPTypeBoostAbility):
    name = "Torrent"


TORRENT = Torrent(
    boost_type=Type.WATER,
)


@dataclass(frozen=True, slots=True)
class Overgrow(LowHPTypeBoostAbility):
    name = "Overgrow"


OVERGROW = Overgrow(
    boost_type=Type.GRASS,
)


@dataclass(frozen=True, slots=True)
class Blaze(LowHPTypeBoostAbility):
    name = "Blaze"


BLAZE = Blaze(boost_type=Type.FIRE)
