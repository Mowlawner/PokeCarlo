from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import requests

from database.learnset_importer import LearnsetImporter
from database.move_importer import MoveImporter
from database.pokemon_importer import PokemonImporter
from database.species_importer import SpeciesImporter

POKEAPI_BASE = "https://pokeapi.co/api/v2"
TARGET_VERSION_GROUP = "champions"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
GENERATED_DATA_DIR = PROJECT_ROOT / "data" / "generated"

RAW_POKEMON_DIR = RAW_DATA_DIR / "pokemon"
RAW_SPECIES_DIR = RAW_DATA_DIR / "species"
RAW_MOVE_DIR = RAW_DATA_DIR / "moves"

GENERATED_POKEMON_DIR = GENERATED_DATA_DIR / "pokemon"
GENERATED_MOVE_DIR = GENERATED_DATA_DIR / "moves"
GENERATED_LEARNSET_DIR = GENERATED_DATA_DIR / "learnsets" / TARGET_VERSION_GROUP


for directory in (
    RAW_POKEMON_DIR,
    RAW_SPECIES_DIR,
    RAW_MOVE_DIR,
    GENERATED_POKEMON_DIR,
    GENERATED_MOVE_DIR,
    GENERATED_LEARNSET_DIR,
):
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )


def save_json(
    data: dict[str, Any],
    path: Path,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open("w") as file:
        json.dump(
            data,
            file,
            indent=4,
            sort_keys=True,
        )


def load_json(
    path: Path,
) -> dict[str, Any]:
    with path.open() as file:
        return json.load(file)


def fetch(
    endpoint: str,
) -> dict[str, Any]:
    """
    Fetch JSON from PokéAPI.
    """
    url = f"{POKEAPI_BASE}/{endpoint}"

    attempts = 3

    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(
                url,
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            time.sleep(0.1)

            return data

        except requests.RequestException:
            if attempt == attempts:
                raise

            print(
                f"Request failed for {endpoint} "
                f"(attempt {attempt}/{attempts}). Retrying..."
            )

    raise RuntimeError("Unreachable")


def fetch_cached(
    endpoint: str,
    cache_path: Path,
    force: bool = False,
) -> dict[str, Any]:
    """
    Fetch from PokéAPI unless cached data exists.

    Args:
        endpoint: PokéAPI endpoint.
        cache_path: Raw JSON cache location.
        force: Ignore cache and redownload.
    """

    if cache_path.exists() and not force:
        print(f"Using cached {cache_path.name}")
        return load_json(cache_path)

    if force and cache_path.exists():
        print(f"Refreshing {cache_path.name}")
    else:
        print(f"Downloading {endpoint}")

    data = fetch(endpoint)

    save_json(
        data,
        cache_path,
    )

    return data


def get_pokemon(
    name: str,
    force: bool = False,
) -> dict[str, Any]:
    return fetch_cached(
        f"pokemon/{name}",
        RAW_POKEMON_DIR / f"{name}.json",
        force=force,
    )


def get_species(
    name: str,
    force: bool = False,
) -> dict[str, Any]:
    return fetch_cached(
        f"pokemon-species/{name}",
        RAW_SPECIES_DIR / f"{name}.json",
        force=force,
    )


def get_move(
    name: str,
    force: bool = False,
) -> dict[str, Any]:
    return fetch_cached(
        f"move/{name}",
        RAW_MOVE_DIR / f"{name}.json",
        force=force,
    )


def build_pokemon(
    name: str,
    force: bool = False,
) -> None:
    print(f"\nBuilding Pokémon: {name}")

    pokemon_raw = get_pokemon(
        name,
        force=force,
    )

    pokemon_raw = get_pokemon(name)

    species_name = pokemon_raw["species"]["name"]

    species_raw = get_species(species_name)

    pokemon_entry = PokemonImporter().to_database_model(
        pokemon_raw,
    )

    species_entry = SpeciesImporter().to_database_model(
        species_raw,
    )

    save_json(
        {
            **species_entry,
            **pokemon_entry,
        },
        GENERATED_POKEMON_DIR / f"{name}.json",
    )

    learnset_entry = LearnsetImporter().to_database_model(
        pokemon_raw,
        target_version_group=TARGET_VERSION_GROUP,
    )

    save_json(
        learnset_entry,
        GENERATED_LEARNSET_DIR / f"{name}.json",
    )


def build_move(
    name: str,
    force: bool = False,
) -> None:
    print(f"\nBuilding move: {name}")

    move_raw = get_move(
        name,
        force=force,
    )
    move_entry = MoveImporter().to_database_model(
        move_raw,
    )

    save_json(
        move_entry,
        GENERATED_MOVE_DIR / f"{name}.json",
    )


def get_index(
    endpoint: str,
    cache_name: str,
) -> list[str]:
    index_path = RAW_DATA_DIR / cache_name

    data = fetch_cached(
        endpoint,
        index_path,
    )

    return [entry["name"] for entry in data["results"]]


def build_all_pokemon() -> None:
    pokemon_names = get_index(
        "pokemon?limit=100000",
        "pokemon_index.json",
    )

    total = len(pokemon_names)

    for index, name in enumerate(pokemon_names, start=1):
        print(f"\n[{index}/{total}] Building Pokémon: {name}")
        build_pokemon(name)


def build_all_moves() -> None:
    move_names = get_index(
        "move?limit=100000",
        "move_index.json",
    )

    for name in move_names:
        build_move(name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the PokeCarlo JSON database.",
    )

    parser.add_argument(
        "--pokemon",
        nargs="+",
        help="Build specific Pokémon.",
    )

    parser.add_argument(
        "--move",
        nargs="+",
        help="Build specific moves.",
    )

    parser.add_argument(
        "--all-pokemon",
        action="store_true",
        help="Build every Pokémon.",
    )

    parser.add_argument(
        "--all-moves",
        action="store_true",
        help="Build every move.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore cached raw data and redownload from PokéAPI.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.pokemon:
        for name in args.pokemon:
            build_pokemon(
                name,
                force=args.force,
            )

    if args.move:
        for name in args.move:
            build_move(
                name,
                force=args.force,
            )

    if args.all_pokemon:
        build_all_pokemon()

    if args.all_moves:
        build_all_moves()

    if not any(
        (
            args.pokemon,
            args.move,
            args.all_pokemon,
            args.all_moves,
        )
    ):
        print("Nothing selected. Use --help for options.")


if __name__ == "__main__":
    main()
