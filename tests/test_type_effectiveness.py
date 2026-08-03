from pokemon_types import Type, effectiveness


def test_super_effective():
    assert effectiveness(Type.GROUND, (Type.ELECTRIC,)) == 2.0


def test_immune():
    assert effectiveness(Type.GROUND, (Type.FLYING,)) == 0.0
    assert effectiveness(Type.FIGHTING, (Type.GHOST,)) == 0.0


def test_extremely_effective():
    assert effectiveness(Type.ICE, (Type.DRAGON, Type.FLYING)) == 4.0


def test_neutral_effectiveness():
    assert effectiveness(Type.NORMAL, (Type.FIRE,)) == 1.0


def test_mostly_ineffective():
    assert effectiveness(Type.FIRE, (Type.WATER, Type.DRAGON)) == 0.25


def test_not_very_effective():
    assert effectiveness(Type.WATER, (Type.DRAGON,)) == 0.5


def test_immunity_overrides_super_effective():
    assert (
        effectiveness(
            Type.NORMAL,
            (Type.GHOST, Type.ROCK),
        )
        == 0.0
    )
