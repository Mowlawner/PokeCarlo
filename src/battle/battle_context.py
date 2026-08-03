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
        opponents = opponent_active if user in player_active else player_active

        allies = player_active if user in player_active else opponent_active

        match targeting:
            case MoveTarget.SINGLE_TARGET:
                if selected_target is None:
                    raise ValueError("Single target move requires a target.")

                if not selected_target.is_fainted:
                    return (selected_target,)

                living_opponents = tuple(p for p in opponents if not p.is_fainted)

                if living_opponents:
                    return (living_opponents[0],)

                return ()

            case MoveTarget.SELF:
                return (user,)

            case MoveTarget.ALL_OTHERS:
                return tuple(
                    pokemon for pokemon in (*allies, *opponents) if pokemon is not user
                )

            case MoveTarget.ALL:
                return (*allies, *opponents)

            case MoveTarget.ALL_OPPONENTS:
                return opponents

            case MoveTarget.ALL_ALLIES:
                return tuple(pokemon for pokemon in allies if pokemon is not user)

            case MoveTarget.RANDOM_OPPONENT:
                # placeholder until RNG integration
                raise NotImplementedError()

            case MoveTarget.FIELD:
                # This is probably not a tuple[Pokemon] conceptually.
                # Future refactor: effects target the battle context itself.
                raise NotImplementedError()

            case _:
                raise ValueError(f"Invalid targeting {targeting}.")
