from battle.rng import RNG


def test_rng_is_seeded():
    rng1 = RNG(123)
    rng2 = RNG(123)

    for _ in range(100):
        assert rng1.roll() == rng2.roll()


def test_rng_different_seeds_produce_different_sequences():
    rng1 = RNG(123)
    rng2 = RNG(456)

    assert rng1.roll() != rng2.roll()
