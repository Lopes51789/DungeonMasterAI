import requests
import json
from dataclasses import dataclass, field

@dataclass
class Spell:
    index: str
    name: str
    desc: list
    higher_level: list
    range: str
    components: list
    material: str
    ritual: bool
    duration: str
    concentration: bool
    casting_time: str
    level: int
    school: str
    classes: list
    subclasses: list
    damage: dict
    dc: dict
    area_of_effect: dict
    url: str
    updated_at: str

def get_spell(spell_name = "NaN"):
    """
    Given a spell name, returns a Spell object with the properties of the spell. If the given name is "NaN", returns None.
    """
    ulr = "https://www.dnd5eapi.co/api/spells/" + spell_name
    response = requests.get(ulr)
    if response.status_code == 200:
        return Spell(**response.json())
    return None

@dataclass
class Item:
    desc: list
    special: list
    index: str
    name: str
    equipment_category: dict
    gear_category: dict
    cost: dict
    weight: str
    url: str
    updated_at: str
    contents: list
    properties: list

def get_item(item_name = "NaN"):
    """
    Given an item name, returns an Item object with the properties of the item. If the given name is "NaN", returns None.
    """
    url = "https://www.dnd5eapi.co/api/equipment/" + item_name
    response = requests.get(url)
    if response.status_code == 200:
        return Item(**response.json())
    return None

class PlayableCharacter:
    valid_backgrounds = ["Acolyte", "Charlatan", "Criminal", "Entertainer", "Folk Hero", "Guild Artisan", "Hermit", "Noble", "Outlander", "Sage", "Sailor", "Soldier", "Urchin"]
    valid_alignments = ["Lawful Good", "Lawful Neutral", "Lawful Evil", "Neutral Good", "Neutral Neutral", "Neutral Evil", "Chaotic Good", "Chaotic Neutral", "Chaotic Evil"]
    valid_races = ["Dragonborn", "Dwarf", "Elf", "Gnome", "Half-Elf", "Halfling", "Half-Orc", "Human", "Tiefling"]
    valid_classes = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
    def __init__(self, name = None, background = None, alignment = None, race = None, player_class = None, player_subclass = None):
        self.name = name
        if background not in self.valid_backgrounds:
            raise ValueError(f"Invalid background: {background}. Must be one of: {', '.join(self.valid_backgrounds)}")
        if alignment not in self.valid_alignments:
            raise ValueError(f"Invalid alignment: {alignment}. Must be one of: {', '.join(self.valid_alignments)}")
        if race not in self.valid_races:
            raise ValueError(f"Invalid race: {race}. Must be one of: {', '.join(self.valid_races)}")
        if player_class not in self.valid_classes:
            raise ValueError(f"Invalid class: {player_class}. Must be one of: {', '.join(self.valid_classes)}")
        if player_subclass not in self.valid_classes:
            raise ValueError(f"Invalid subclass: {player_subclass}. Must be one of: {', '.join(self.valid_classes)}")
        
        self.background = background
        self.alignment = alignment
        self.race = race
        self.player_class = player_class
        self.player_subclass = player_subclass        
        self.inventory = {}
        self.carry_capacity = 100 #depends from race
        self.carry_current = 0
        self.equipped_items = {"Head": None, "Body": None, "Cape": None, "Hands": None, "Feet": None, "Main Hand": None, "Off Hand": None}
        self.spells = []
        self.__level = 1
        self._level_acm = 0
        self._level_threshold = 100

    def get_player_name(self):
        return self.name
    
    def get_level(self):
        return self.__level
    
    def get_inventory(self):
        return self.inventory
    
    def get_spells(self):
        return self.spells
    def set_level(self, level):
        self.__level = level
    def __str__(self):
        return f"{self.name} is a {self.background} {self.alignment} {self.race} {self.player_class}"
    
    def can_level_up(self):
        if self.level < 20 and self.level_acm >= self.level_threshold:
            return True
        return False

    def level_up(self):
        """
        If the player has enough accumulated experience, they level up.
        
        If the player is not already at the maximum level (20), and they have
        enough accumulated experience to exceed the threshold, the player's
        level is increased by one, and the accumulated experience is reset to
        zero. The threshold is then increased by a factor of 20.

        Returns:
            None
        """
        if self.can_level_up():
            self.set_level(self.get_level() + 1)
            self.level_acm = 0
            self.level_threshold *= 20

    def can_add_spell(self, spell: Spell):
        """
        Checks if a player can add a given spell to their spellbook.

        Checks if the spell is of a level that the player can cast, and if it is
        of a class or subclass that the player is capable of casting.

        Args:
            spell: The spell to check.

        Returns:
            True if the player can add the spell, False otherwise.
        """
       
        classes = [cls["name"] for cls in spell.classes]
        subclasses = [subcls["name"] for subcls in spell.subclasses]
        
        if spell.level <= self.__level and (self.player_class in classes or self.player_subclass in subclasses):
            return True
        return False
    

    def add_spell(self, spell: Spell):
        """
        Adds a spell to the character's list of spells.

        Args:
            spell: A Spell object representing the spell to be added.

        Returns:
            None
        """
        if self.can_add_spell(spell):
            self.spells.append(spell.name)
        else:
            print(f"{spell.name} is not a spell for your class.")


    def can_add_item(self, item: Item, quantity = 1):
        if self.carry_current + (item.weight * quantity) <= self.carry_capacity:
            return True
        return False

    def add_item(self, item: Item, quantity = 1):
        """
        Adds an item to the character's inventory.

        Args:
            item: An Item object representing the item to be added.

        Returns:
            None
        """
        if self.can_add_item(item, quantity):
            if item.name not in self.inventory:
                self.inventory[item.name] = quantity
            elif item.name in self.inventory:
                self.inventory[item.name] += quantity
            self.carry_current += (item.weight * quantity)

        else:
            print(f"{item.name} is too heavy for you to carry.")

    def use_consumable_item(self, item: Item):
        """
        Removes one instance of the given item from the character's inventory.

        If the given item is in the character's inventory, and the character has
        more than one of the given item, the count of the item in the inventory
        is decremented by one. If the character has only one of the given item,
        the item is removed from the inventory.

        If the given item is not in the character's inventory, a message is
        printed to the console indicating this.

        Args:
            item: An Item object representing the item to be removed.

        Returns:
            None
        """
        if item in self.inventory:
            if self.inventory[item] > 1:
                self.inventory[item] -= 1
            else:
                self.inventory.pop(item)

        else:
            print(f"{item} is not in your inventory.")

    def _toJson(self):
        data = {
            "name": self.name,
            "background": self.background,
            "alignment": self.alignment,
            "race": self.race,
            "player_class": self.player_class,
            "player_subclass": self.player_subclass,
            "inventory": self.inventory,
            "carry_capacity": self.carry_capacity,
            "carry_current": self.carry_current,
            "equipped_items": self.equipped_items,
            "spells": self.spells,
            "level": self.__level,
            "level_acm": self._level_acm,
            "level_threshold": self._level_threshold
        }
        return json.dumps(data, indent=4)
    
    def toJsonFile(self):
        with open(f"{self.name}.json", "w") as f:
            f.write(self._toJson())
    
def test():
    """fireball = get_spell("fireball")
    print(fireball.name)

    pc1 = PlayableCharacter("Char1", player_class="Wizard")
    print(pc1)

    shovel = get_item("shovel")
    print(shovel)"""

    """spell = get_spell("fireball")
    print(spell)"""


    pass

if __name__ == "__main__":
    test()