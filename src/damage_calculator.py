def calculate_damage(
    *,
    level: int,
    power: int,
    attack: int,
    defense: int,
    stab: float = 1.0,
    effectiveness: float = 1.0,
    critical: bool = False,
    random: float = 1.0,
) -> int:
    base_damage = ((((2 * level) / 5) + 2) * power * attack / defense) / 50 + 2

    critical_multiplier = 1.5 if critical else 1.0

    return int(base_damage * stab * effectiveness * critical_multiplier * random)
