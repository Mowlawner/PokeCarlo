from move import Move
from pokemon import Pokemon


def calculate_damage(
    attacker: Pokemon,
    defender: Pokemon,
    move: Move,
) -> int:
    level = attacker.pokemon_set.level
    power = move.power
    if move.category == "special":
        attack = attacker.stats.sp_attack
        defense = defender.stats.sp_defense
    elif move.category == "status":
        attack = 0
        defense = 1
    else:
        attack = attacker.stats.attack
        defense = defender.stats.defense
    damage = int(((((2 * level) / 5) + 2) * power * attack / defense) / 50) + 2
    return damage
