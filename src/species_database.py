from pokemon_species import PokemonSpecies


class SpeciesDatabase:
    def __init__(self, species: dict[str, PokemonSpecies]):
        self._species = species

    def get(self, name: str) -> PokemonSpecies:
        return self._species[name]
