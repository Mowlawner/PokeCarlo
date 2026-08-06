from damage_calculator import calculate_damage


def test_calculate_damage_simple_case():
    damage = calculate_damage(
        level=50,
        power=100,
        attack=120,
        defense=100,
    )

    assert damage == 54  # whatever the actual value is
