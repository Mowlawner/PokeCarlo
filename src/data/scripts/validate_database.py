from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

GENERATED_DATA_DIR = PROJECT_ROOT / "data" / "generated"

POKEMON_DIR = GENERATED_DATA_DIR / "pokemon"
LEARNSET_DIR = GENERATED_DATA_DIR / "learnsets" / "champions"
MOVES_DIR = GENERATED_DATA_DIR / "moves"


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


REQUIRED_LEARNSET_FIELDS = {
    "pokemon",
    "version_group",
    "moves",
}

REQUIRED_MOVE_FIELDS = {
    "id",
    "move_name",
    "display_name",
    "move_type",
    "category",
    "power",
    "accuracy",
    "pp",
    "priority",
    "target",
    "effects",
}

FIXED_DAMAGE_MOVES = {
    "NIGHT_SHADE",      # damage = user's level
    "SEISMIC_TOSS",     # damage = user's level
    "SONIC_BOOM",       # fixed 20 damage
    "DRAGON_RAGE",      # fixed 40 damage
    "PSYWAVE",          # random level-based damage
    "SHADOW_HALF",      # halves both users HP
}

VARIABLE_POWER_MOVES = {
    "ELECTRO_BALL",     # speed ratio
    "HEAVY_SLAM",       # weight ratio
    "LOW_KICK",         # target weight
    "GRASS_KNOT",       # target weight
    "GYRO_BALL",        # speed ratio
    "HEAT_CRASH",       # weight ratio
    "FLAIL",            # user's remaining HP
    "REVERSAL",         # user's remaining HP
    "TRUMP_CARD",       # PP remaining
    "WRING_OUT",        # target remaining HP
    "CRUSH_GRIP",       # target remaining HP
    "NATURAL_GIFT",     # held berry
    "FLING",            # held item
    "PRESENT",          # random damage/heal behavior
}

DAMAGE_RETURN_MOVES = {
    "COUNTER",          # 2x physical damage received
    "MIRROR_COAT",      # 2x special damage received
    "METAL_BURST",      # 1.5x damage received
    "BIDE",             # stored damage returned
}

OHKO_MOVES = {
    "HORN_DRILL",
    "GUILLOTINE",
    "FISSURE",
    "SHEER_COLD",
}

LEVEL_BASED_DAMAGE_MOVES = {
    "SEISMIC_TOSS",
    "NIGHT_SHADE",
}

HP_BASED_DAMAGE_MOVES = {
    "FLAIL",
    "REVERSAL",
    "WRING_OUT",
    "CRUSH_GRIP",
    "SUPER_FANG",
    "NATURES_MADNESS",
    "ENDEAVOR",
}

SPECIAL_DAMAGE_MOVES = {
    "BEAT_UP",          # uses party members
    "FINAL_GAMBIT",     # user's HP
    "GUARDIAN_OF_ALOLA",# HP-based Z move
}

Z_MOVE_DAMAGE_MOVES = {
    "ALL_OUT_PUMMELING__PHYSICAL",
    "ALL_OUT_PUMMELING__SPECIAL",
    "ACID_DOWNPOUR__PHYSICAL",
    "ACID_DOWNPOUR__SPECIAL",
    "BLOOM_DOOM__PHYSICAL",
    "BLOOM_DOOM__SPECIAL",
    "BLACK_HOLE_ECLIPSE__PHYSICAL",
    "BLACK_HOLE_ECLIPSE__SPECIAL",
    "BREAKNECK_BLITZ__PHYSICAL",
    "BREAKNECK_BLITZ__SPECIAL",
    "CORKSCREW_CRASH__PHYSICAL",
    "CORKSCREW_CRASH__SPECIAL",
    "CONTINENTAL_CRUSH__PHYSICAL",
    "CONTINENTAL_CRUSH__SPECIAL",
    "DEVASTATING_DRAKE__PHYSICAL",
    "DEVASTATING_DRAKE__SPECIAL",
    "GIGAVOLT_HAVOC__PHYSICAL",
    "GIGAVOLT_HAVOC__SPECIAL",
    "HYDRO_VORTEX__PHYSICAL",
    "HYDRO_VORTEX__SPECIAL",
    "INFERNO_OVERDRIVE__PHYSICAL",
    "INFERNO_OVERDRIVE__SPECIAL",
    "NEVER_ENDING_NIGHTMARE__PHYSICAL",
    "NEVER_ENDING_NIGHTMARE__SPECIAL",
    "SAVAGE_SPIN_OUT__PHYSICAL",
    "SAVAGE_SPIN_OUT__SPECIAL",
    "SHATTERED_PSYCHE__PHYSICAL",
    "SHATTERED_PSYCHE__SPECIAL",
    "SUBZERO_SLAMMER__PHYSICAL",
    "SUBZERO_SLAMMER__SPECIAL",
    "SUPERSONIC_SKYSTRIKE__PHYSICAL",
    "SUPERSONIC_SKYSTRIKE__SPECIAL",
    "TECTONIC_RAGE__PHYSICAL",
    "TECTONIC_RAGE__SPECIAL",
    "TWINKLE_TACKLE__PHYSICAL",
    "TWINKLE_TACKLE__SPECIAL",
}

MAX_MOVE_DAMAGE_MOVES = {
    # likely empty unless you are importing Dynamax moves separately
}

REVIEW_MOVES = {
    "PUNISHMENT",
    "MAGNITUDE",
    "SPIT_UP",
    "PIKA_PAPOW",
    "VEEVEE_VOLLEY",
    "FRUSTRATION",
    "RETURN",
}

NONSTANDARD_DAMAGE_MOVES = (
    FIXED_DAMAGE_MOVES
    | VARIABLE_POWER_MOVES
    | DAMAGE_RETURN_MOVES
    | OHKO_MOVES
    | HP_BASED_DAMAGE_MOVES
    | SPECIAL_DAMAGE_MOVES
    | Z_MOVE_DAMAGE_MOVES
    | REVIEW_MOVES
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as file:
        return json.load(file)


def validate_pokemon_database() -> list[str]:
    """
    Validate generated Pokémon entries.
    """

    errors: list[str] = []

    pokemon_files = list(POKEMON_DIR.glob("*.json"))

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
            errors.append(
                f"{path.name}: duplicate pokemon_id {pokemon_id}"
            )

        seen_ids.add(pokemon_id)

        # Validate IDs
        if not isinstance(pokemon_id, int):
            errors.append(
                f"{path.name}: pokemon_id is not an integer"
            )

        if not isinstance(national_dex, int):
            errors.append(
                f"{path.name}: national_dex is not an integer"
            )

        # Normal Pokémon should have matching IDs.
        # Alternate forms (Mega, regional, etc.) should not.
        if pokemon_id == national_dex:
            pass
        else:
            print(
                f"Form detected: {path.name} "
                f"(pokemon_id={pokemon_id}, "
                f"national_dex={national_dex})"
            )

        if not data.get("species_name"):
            errors.append(
                f"{path.name}: missing species_name"
            )

        if not data.get("types"):
            errors.append(
                f"{path.name}: has no types"
            )

        if not data.get("base_stats"):
            errors.append(
                f"{path.name}: has no base stats"
            )

    return errors

def validate_forms() -> list[str]:
    """
    Validate alternate forms.

    Forms should:
    - have a pokemon_id different from national_dex
    - still point at a valid species
    """

    errors: list[str] = []

    for path in POKEMON_DIR.glob("*.json"):
        data = load_json(path)

        pokemon_id = data.get("pokemon_id")
        national_dex = data.get("national_dex")

        if pokemon_id is None or national_dex is None:
            continue

        # Alternate form
        if pokemon_id != national_dex:
            species_name = data.get("species_name")

            if not species_name:
                errors.append(
                    f"{path.name}: alternate form missing species_name"
                )

    return errors

def validate_learnsets() -> tuple[list[str], set[str]]:
    """
    Validate Champions learnsets and collect referenced moves.
    """

    errors: list[str] = []
    moves: set[str] = set()

    learnset_files = list(LEARNSET_DIR.glob("*.json"))

    print(f"Checking Champions learnsets ({len(learnset_files)} entries)...")

    for path in learnset_files:
        data = load_json(path)

        missing = REQUIRED_LEARNSET_FIELDS - data.keys()

        if missing:
            errors.append(f"{path.name}: missing fields {sorted(missing)}")
            continue

        if data["version_group"] != "CHAMPIONS":
            errors.append(
                f"{path.name}: incorrect version group {data['version_group']}"
            )

        for move in data["moves"]:
            if not move:
                errors.append(f"{path.name}: empty move entry")
                continue

            moves.add(move)

    return errors, moves

def validate_moves(
    referenced_moves: set[str],
) -> list[str]:
    """
    Validate generated move entries and ensure all referenced moves exist.
    """

    errors: list[str] = []

    move_files = list(MOVES_DIR.glob("*.json"))

    print(f"Checking move database ({len(move_files)} entries)...")

    generated_moves: set[str] = set()

    for path in move_files:
        data = load_json(path)

        missing = REQUIRED_MOVE_FIELDS - data.keys()

        if missing:
            errors.append(
                f"{path.name}: missing fields {sorted(missing)}"
            )
            continue

        move_name = data["move_name"]

        if move_name in generated_moves:
            errors.append(
                f"{path.name}: duplicate move_name {move_name}"
            )

        generated_moves.add(move_name)

        if not isinstance(data["id"], int):
            errors.append(
                f"{path.name}: id is not an integer"
            )

        if not isinstance(data["priority"], int):
            errors.append(
                f"{path.name}: priority is not an integer"
            )

        if not isinstance(data["effects"], list):
            errors.append(
                f"{path.name}: effects is not a list"
            )

        if not data["move_type"]:
            errors.append(
                f"{path.name}: missing move_type"
            )

        if not data["category"]:
            errors.append(
                f"{path.name}: missing category"
            )

        if data["category"] == "STATUS" and data["power"] not in (None, 0):
            errors.append(
                f"{path.name}: STATUS move has nonzero power"
            )

        if data["category"] != "STATUS" and data["power"] is None and move_name not in NONSTANDARD_DAMAGE_MOVES:
            errors.append(
                f"{path.name}: damaging move has no power"
            )


    missing_moves = referenced_moves - generated_moves

    for move in sorted(missing_moves):
        errors.append(
            f"Missing generated move: {move}"
        )

    return errors


def print_move_summary(
    moves: set[str],
) -> None:
    print()
    print("Champions move references:")
    print(f"Unique moves required: {len(moves)}")

    print()
    print("Sample moves:")

    for move in sorted(moves)[:25]:
        print(f" - {move}")


def print_form_summary() -> None:
    forms = []

    for path in POKEMON_DIR.glob("*.json"):
        data = load_json(path)

        if data["pokemon_id"] != data["national_dex"]:
            forms.append(
                (
                    path.stem,
                    data["species_name"],
                    data["pokemon_id"],
                    data["national_dex"],
                )
            )

    print()
    print(f"Alternate forms found: {len(forms)}")

    for form in forms[:25]:
        print(
            f" - {form[0]} "
            f"({form[1]} #{form[3]})"
        )


def main() -> None:
    errors: list[str] = []

    errors.extend(validate_pokemon_database())

    errors.extend(validate_forms())

    learnset_errors, moves = validate_learnsets()
    move_errors = validate_moves(moves)


    errors.extend(learnset_errors)
    errors.extend(move_errors)

    print_move_summary(moves)
    print_form_summary()

    print()

    if errors:
        print(f"Validation failed with {len(errors)} errors:")

        for error in errors:
            print(f" - {error}")

        raise SystemExit(1)

    print("Database validation passed!")


if __name__ == "__main__":
    main()
