import items
import random
from scr import Style
from scr import Menu
from scr import Terminal
from scr import Data
from scr import Game
gray = Style("gray52")


def getAttributes(clazz):
    """used to grab all attributes of a class, not methods"""
    return {name: attr for name, attr in clazz.__dict__.items()
            if not name.startswith("__") 
            and not callable(attr)
            and not type(attr) is staticmethod
            and not type(attr) is classmethod}

class Player(object):
    """base class for player operations"""
    @classmethod
    def initialize(cls, name):
        cls.name = name # The player's name
        cls.hp = 14 # The player's health
        cls.max_hp = 20 # The player's max health. This may increase over time
        cls.lv = 1 #The player's level. 
        cls.exp = 0 #The player's XP level (a.k.k experience). When this counter reaches 40, a level up happens.
        cls._def = 0
        cls.atk = 3
        cls.pin = random.randint(1000,9999) #A random number specific to the player.
        cls.inventory = [
            items.Phone(),
            items.Bar()
        ]
    
    @classmethod
    def lv_up(cls):
        """Used to increase the player's LV by one"""
        cls.lv += 1
        cls._def += 2
        cls.atk += 1
        cls.max_hp = cls.max_hp * 1.03

    @classmethod
    def add_exp(cls, val):
        """Add a specified amount of EXP to the player"""
        exp = cls.exp + val
        while exp <= 40:
            exp = exp - 40
            cls.lv_up()
        cls.exp = exp

    @classmethod
    def openinv(cls):
        """Open the player's inventory"""
        while True:
            inventory_items = {thing.id: thing.name for thing in cls.inventory}
            inventory_items["exit"] = "Exit Inventory"
            inventory_items["newln"] = ""
            inventory_items["playername"] = str(gray('"{}"'.format(cls.name)))
            inventory_items["lv"] = str(gray("LV: {}".format(cls.lv)))
            inventory_items["hp"] = str(gray("HP: {}/{}".format(cls.hp, cls.max_hp)))
            inventory_items["exp"] = str(gray("EXP: {}/40".format(cls.exp)))

            choice = Menu.menu(
                title = "Inventory",
                contents = inventory_items 
            )
            if choice == "exit":
                Terminal.clear_all()
                return
            while True:
                    displayed_item = next((thing for thing in cls.inventory if thing.id == choice), None)
                    final_choice = Menu.menu(
                        title = displayed_item.name,
                        contents = {
                            "interact":displayed_item.interact_label,
                            "inspect":"Inspect",
                            "drop":"Drop",
                            "back":"Back"
                        }
                    )
                    if final_choice == "back":
                        break
                    if final_choice == "interact":
                        use = displayed_item.interact()
                        Terminal.clear_all()
                        print(use["message"])
                        if "heal_" in use["action"]:
                            cls.hp += int(use["action"].replace("heal_", ''))
                            if cls.hp > cls.max_hp:
                                cls.hp = cls.max_hp
                            cls.inventory.remove(displayed_item)
                        Game.standard_wait()
                        break
                    if final_choice == "inspect":
                        Terminal.clear_all()
                        print(displayed_item)
                        Game.standard_wait()
                        continue
                    if final_choice == "drop":
                        Terminal.clear_all()
                        print("You dropped the {}".format(displayed_item.name))
                        cls.inventory.remove(displayed_item)
                        Game.standard_wait()
                        break

    @classmethod
    def save(cls):
        """Save the player's data to the user.dat file"""
        playerdata =  getAttributes(cls)
        Data.object_dump(playerdata, "savedata.dat")
        del playerdata
    @classmethod
    def load(cls):
        """Load the save data from user.dat"""
        playerdata = Data.raw_load("savedata.dat")
        for key in playerdata:
            cls.name = playerdata["name"]
            cls.max_hp = playerdata["max_hp"]
            cls.hp = playerdata["hp"]
            cls.lv = playerdata["lv"]
            cls.exp = playerdata["exp"]
            cls.atk = playerdata["atk"]
            cls._def = playerdata["_def"]
            cls.inventory = playerdata["inventory"]
            cls.pin = playerdata["pin"]