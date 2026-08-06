from __future__ import annotations

import requests

from database.learnset_importer import LearnsetImporter
from database.move_importer import MoveImporter
from database.pokemon_importer import PokemonImporter
from database.species_importer import SpeciesImporter

POKEAPI_BASE = "https://pokeapi.co/api/v2"


def fetch(endpoint: str) -> dict:
    response = requests.get(
        f"{POKEAPI_BASE}/{endpoint}",
        timeout=30,
    )
    response.raise_for_status()

    return response.json()


def validate_garchomp() -> None:
    print("Validating Garchomp import...")

    pokemon_data = fetch("pokemon/garchomp")
    species_data = fetch("pokemon-species/garchomp")

    pokemon = PokemonImporter().to_database_model(
        pokemon_data,
    )

    species = SpeciesImporter().to_database_model(
        species_data,
    )

    assert pokemon["national_dex"] == 445
    assert pokemon["species_name"] == "GARCHOMP"
    assert pokemon["types"] == [
        "DRAGON",
        "GROUND",
    ]
    assert pokemon["base_stats"]["attack"] == 130
    assert pokemon["base_stats"]["speed"] == 102
    assert pokemon["abilities"] == [
        "SAND_VEIL",
        "ROUGH_SKIN",
    ]

    assert species["gender_ratio"] == {
        "male": 0.5,
        "female": 0.5,
    }
    assert species["capture_rate"] == 45
    assert species["growth_rate"] == "SLOW"

    print("✓ Garchomp import validated")


def validate_moves() -> None:
    print("Validating move imports...")

    for move_name, expected in (
        (
            "earthquake",
            {
                "move_name": "EARTHQUAKE",
                "move_type": "GROUND",
                "category": "PHYSICAL",
                "power": 100,
                "accuracy": 100,
            },
        ),
        (
            "protect",
            {
                "move_name": "PROTECT",
                "move_type": "NORMAL",
                "category": "STATUS",
                "power": None,
                "priority": 4,
            },
        ),
    ):
        move_data = fetch(f"move/{move_name}")

        move = MoveImporter().to_database_model(
            move_data,
        )

        for key, value in expected.items():
            assert move[key] == value, (
                f"{move_name}: expected {key}={value}, got {move[key]}"
            )

        print(f"✓ {move_name.title()} import validated")


def validate_champions_learnset() -> None:
    print("Validating Pokémon Champions learnsets...")

    pokemon_data = fetch("pokemon/garchomp")

    learnset = LearnsetImporter().to_database_model(
        pokemon_data,
        target_version_group="champions",
    )

    assert learnset["pokemon"] == "GARCHOMP"

    moves = learnset["moves"]

    assert isinstance(moves, list)
    assert len(moves) > 0

    # Known Garchomp Champions moves we expect to exist.
    expected_moves = {
        "EARTHQUAKE",
        "DRAGON_CLAW",
        "PROTECT",
    }

    missing_moves = expected_moves - set(moves)

    assert not missing_moves, f"Missing expected Champions moves: {missing_moves}"

    print(f"✓ Champions learnset validated ({len(moves)} moves found)")


def main() -> None:
    validate_garchomp()
    validate_moves()
    validate_champions_learnset()

    print("\nAll importer validations passed.")


if __name__ == "__main__":
    main()
