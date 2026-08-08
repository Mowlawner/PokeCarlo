from pathlib import Path

from .common import load_json

REQUIRED_LEARNSET_FIELDS = {
    "pokemon",
    "version_group",
    "moves",
}


def validate_learnsets(learnset_dir: Path) -> tuple[list[str], set[str]]:
    """
    Validate Champions learnsets and collect referenced moves.
    """
    errors: list[str] = []
    moves: set[str] = set()

    learnset_files = list(learnset_dir.glob("*.json"))

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
