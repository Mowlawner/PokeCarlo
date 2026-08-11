import json

import pytest

from database.move_database import MoveDatabase
from move.move_category import MoveCategory
from move_effects.damage_effect import DamageEffect
from move_effects.stat_change_effect import StatChangeEffect
from move_effects.status_effect import StatusEffect
from pokemon_types import Type
from stats.stat import Stat
from status_condition import StatusCondition


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
    assert len(move.effects) == 1
    assert isinstance(move.effects[0], DamageEffect)
    assert move.effects[0].power == 20
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


def test_load_move_database_constructs_explicit_stat_change_effect(tmp_path):
    move_dir = tmp_path / "moves"
    move_dir.mkdir()
    (move_dir / "swords-dance.json").write_text(
        json.dumps(
            {
                "accuracy": None,
                "category": "STATUS",
                "display_name": "Swords Dance",
                "effects": [{"type": "stat_change", "stat": "ATTACK", "stages": 2}],
                "id": 14,
                "move_flags": [],
                "move_name": "SWORDS_DANCE",
                "move_type": "NORMAL",
                "power": None,
                "pp": 20,
                "priority": 0,
                "target": "SELF",
            }
        ),
        encoding="utf-8",
    )

    move = MoveDatabase.load(move_dir).get("SWORDS_DANCE")

    assert len(move.effects) == 1
    assert isinstance(move.effects[0], StatChangeEffect)
    assert move.effects[0].stat is Stat.ATTACK
    assert move.effects[0].stages == 2


def test_load_move_database_constructs_explicit_status_effect(tmp_path):
    move_dir = tmp_path / "moves"
    move_dir.mkdir()
    (move_dir / "thunder-wave.json").write_text(
        json.dumps(
            {
                "accuracy": 90,
                "category": "STATUS",
                "display_name": "Thunder Wave",
                "effects": [{"type": "status", "status": "PARALYSIS"}],
                "id": 86,
                "move_flags": [],
                "move_name": "THUNDER_WAVE",
                "move_type": "ELECTRIC",
                "power": None,
                "pp": 20,
                "priority": 0,
                "target": "SINGLE_TARGET",
            }
        ),
        encoding="utf-8",
    )

    move = MoveDatabase.load(move_dir).get("THUNDER_WAVE")

    assert len(move.effects) == 1
    assert isinstance(move.effects[0], StatusEffect)
    assert move.effects[0].status is StatusCondition.PARALYSIS


def test_load_move_database_constructs_chance_bearing_status_effect(tmp_path):
    move_dir = tmp_path / "moves"
    move_dir.mkdir()
    (move_dir / "flamethrower.json").write_text(
        json.dumps(
            {
                "accuracy": 100,
                "category": "SPECIAL",
                "display_name": "Flamethrower",
                "effects": [
                    {"type": "damage", "power": 90},
                    {"type": "status", "status": "BURN", "chance": 10},
                ],
                "id": 53,
                "move_flags": [],
                "move_name": "FLAMETHROWER",
                "move_type": "FIRE",
                "power": 90,
                "pp": 15,
                "priority": 0,
                "target": "SINGLE_TARGET",
            }
        ),
        encoding="utf-8",
    )

    move = MoveDatabase.load(move_dir).get("FLAMETHROWER")

    assert len(move.effects) == 2
    assert isinstance(move.effects[0], DamageEffect)
    assert isinstance(move.effects[1], StatusEffect)
    assert move.effects[1].status is StatusCondition.BURN
    assert move.effects[1].chance == 10
