from __future__ import annotations

import sys
from pathlib import Path

# Add src to path so we can import from database.validation
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from database.validation.common import load_json
from database.validation.learnsets import validate_learnsets
from database.validation.moves import validate_moves
from database.validation.pokemon import validate_forms, validate_pokemon_database

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

GENERATED_DATA_DIR = PROJECT_ROOT / "data" / "generated"

POKEMON_DIR = GENERATED_DATA_DIR / "pokemon"
LEARNSET_DIR = GENERATED_DATA_DIR / "learnsets" / "champions"
MOVES_DIR = GENERATED_DATA_DIR / "moves"


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
        print(f" - {form[0]} ({form[1]} #{form[3]})")


def main() -> None:
    errors: list[str] = []

    errors.extend(validate_pokemon_database(POKEMON_DIR))

    errors.extend(validate_forms(POKEMON_DIR))

    learnset_errors, moves = validate_learnsets(LEARNSET_DIR)
    move_errors = validate_moves(MOVES_DIR, moves)

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
