def test_take_damage_returns_actual_hp_lost(garchomp):
    garchomp.current_hp = 100

    assert garchomp.take_damage(30) == 30
    assert garchomp.current_hp == 70


def test_take_damage_returns_only_remaining_hp_when_damage_is_too_high(garchomp):
    garchomp.current_hp = 25

    assert garchomp.take_damage(100) == 25
    assert garchomp.current_hp == 0


def test_take_damage_returns_zero_for_zero_damage(garchomp):
    garchomp.current_hp = 100

    assert garchomp.take_damage(0) == 0
    assert garchomp.current_hp == 100
