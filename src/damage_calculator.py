def calculate_damage(
    level: int,
    power: int,
    attack: int,
    defense: int,
) -> int:
    return int(((((2 * level) / 5) + 2) * power * attack / defense) / 50) + 2
