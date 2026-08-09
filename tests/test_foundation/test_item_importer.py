import pytest

from database.item_importer import ItemImporter


def item_data():
    return {
        "attributes": [
            {"name": "holdable-active"},
            {"name": "holdable"},
        ],
        "category": {"name": "held-items"},
        "id": 211,
        "name": "leftovers",
        "names": [
            {"language": {"name": "fr"}, "name": "Restes"},
            {"language": {"name": "en"}, "name": "Leftovers"},
        ],
    }


def test_item_importer_maps_and_canonicalizes_fields():
    assert ItemImporter().to_database_model(item_data()) == {
        "item_id": 211,
        "item_name": "LEFTOVERS",
        "display_name": "Leftovers",
        "category": "HELD_ITEMS",
        "attributes": ["HOLDABLE", "HOLDABLE_ACTIVE"],
    }


def test_item_importer_uses_canonical_api_name_not_display_name():
    data = item_data()
    data["name"] = "choice-band"
    data["names"][1]["name"] = "Localized Presentation"

    result = ItemImporter().to_database_model(data)

    assert result["item_name"] == "CHOICE_BAND"
    assert result["display_name"] == "Localized Presentation"


def test_item_importer_requires_english_name():
    data = item_data()
    data["names"] = [{"language": {"name": "fr"}, "name": "Restes"}]

    with pytest.raises(ValueError, match="no English name"):
        ItemImporter().to_database_model(data)
