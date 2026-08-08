from database.species_database import SpeciesDatabase


def load_species_db(
    directory_path: str = "src/data/generated/pokemon",
) -> SpeciesDatabase:
    return SpeciesDatabase.load(directory_path)
