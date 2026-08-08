import json

import pytest

from database.move_database import MoveDatabase
from move.move_category import MoveCategory
from pokemon_types import Type


def test_load_move_database(tmp_path):
    # Create a dummy move JSON file
    move_data = {
        "accuracy": 100,
        "category": "SPECIAL",
        "display_name": "Absorb",
        "effects": [],
        "id": 71,
        "move_flags": [],
        "move_name": "ABSORB",
        "move_type": "GRASS",
        "power": 20,
        "pp": 25,
        "priority": 0,
        "target": "SINGLE_TARGET",
    }

    move_dir = tmp_path / "moves"
    move_dir.mkdir()
    (move_dir / "absorb.json").write_text(json.dumps(move_data), encoding="utf-8")

    db = MoveDatabase.load(move_dir)

    assert len(db) == 1
    move = db.get("ABSORB")
    assert move.name == "ABSORB"
    assert move.accuracy == 100
    assert move.move_type == Type.GRASS
    assert move.category == MoveCategory.SPECIAL
    assert len(move.effects) == 0
    assert move.power == 20
    assert move.pp == 25
    assert move.display_name == "Absorb"
    assert move.id == 71


def test_load_move_database_missing_dir():
    with pytest.raises(ValueError, match="is not a directory"):
        MoveDatabase.load("non_existent_directory_12345")


def test_get_move_normalization(tmp_path):
    move_data = {
        "accuracy": 100,
        "category": "PHYSICAL",
        "display_name": "Tackle",
        "effects": [],
        "id": 33,
        "move_flags": [],
        "move_name": "TACKLE",
        "move_type": "NORMAL",
        "power": 40,
        "pp": 35,
        "priority": 0,
        "target": "SINGLE_TARGET",
    }
    move_dir = tmp_path / "moves"
    move_dir.mkdir()
    (move_dir / "tackle.json").write_text(json.dumps(move_data), encoding="utf-8")

    db = MoveDatabase.load(move_dir)

    assert db.get("tackle").name == "TACKLE"
    assert db.get("TACKLE").name == "TACKLE"
    assert db.get("Tackle").name == "TACKLE"


def test_load_move_invalid_target(tmp_path):
    move_data = {
        "accuracy": 100,
        "category": "PHYSICAL",
        "display_name": "Tackle",
        "effects": [],
        "id": 33,
        "move_flags": [],
        "move_name": "TACKLE",
        "move_type": "NORMAL",
        "power": 40,
        "pp": 35,
        "priority": 0,
        "target": "INVALID_TARGET",
    }
    move_dir = tmp_path / "invalid_moves"
    move_dir.mkdir()
    (move_dir / "tackle.json").write_text(json.dumps(move_data), encoding="utf-8")

    with pytest.raises(KeyError, match="INVALID_TARGET"):
        MoveDatabase.load(move_dir)
