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

def test_existing_character_no_inventory():
    char1 = dnd.PlayableCharacter("Char1")
    assert char1.get_inventory() == {}
    assert char1.get_spells() == []


def test_can_add_item():
    char1 = dnd.PlayableCharacter("Char1", player_class="Wizard")
    assert char1.can_add_item(dnd.get_item("shovel")) == True
    assert char1.can_add_item(dnd.get_item("shovel"), 9999999) == False

def test_add_item():
    char1 = dnd.PlayableCharacter("Char1", player_class="Wizard")
    char1.add_item(dnd.get_item("shovel"))
    assert char1.get_inventory() == {"Shovel": 1}

def test_can_add_spell():
    char1 = dnd.PlayableCharacter("Char1", player_class="Barbarian")
    char2 = dnd.PlayableCharacter("Char2", player_class="Wizard")
    char2.set_level(5)
    assert char1.can_add_spell(dnd.get_spell("fireball")) == False
    assert char2.can_add_spell(dnd.get_spell("fireball")) == True #not all spells have all of the properties

def test_set_level():
    char1 = dnd.PlayableCharacter("Char1", player_class="Barbarian")
    char1.set_level(5)
    assert char1.get_level() == 5
    