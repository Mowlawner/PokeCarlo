def calculate_damage(attacker, defender, move, state) -> int:
    level = attacker.level
    power = move.power
    if move.category == "special":
        attack = attacker.special_attack
        defense = defender.special_defense
    elif move.category == "status":
        attack = 0
        defense = 1
    else:
        attack = attacker.attack
        defense = defender.defense
    damage = (((((2 * level) / 5) + 2) * power * attack / defense) / 50) + 2
    return damage
