import dnd
import discordBot


def test_existing_spells():
    assert dnd.get_spell("fireball").name == "Fireball"


def test_non_existing_spells():
    assert dnd.get_spell("firebal") is None
    assert dnd.get_spell() is None

def test_existing_items():
    assert dnd.get_item("shovel").name == "Shovel"

def test_non_existing_items():
    assert dnd.get_item("shov") is None
    assert dnd.get_item() is None

def test_existing_characters():
    char1 = dnd.PlayableCharacter("Char1")
    assert char1


