import json

from species_database import SpeciesDatabase
from pokemon_species import PokemonSpecies


def load_species_db(path_to_json: str = "../data/species.json") -> SpeciesDatabase:
    with open(path_to_json, "r") as f:
        species = json.load(f)
    species_data = {
        k: PokemonSpecies.from_json(name=k, json_data=v) for k, v in species.items()
    }
    return SpeciesDatabase(species_data)
