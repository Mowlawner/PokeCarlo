import json

import pytest

from database.learnset_database import LearnsetDatabase


def write_learnset(directory, filename="garchomp.json", **overrides):
    data = {
        "moves": ["TACKLE", "EARTHQUAKE"],
        "pokemon": "GARCHOMP",
        "version_group": "CHAMPIONS",
    }
    data.update(overrides)
    (directory / filename).write_text(json.dumps(data), encoding="utf-8")


def test_load_learnset_and_normalize_form_name(tmp_path):
    write_learnset(
        tmp_path,
        filename="garchomp-mega.json",
        pokemon="GARCHOMP-MEGA",
        moves=["DRAGON-CLAW"],
    )

    database = LearnsetDatabase.load(tmp_path)

    assert database.get("garchomp-mega") == frozenset({"DRAGON_CLAW"})
    assert database.get("GARCHOMP_MEGA") == database.get("garchomp-mega")


def test_learnset_database_length_and_iteration(tmp_path):
    write_learnset(tmp_path)
    write_learnset(
        tmp_path,
        filename="gyarados.json",
        pokemon="GYARADOS",
        moves=["TACKLE"],
    )

    database = LearnsetDatabase.load(tmp_path)

    assert len(database) == 2
    assert set(database) == {
        frozenset({"TACKLE", "EARTHQUAKE"}),
        frozenset({"TACKLE"}),
    }


def test_missing_learnset_directory():
    with pytest.raises(ValueError, match="is not a directory"):
        LearnsetDatabase.load("missing_learnset_directory_12345")


def test_malformed_learnset_json(tmp_path):
    (tmp_path / "broken.json").write_text("{", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid learnset data.*broken.json"):
        LearnsetDatabase.load(tmp_path)
