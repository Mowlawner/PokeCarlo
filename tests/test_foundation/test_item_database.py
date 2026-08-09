import json

import pytest

from database.item_database import ItemDatabase


def write_item(directory, filename="leftovers.json", **overrides):
    data = {
        "attributes": ["HOLDABLE", "HOLDABLE_ACTIVE"],
        "category": "HELD_ITEMS",
        "display_name": "Leftovers",
        "item_id": 211,
        "item_name": "LEFTOVERS",
    }
    data.update(overrides)
    (directory / filename).write_text(json.dumps(data), encoding="utf-8")


def test_load_item_database_parses_all_fields(tmp_path):
    write_item(tmp_path)

    item = ItemDatabase.load(tmp_path).get("LEFTOVERS")

    assert item.name == "LEFTOVERS"
    assert item.display_name == "Leftovers"
    assert item.id == 211
    assert item.category == "HELD_ITEMS"
    assert item.attributes == ("HOLDABLE", "HOLDABLE_ACTIVE")


def test_item_lookup_normalizes_names(tmp_path):
    write_item(
        tmp_path,
        filename="choice-band.json",
        item_id=197,
        item_name="CHOICE_BAND",
        display_name="Choice Band",
        category="CHOICE",
        attributes=["HOLDABLE", "HOLDABLE_ACTIVE"],
    )
    database = ItemDatabase.load(tmp_path)

    assert database.get("CHOICE_BAND") is database.get("choice-band")
    assert database.get("Choice Band").id == 197


def test_missing_item_directory():
    with pytest.raises(ValueError, match="is not a directory"):
        ItemDatabase.load("missing_item_directory_12345")


def test_malformed_item_json(tmp_path):
    (tmp_path / "broken.json").write_text("{", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid item data.*broken.json"):
        ItemDatabase.load(tmp_path)


def test_missing_required_item_field(tmp_path):
    write_item(tmp_path)
    data = json.loads((tmp_path / "leftovers.json").read_text())
    del data["category"]
    (tmp_path / "leftovers.json").write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid item data.*category"):
        ItemDatabase.load(tmp_path)


@pytest.mark.parametrize(
    "overrides",
    [
        {"item_id": 0},
        {"item_name": ""},
        {"display_name": ""},
        {"category": ""},
        {"attributes": "HOLDABLE"},
    ],
)
def test_invalid_item_values(tmp_path, overrides):
    write_item(tmp_path, **overrides)

    with pytest.raises((TypeError, ValueError), match="Invalid item data"):
        ItemDatabase.load(tmp_path)


def test_duplicate_item_names_raise(tmp_path):
    write_item(tmp_path)
    write_item(
        tmp_path,
        filename="duplicate.json",
        item_id=999,
        display_name="Another Leftovers",
    )

    with pytest.raises(ValueError, match="Duplicate item name 'LEFTOVERS'"):
        ItemDatabase.load(tmp_path)


def test_item_database_length_and_iteration(tmp_path):
    write_item(tmp_path)
    write_item(
        tmp_path,
        filename="life-orb.json",
        item_id=247,
        item_name="LIFE_ORB",
        display_name="Life Orb",
    )
    database = ItemDatabase.load(tmp_path)

    assert len(database) == 2
    assert {item.name for item in database} == {"LEFTOVERS", "LIFE_ORB"}
