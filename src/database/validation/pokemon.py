from pathlib import Path

from .common import load_json

REQUIRED_POKEMON_FIELDS = {
    "pokemon_id",
    "national_dex",
    "species_name",
    "display_name",
    "types",
    "base_stats",
    "abilities",
    "height",
    "weight",
}


def validate_pokemon_database(pokemon_dir: Path) -> list[str]:
    """
    Validate generated Pokémon entries.
    """
    errors: list[str] = []
    pokemon_files = list(pokemon_dir.glob("*.json"))

    print(f"Checking Pokémon database ({len(pokemon_files)} entries)...")

    seen_ids: set[int] = set()

    for path in pokemon_files:
        data = load_json(path)

        missing = REQUIRED_POKEMON_FIELDS - data.keys()

        if missing:
            errors.append(
                f"{path.name}: missing fields {sorted(missing)} "
                f"(keys={sorted(data.keys())})"
            )
            continue

        pokemon_id = data["pokemon_id"]
        national_dex = data["national_dex"]

        # Ensure internal form IDs are unique
        if pokemon_id in seen_ids:
            errors.append(f"{path.name}: duplicate pokemon_id {pokemon_id}")

        seen_ids.add(pokemon_id)

        # Validate IDs
        if not isinstance(pokemon_id, int):
            errors.append(f"{path.name}: pokemon_id is not an integer")

        if not isinstance(national_dex, int):
            errors.append(f"{path.name}: national_dex is not an integer")

        # Normal Pokémon should have matching IDs.
        # Alternate forms (Mega, regional, etc.) should not.
        if pokemon_id != national_dex:
            print(
                f"Form detected: {path.name} "
                f"(pokemon_id={pokemon_id}, "
                f"national_dex={national_dex})"
            )

        if not data.get("species_name"):
            errors.append(f"{path.name}: missing species_name")

        if not data.get("types"):
            errors.append(f"{path.name}: has no types")

        if not data.get("base_stats"):
            errors.append(f"{path.name}: has no base stats")

    return errors


def validate_forms(pokemon_dir: Path) -> list[str]:
    """
    Validate alternate forms.

    Forms should:
    - have a pokemon_id different from national_dex
    - still point at a valid species
    """
    errors: list[str] = []

    for path in pokemon_dir.glob("*.json"):
        data = load_json(path)

        pokemon_id = data.get("pokemon_id")
        national_dex = data.get("national_dex")

        if pokemon_id is None or national_dex is None:
            continue

        # Alternate form
        if pokemon_id != national_dex:
            species_name = data.get("species_name")

            if not species_name:
                errors.append(f"{path.name}: alternate form missing species_name")

    return errors
