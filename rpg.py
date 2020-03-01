#This is the main game file. This is where the story and stuff go.
from scr import classproperty #properties, but for classes, instead of instances.
from scr import _Globals as scr_gl #set standard keys
from scr import Style #styling
from scr import Utility #utilities, general purpose
from scr import Terminal #clearing screen n stuff
from scr import Keyboard #getkey() and others
from scr import Data #file interaction
from scr import Menu #menus
from scr import Game #game-related functions
import items
import player
"""
IMPORTANT!!!

For each state function (section of the game that has its own save),
be sure to list it in game_states, in the class GameManager, in main.py 

That is, so the game can run automatically, in a specific order of functions. Have fun!


"""
gray = Style("gray52")
yellow = Style("gold1")
underline = Style("underline")
red = Style("red1")


clear = Terminal.clear_all
wait = Game.standard_wait

def game_menu(title, choices):
    while True:
        choices["newln0"] = "=============="
        choices["inventory"] = "Inventory"
        choices["newln1"] = ""
        choices["playername"] = str(gray('"{}"'.format(player.Player.name)))
        choices["newln2"] = ""
        choices["lv"] = str(gray("LV: {}".format(player.Player.lv)))
        choices["hp"] = str(gray("HP: {}/{}".format(player.Player.hp, player.Player.max_hp)))
        choices["exp"] = str(gray("EXP: {}/40".format(player.Player.exp)))
        result = Menu.menu(title, choices)
        if result == "inventory":
            player.Player.openinv()
            continue
        elif result in ["newln0", "newln1", "playername", "hp", "lv", "exp", "newln2"]:
            continue
        elif result not in ["newln0", "inventory", "newln1", "playername", "hp", "lv"]:
            return result

class Part1:
    @staticmethod
    def home_1():
        clear()
        state = "wake_up_1"
        while True:
            #Infinite loop
            if state == "wake_up_1":
                state = game_menu(
                    title = "You wake up in the middle of a forest...",
                    choices = {
                        "fall_asleep_1":"Go back to sleep",
                        "get_up_1":"Get up"
                    }
                )
            if state == "fall_asleep_1":
               Game.flavor_text("You can't go back to sleep now!")
               state = "wake_up_1"

            if state == "get_up_1":
                Game.flavor_text("You get up from the grass...")
                Game.flavor_text("But wait... the developer never finished writing this story.")
                Game.flavor_text("But, you can. With this simple framework, you can rewrite this game to be whatever you want it to be, the code isn't that hard to understand (if you know python), and it is much better than the previous version.")
                Game.flavor_text("Simply fork this repl, study this sample game, and you'll be set to make your own RPG! ")
                break
    @staticmethod
    def home_2():
        game_menu(
            title = "Oh, and this is just to show you how continues work. Instead of starting a new game, hit continue, and you'll land on this page. Look at the code, and see how it works for yourself!",
            choices = {
                "ok":"Ok!"
            }
        )