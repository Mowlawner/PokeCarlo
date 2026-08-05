from dataclasses import dataclass

from pokemon import Pokemon
from terrain import Terrain
from weather import Weather


@dataclass(slots=True)
class BattleState:
    player_active: tuple[Pokemon, ...]
    opponent_active: tuple[Pokemon, ...]

    turn_number: int = 1

    weather: Weather | None = None
    terrain: Terrain | None = None

    def replace_active(
        self,
        *,
        outgoing: Pokemon,
        incoming: Pokemon,
    ) -> None:
        if incoming is outgoing:
            raise ValueError("Cannot replace a Pokémon with itself.")

        if any(pokemon is incoming for pokemon in self.player_active):
            raise ValueError("Incoming Pokémon is already active.")

        if any(pokemon is incoming for pokemon in self.opponent_active):
            raise ValueError("Incoming Pokémon is already active.")

        player_index = next(
            (i for i, pokemon in enumerate(self.player_active) if pokemon is outgoing),
            None,
        )

        if player_index is not None:
            player_active = list(self.player_active)
            player_active[player_index] = incoming
            self.player_active = tuple(player_active)
            return

        opponent_index = next(
            (
                i
                for i, pokemon in enumerate(self.opponent_active)
                if pokemon is outgoing
            ),
            None,
        )

        if opponent_index is not None:
            opponent_active = list(self.opponent_active)
            opponent_active[opponent_index] = incoming
            self.opponent_active = tuple(opponent_active)
            return

        raise ValueError("Outgoing Pokémon is not currently active.")
