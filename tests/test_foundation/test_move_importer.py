from database.move_importer import MoveImporter


def test_move_importer_normalizes_status_effect_descriptor():
    move = MoveImporter().to_database_model(
        {
            "id": 86,
            "name": "thunder-wave",
            "type": {"name": "electric"},
            "damage_class": {"name": "status"},
            "power": None,
            "accuracy": 90,
            "pp": 20,
            "priority": 0,
            "target": {"name": "selected-pokemon"},
            "flags": [],
            "effects": [{"type": "status", "status": "paralysis"}],
        }
    )

    assert move["effects"] == [{"type": "status", "status": "PARALYSIS"}]


def test_move_importer_preserves_canonical_status_chance():
    effect = MoveImporter()._normalize_effect(
        {"type": "status", "status": "burn", "chance": 10}
    )

    assert effect == {"type": "status", "status": "BURN", "chance": 10}
