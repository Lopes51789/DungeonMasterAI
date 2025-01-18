import requests
import json
from dataclasses import dataclass

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
    def __init__(self, name = None, background = None, alignment = None, race = None, player_class = None):
        self.name = name
        self.background = background
        self.alignment = alignment
        self.race = race
        self.player_class = player_class
        self.inventory = {}
        self.spells = []
        self.level = 1
        self.__level_acm = 0
        self.__level_threshold = 100

    def get_player_name(self):
        return self.name
    
    def get_level(self):
        return self.level
    
    def get_inventory(self):
        return self.inventory
    
    def get_spells(self):
        return self.spells
    
    def __str__(self):
        return f"{self.name} is a {self.background} {self.alignment} {self.race} {self.player_class}"

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
        if self.level < 20 and self.level_acm >= self.level_threshold:
            self.level += 1
            self.level_acm = 0
            self.level_threshold *= 20

    def add_spell(self, spell: Spell):
        """
        Adds a spell to the character's list of spells.

        Args:
            spell: A Spell object representing the spell to be added.

        Returns:
            None
        """

        self.spells.append(spell)

    def add_item(self, item: Item):
        """
        Adds an item to the character's inventory.

        Args:
            item: An Item object representing the item to be added.

        Returns:
            None
        """

        self.inventory.append(item)

    def use_item(self, item: Item):
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
    
def test():
    fireball = get_spell("fireball")
    print(fireball.name)

    pc1 = PlayableCharacter("Char1")
    print(pc1)

    shovel = get_item("shovel")
    print(shovel.name)

    pass

if __name__ == "__main__":
    test()