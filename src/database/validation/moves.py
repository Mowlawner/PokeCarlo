from pathlib import Path

from status_condition import StatusCondition

from .common import load_json

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
    "NIGHT_SHADE",  # damage = user's level
    "SEISMIC_TOSS",  # damage = user's level
    "SONIC_BOOM",  # fixed 20 damage
    "DRAGON_RAGE",  # fixed 40 damage
    "PSYWAVE",  # random level-based damage
    "SHADOW_HALF",  # halves both users HP
}

VARIABLE_POWER_MOVES = {
    "ELECTRO_BALL",  # speed ratio
    "HEAVY_SLAM",  # weight ratio
    "LOW_KICK",  # target weight
    "GRASS_KNOT",  # target weight
    "GYRO_BALL",  # speed ratio
    "HEAT_CRASH",  # weight ratio
    "FLAIL",  # user's remaining HP
    "REVERSAL",  # user's remaining HP
    "TRUMP_CARD",  # PP remaining
    "WRING_OUT",  # target remaining HP
    "CRUSH_GRIP",  # target remaining HP
    "NATURAL_GIFT",  # held berry
    "FLING",  # held item
    "PRESENT",  # random damage/heal behavior
}

DAMAGE_RETURN_MOVES = {
    "COUNTER",  # 2x physical damage received
    "MIRROR_COAT",  # 2x special damage received
    "METAL_BURST",  # 1.5x damage received
    "BIDE",  # stored damage returned
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
    "BEAT_UP",  # uses party members
    "FINAL_GAMBIT",  # user's HP
    "GUARDIAN_OF_ALOLA",  # HP-based Z move
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


def validate_moves(
    moves_dir: Path,
    referenced_moves: set[str],
) -> list[str]:
    """
    Validate generated move entries and ensure all referenced moves exist.
    """
    errors: list[str] = []
    move_files = list(moves_dir.glob("*.json"))

    print(f"Checking move database ({len(move_files)} entries)...")

    generated_moves: set[str] = set()

    for path in move_files:
        data = load_json(path)

        missing = REQUIRED_MOVE_FIELDS - data.keys()

        if missing:
            errors.append(f"{path.name}: missing fields {sorted(missing)}")
            continue

        move_name = data["move_name"]

        if move_name in generated_moves:
            errors.append(f"{path.name}: duplicate move_name {move_name}")

        generated_moves.add(move_name)

        if not isinstance(data["id"], int):
            errors.append(f"{path.name}: id is not an integer")

        if not isinstance(data["priority"], int):
            errors.append(f"{path.name}: priority is not an integer")

        if not isinstance(data["effects"], list):
            errors.append(f"{path.name}: effects is not a list")
        else:
            for index, effect in enumerate(data["effects"]):
                if not isinstance(effect, dict):
                    errors.append(f"{path.name}: effect {index} is not an object")
                    continue

                if effect.get("type") == "status":
                    status = effect.get("status")
                    if not isinstance(status, str):
                        errors.append(
                            f"{path.name}: status effect {index} is missing status"
                        )
                    elif status not in StatusCondition.__members__:
                        errors.append(
                            f"{path.name}: invalid status effect status {status}"
                        )
                    chance = effect.get("chance")
                    if chance is not None and (
                        not isinstance(chance, (int, float)) or not 0 <= chance <= 100
                    ):
                        errors.append(
                            f"{path.name}: status effect {index} has invalid chance"
                        )

        if not data["move_type"]:
            errors.append(f"{path.name}: missing move_type")

        if not data["category"]:
            errors.append(f"{path.name}: missing category")

        if data["category"] == "STATUS" and data["power"] not in (None, 0):
            errors.append(f"{path.name}: STATUS move has nonzero power")

        if (
            data["category"] != "STATUS"
            and data["power"] is None
            and move_name not in NONSTANDARD_DAMAGE_MOVES
        ):
            errors.append(f"{path.name}: damaging move has no power")

    missing_moves = referenced_moves - generated_moves

    for move in sorted(missing_moves):
        errors.append(f"Missing generated move: {move}")

    return errors
