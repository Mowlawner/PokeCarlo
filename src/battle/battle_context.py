from dataclasses import dataclass

from battle.battle_state import BattleState
from battle.rng import RNG
from move import MoveTarget
from pokemon import Pokemon


@dataclass
class BattleContext:
    state: BattleState
    rng: RNG

    def get_targets(
        self,
        user: Pokemon,
        targeting: MoveTarget,
        selected_target: Pokemon | None = None,
    ) -> tuple[Pokemon, ...]:
        player_active = self.state.player_active
        opponent_active = self.state.opponent_active

        if self.is_player_pokemon(user):
            allies = player_active
            opponents = opponent_active
        else:
            allies = opponent_active
            opponents = player_active

        living_allies = tuple(pokemon for pokemon in allies if not pokemon.is_fainted)

        living_opponents = tuple(
            pokemon for pokemon in opponents if not pokemon.is_fainted
        )

        match targeting:
            case MoveTarget.SINGLE_TARGET:
                if selected_target is not None:
                    if selected_target not in living_opponents:
                        raise ValueError(
                            "Selected target is not a valid living opponent."
                        )

                    return (selected_target,)

                return living_opponents

            case MoveTarget.SELF:
                return (user,)

            case MoveTarget.ALL_OTHERS:
                return tuple(
                    pokemon
                    for pokemon in (*living_allies, *living_opponents)
                    if pokemon is not user
                )

            case MoveTarget.ALL:
                return (*living_allies, *living_opponents)

            case MoveTarget.ALL_OPPONENTS:
                return living_opponents

            case MoveTarget.ALL_ALLIES:
                return tuple(
                    pokemon for pokemon in living_allies if pokemon is not user
                )

            case MoveTarget.RANDOM_OPPONENT:
                return living_opponents

            case MoveTarget.FIELD:
                raise NotImplementedError()

            case _:
                raise ValueError(f"Invalid targeting {targeting}.")

    def is_player_pokemon(
        self,
        pokemon: Pokemon,
    ) -> bool:
        return any(active is pokemon for active in self.state.player_active)

    def get_bench(
        self,
        pokemon: Pokemon,
    ) -> tuple[Pokemon, ...]:
        if self.is_player_pokemon(pokemon):
            return self.state.player_bench

        if any(active is pokemon for active in self.state.opponent_active):
            return self.state.opponent_bench

        raise ValueError("Pokémon is not currently active.")
