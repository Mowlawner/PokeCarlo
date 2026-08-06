from dataclasses import dataclass

from battle.battle_state import BattleState
from battle.rng import RNG
from move import MoveTarget
from pokemon import Pokemon


@dataclass
class BattleContext:
    state: BattleState
    rng: RNG

    def get_legal_targets(
        self,
        user: Pokemon,
        targeting: MoveTarget,
    ) -> tuple[Pokemon, ...]:
        """
        Return all valid Pokémon targets that may be selected for a move.

        This is used during action generation. It should not perform random
        selection or resolve the final targets affected by a move.

        Args:
            user: The Pokémon using the move.
            targeting: The move's targeting category.

        Returns:
            A tuple of valid target Pokémon.
        """
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

    def resolve_targets(
        self,
        user: Pokemon,
        targeting: MoveTarget,
        selected_target: Pokemon | None = None,
    ) -> tuple[Pokemon, ...]:
        """
        Resolve the actual targets affected by a move during execution.

        Unlike get_legal_targets(), this function operates on an already
        selected action. For moves requiring a chosen target, selected_target
        must be provided.

        Args:
            user: The Pokémon using the move.
            targeting: The move's targeting category.
            selected_target: The target chosen when the action was created.

        Returns:
            A tuple of Pokémon affected by the move.
        """
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
                if selected_target is None:
                    raise ValueError("Single-target moves require a selected target.")

                if selected_target not in living_opponents:
                    raise ValueError("Selected target is not a valid living opponent.")

                return (selected_target,)

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
                if not living_opponents:
                    return ()

                return (self.rng.choice(living_opponents),)

            case MoveTarget.FIELD:
                raise NotImplementedError()

            case _:
                raise ValueError(f"Invalid targeting {targeting}.")

    def is_player_pokemon(
        self,
        pokemon: Pokemon,
    ) -> bool:
        """
        Determine whether a Pokémon belongs to the player's active side.

        This checks object identity rather than equality because Pokémon instances
        represent the runtime state of a battler. A Pokémon is considered a player
        Pokémon if the exact instance appears in the player's active Pokémon.

        Args:
            pokemon: The Pokémon to check.

        Returns:
            True if the Pokémon is currently active on the player's side,
            otherwise False.
        """
        return any(active is pokemon for active in self.state.player_active)

    def get_bench(
        self,
        pokemon: Pokemon,
    ) -> tuple[Pokemon, ...]:
        """
        Return the available bench Pokémon for the side the given active Pokémon
        belongs to.

        The provided Pokémon must currently be active in battle. The returned tuple
        excludes active Pokémon because only bench Pokémon are valid switch targets.

        Args:
            pokemon: The active Pokémon whose bench should be retrieved.

        Returns:
            A tuple containing valid switch-in Pokémon.

        Raises:
            ValueError: If the Pokémon is not currently active in battle.
        """
        if self.is_player_pokemon(pokemon):
            return self.state.player_bench

        if any(active is pokemon for active in self.state.opponent_active):
            return self.state.opponent_bench

        raise ValueError("Pokémon is not currently active.")
