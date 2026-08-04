from status_condition import StatusCondition


def test_pokemon_starts_without_status(garchomp):
    assert garchomp.status is StatusCondition.NONE


def test_pokemon_can_be_burned(garchomp):
    garchomp.status = StatusCondition.BURN

    assert garchomp.status is StatusCondition.BURN
