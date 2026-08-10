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
