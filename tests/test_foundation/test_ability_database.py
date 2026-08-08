import json

import pytest

from database.ability_database import AbilityDatabase


def write_ability(directory, filename="adaptability.json", **overrides):
    data = {
        "ability_id": 91,
        "ability_name": "ADAPTABILITY",
        "display_name": "Adaptability",
        "generation": "GENERATION_IV",
    }
    data.update(overrides)
    (directory / filename).write_text(json.dumps(data), encoding="utf-8")


def test_load_ability_database_parses_all_fields(tmp_path):
    ability_dir = tmp_path / "abilities"
    ability_dir.mkdir()
    write_ability(ability_dir)

    ability = AbilityDatabase.load(ability_dir).get("ADAPTABILITY")

    assert ability.id == 91
    assert ability.name == "ADAPTABILITY"
    assert ability.display_name == "Adaptability"
    assert ability.generation == "GENERATION_IV"


def test_get_ability_normalization(tmp_path):
    ability_dir = tmp_path / "abilities"
    ability_dir.mkdir()
    write_ability(
        ability_dir,
        filename="speed-boost.json",
        ability_id=3,
        ability_name="SPEED_BOOST",
        display_name="Speed Boost",
    )
    database = AbilityDatabase.load(ability_dir)

    assert database.get("SPEED_BOOST").id == 3
    assert database.get("speed_boost").id == 3
    assert database.get("Speed-Boost").id == 3


def test_load_ability_database_missing_directory():
    with pytest.raises(ValueError, match="is not a directory"):
        AbilityDatabase.load("non_existent_ability_directory_12345")


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"ability_id": 0}, "Ability ID must be a positive integer"),
        ({"ability_name": ""}, "Ability name must be a non-empty string"),
    ],
)
def test_load_ability_database_rejects_invalid_data(tmp_path, overrides, message):
    ability_dir = tmp_path / "abilities"
    ability_dir.mkdir()
    write_ability(ability_dir, **overrides)

    with pytest.raises(ValueError, match=message):
        AbilityDatabase.load(ability_dir)


def test_load_ability_database_rejects_missing_data(tmp_path):
    ability_dir = tmp_path / "abilities"
    ability_dir.mkdir()
    data = {
        "ability_id": 91,
        "ability_name": "ADAPTABILITY",
        "display_name": "Adaptability",
    }
    (ability_dir / "adaptability.json").write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid ability data.*generation"):
        AbilityDatabase.load(ability_dir)


def test_load_ability_database_rejects_malformed_json(tmp_path):
    ability_dir = tmp_path / "abilities"
    ability_dir.mkdir()
    (ability_dir / "broken.json").write_text("{", encoding="utf-8")

    with pytest.raises(ValueError, match=r"Invalid ability data in .*broken\.json"):
        AbilityDatabase.load(ability_dir)


def test_ability_database_length_and_iteration(tmp_path):
    ability_dir = tmp_path / "abilities"
    ability_dir.mkdir()
    write_ability(ability_dir)
    write_ability(
        ability_dir,
        filename="speed-boost.json",
        ability_id=3,
        ability_name="SPEED_BOOST",
        display_name="Speed Boost",
    )

    database = AbilityDatabase.load(ability_dir)

    assert len(database) == 2
    assert {ability.name for ability in database} == {"ADAPTABILITY", "SPEED_BOOST"}
