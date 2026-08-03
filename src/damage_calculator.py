def calculate_damage(
    *,
    level: int,
    power: int,
    attack: int,
    defense: int,
    stab: float = 1.0,
    effectiveness: float = 1.0,
    critical: float = 1.0,
    random: float = 1.0,
) -> int:
    base_damage = ((((2 * level) / 5) + 2) * power * attack / defense) / 50 + 2

    return int(base_damage * stab * effectiveness * critical * random)
