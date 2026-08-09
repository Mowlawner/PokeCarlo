from dataclasses import FrozenInstanceError

import pytest

from item import Item


def test_item_stores_static_metadata():
    item = Item(
        name="LEFTOVERS",
        display_name="Leftovers",
        id=211,
        category="HELD_ITEMS",
        attributes=("HOLDABLE", "HOLDABLE_ACTIVE"),
    )

    assert item.name == "LEFTOVERS"
    assert item.display_name == "Leftovers"
    assert item.id == 211
    assert item.category == "HELD_ITEMS"
    assert item.attributes == ("HOLDABLE", "HOLDABLE_ACTIVE")


def test_item_is_immutable_and_slotted():
    item = Item("LEFTOVERS", "Leftovers", 211, "HELD_ITEMS", ())

    with pytest.raises(FrozenInstanceError):
        item.name = "LIFE_ORB"

    assert not hasattr(item, "__dict__")


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("name", ""),
        ("display_name", ""),
        ("category", ""),
        ("id", 0),
        ("id", -1),
    ],
)
def test_item_rejects_invalid_fields(field, value):
    values = {
        "name": "LEFTOVERS",
        "display_name": "Leftovers",
        "id": 211,
        "category": "HELD_ITEMS",
        "attributes": (),
    }
    values[field] = value

    with pytest.raises((TypeError, ValueError)):
        Item(**values)


def test_item_rejects_duplicate_attributes():
    with pytest.raises(ValueError, match="cannot contain duplicates"):
        Item(
            "LEFTOVERS",
            "Leftovers",
            211,
            "HELD_ITEMS",
            ("HOLDABLE", "HOLDABLE"),
        )
