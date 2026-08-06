from dataclasses import dataclass

from pokemon import Pokemon
from terrain import Terrain
from weather import Weather


@dataclass(slots=True)
class BattleState:
    player_active: tuple[Pokemon, ...]
    opponent_active: tuple[Pokemon, ...]

    player_party: tuple[Pokemon, ...] | None = None
    opponent_party: tuple[Pokemon, ...] | None = None

    turn_number: int = 1

    weather: Weather | None = None
    terrain: Terrain | None = None

    def __post_init__(self) -> None:
        if self.player_party is None:
            self.player_party = self.player_active

        if self.opponent_party is None:
            self.opponent_party = self.opponent_active

        self._validate_party(
            active=self.player_active,
            party=self.player_party,
            side="player",
        )

        self._validate_party(
            active=self.opponent_active,
            party=self.opponent_party,
            side="opponent",
        )

    @staticmethod
    def _validate_party(
        *,
        active: tuple[Pokemon, ...],
        party: tuple[Pokemon, ...],
        side: str,
    ) -> None:
        seen = set()
        for pokemon in party:
            if id(pokemon) in seen:
                raise ValueError(...)
            seen.add(id(pokemon))
        if len(seen) != len(party):
            raise ValueError(f"{side.capitalize()} party contains duplicate Pokémon.")

        for active_pokemon in active:
            if not any(active_pokemon is pokemon for pokemon in party):
                raise ValueError(f"Active {side} Pokémon must be present in the party.")

    @property
    def player_bench(self) -> tuple[Pokemon, ...]:
        return tuple(
            pokemon
            for pokemon in self.player_party
            if all(pokemon is not active for active in self.player_active)
        )

    @property
    def opponent_bench(self) -> tuple[Pokemon, ...]:
        return tuple(
            pokemon
            for pokemon in self.opponent_party
            if all(pokemon is not active for active in self.opponent_active)
        )

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
            if not any(pokemon is incoming for pokemon in self.player_party):
                raise ValueError("Incoming Pokémon is not in the player's party.")

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
            if not any(pokemon is incoming for pokemon in self.opponent_party):
                raise ValueError("Incoming Pokémon is not in the opponent's party.")

            opponent_active = list(self.opponent_active)
            opponent_active[opponent_index] = incoming
            self.opponent_active = tuple(opponent_active)
            return

        raise ValueError("Outgoing Pokémon is not currently active.")
