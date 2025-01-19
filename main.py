import dnd
import discordBot
import openai

def test():
    char1 = dnd.PlayableCharacter("Nabo Apelaum", background="Acolyte",player_class="Barbarian", alignment="Lawful Good", race="Human", player_subclass="Druid")
    item1 = dnd.get_item("shovel")
    char1.add_item(item1, 5)
    print(char1)
    print(char1.get_inventory())
    char1.save()
    char1.add_item(item1, 5)
    char1.save()
    pass
    

if __name__ == "__main__":
    test()
    
    pass
