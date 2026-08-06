import pytest

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


def test_rng_choice_returns_item_from_sequence():
    rng = RNG(seed=1)

    values = ("a", "b", "c")

    result = rng.choice(values)

    assert result in values


def test_rng_choice_is_deterministic_with_seed():
    first_rng = RNG(seed=12345)
    second_rng = RNG(seed=12345)

    values = ("a", "b", "c", "d")

    assert first_rng.choice(values) == second_rng.choice(values)


def test_rng_choice_works_with_non_string_types():
    rng = RNG(seed=1)

    values = (1, 2, 3)

    result = rng.choice(values)

    assert result in values


def test_rng_choice_rejects_empty_sequence():
    rng = RNG(seed=1)

    with pytest.raises(ValueError, match="Cannot choose from an empty sequence"):
        rng.choice(())
