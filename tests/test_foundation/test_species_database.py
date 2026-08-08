import json

import pytest

from database.species_database import SpeciesDatabase
from pokemon_types import Type


def write_species(directory, filename="garchomp.json", **overrides):
    data = {
        "abilities": ["ROUGH_SKIN", "SAND_VEIL"],
        "base_stats": {
            "attack": 130,
            "defense": 95,
            "hp": 108,
            "sp_attack": 80,
            "sp_defense": 85,
            "speed": 102,
        },
        "display_name": "Garchomp",
        "name": "GARCHOMP",
        "national_dex": 445,
        "pokemon_id": 445,
        "species_name": "GARCHOMP",
        "types": ["DRAGON", "GROUND"],
    }
    data.update(overrides)
    (directory / filename).write_text(json.dumps(data), encoding="utf-8")


def test_load_species_database_parses_static_fields(tmp_path):
    write_species(tmp_path)

    species = SpeciesDatabase.load(tmp_path).get("GARCHOMP")

    assert species.name == "GARCHOMP"
    assert species.display_name == "Garchomp"
    assert species.species_name == "GARCHOMP"
    assert species.pokemon_id == 445
    assert species.national_dex == 445
    assert species.types == (Type.DRAGON, Type.GROUND)
    assert species.base_stats.attack == 130
    assert species.abilities == ("ROUGH_SKIN", "SAND_VEIL")


def test_species_lookup_normalizes_names(tmp_path):
    write_species(tmp_path, name="TACKLE_TEST", display_name="Tackle-Test")
    database = SpeciesDatabase.load(tmp_path)

    assert database.get("tackle-test") is database.get("TACKLE_TEST")
    assert database.get("Tackle Test").name == "TACKLE_TEST"


def test_missing_directory():
    with pytest.raises(ValueError, match="is not a directory"):
        SpeciesDatabase.load("missing_species_directory_12345")


def test_malformed_json(tmp_path):
    (tmp_path / "broken.json").write_text("{", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid species data.*broken.json"):
        SpeciesDatabase.load(tmp_path)


def test_missing_required_field(tmp_path):
    write_species(tmp_path)
    data = json.loads((tmp_path / "garchomp.json").read_text())
    del data["base_stats"]
    (tmp_path / "garchomp.json").write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid species data.*base_stats"):
        SpeciesDatabase.load(tmp_path)


def test_missing_canonical_name(tmp_path):
    write_species(tmp_path)
    data = json.loads((tmp_path / "garchomp.json").read_text())
    del data["name"]
    (tmp_path / "garchomp.json").write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid species data.*name"):
        SpeciesDatabase.load(tmp_path)


@pytest.mark.parametrize(
    "overrides",
    [
        {"pokemon_id": 0},
        {"types": ["NOT_A_TYPE"]},
        {"abilities": "ROUGH_SKIN"},
        {"display_name": ""},
        {"name": "garchomp"},
    ],
)
def test_invalid_field_values(tmp_path, overrides):
    write_species(tmp_path, **overrides)

    with pytest.raises(ValueError, match="Invalid species data"):
        SpeciesDatabase.load(tmp_path)


def test_duplicate_form_names_raise(tmp_path):
    write_species(tmp_path)
    write_species(
        tmp_path,
        filename="duplicate.json",
        pokemon_id=10000,
        name="GARCHOMP",
        display_name="Garchomp",
    )

    with pytest.raises(ValueError, match="Duplicate species name 'GARCHOMP'"):
        SpeciesDatabase.load(tmp_path)


def test_length_and_iteration(tmp_path):
    write_species(tmp_path)
    write_species(
        tmp_path,
        filename="mega.json",
        name="GARCHOMP_MEGA",
        display_name="Garchomp Mega",
        pokemon_id=10001,
    )
    database = SpeciesDatabase.load(tmp_path)

    assert len(database) == 2
    assert {entry.name for entry in database} == {"GARCHOMP", "GARCHOMP_MEGA"}


def test_alternate_forms_are_distinct(tmp_path):
    write_species(tmp_path)
    write_species(
        tmp_path,
        filename="mega.json",
        name="GARCHOMP_MEGA",
        display_name="Garchomp Mega",
        pokemon_id=10001,
        base_stats={
            "attack": 170,
            "defense": 115,
            "hp": 108,
            "sp_attack": 120,
            "sp_defense": 95,
            "speed": 92,
        },
    )
    database = SpeciesDatabase.load(tmp_path)

    assert (
        database.get("GARCHOMP").pokemon_id != database.get("GARCHOMP_MEGA").pokemon_id
    )
    assert database.get("GARCHOMP_MEGA").base_stats.attack == 170


def test_display_name_does_not_determine_canonical_name(tmp_path):
    write_species(tmp_path, name="GARCHOMP_MEGA", display_name="Mega Garchomp")

    database = SpeciesDatabase.load(tmp_path)

    assert database.get("GARCHOMP_MEGA").name == "GARCHOMP_MEGA"
    with pytest.raises(KeyError):
        database.get("MEGA_GARCHOMP")


def test_load_actual_generated_species_directory():
    database = SpeciesDatabase.load("src/data/generated/pokemon")

    assert len(database) > 100
    assert database.get("GARCHOMP").species_name == "GARCHOMP"
