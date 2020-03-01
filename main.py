#"Anomalous" game engine.
from scr import classproperty #properties, but for classes, instead of instances.
from scr import _Globals as scr_gl #set standard keys
from scr import Style #styling
from scr import Utility #utilities, general purpose
from scr import Terminal #clearing screen n stuff
from scr import Keyboard #getkey() and others
from scr import Data #file interaction
from scr import Menu #menus
from scr import Game #game-related functions


gray = Style("gray52")
yellow = Style("gold1")
underline = Style("underline")
red = Style("red1")

game_title = "Your Game Title" #Title of your game.
game_title_color = red 

import items
import player
import rpg
import sys

class GameManager:
    """Manage game stuff, such as what do do and such"""
    game_states = [
        rpg.Part1.home_1,
        rpg.Part1.home_2
    ]
    #List all these states
    @classmethod
    def newgame(cls):
            for save in cls.game_states:
                player.Player.saved = save.__name__
                player.Player.save()
                save()
                Terminal.clear_all()
                player.Player.save()
    @classmethod
    def run_continue(cls):
            try:
                eff = Data.raw_load("savedata.dat")
            except:
                Terminal.clear_all()
                print("No save file exists. Try starting a new game.")
                Game.standard_wait()
                return
            for funct in cls.game_states:
                if funct.__name__ == eff["saved"]:
                    i = cls.game_states.index(funct)
                    break
            player.Player.load()
            saves = cls.game_states[i:]
            for save in saves:
                player.Player.saved = save.__name__
                player.Player.save()
                save()
                Terminal.clear_all()
                player.Player.save()


class Main:
    @staticmethod
    def show_instructions():
        Terminal.clear_all()
        print("Controls:", end='\n')
        print(gray("[ARROW UP]: Move cursor position up"))
        print(gray("[ARROW DOWN]: Move cursor position DOWN"))
        print(gray("[Z]/[ENTER]: Confirm selection"))
        print("MAKE SURE YOU PLAY IN FULLSCREEN! MENUS WON'T WORK PROPERLY IF YOU AREN'T IN FULLSCREEN! (or at least, by opening the repl in another window)")
        print(yellow("Press [ENTER] to continue."))
        Game.standard_wait()
    
    @classmethod
    def help_credits(cls):
        """Replace the text in this function with whatever suits you!
        Just make sure to credit me"""
        Terminal.clear_all()
        print("{title}.".format(title = cls.game_title))
        print("Powered by Anomalous: ")
        print(underline(
            "https://github.com/eidhernan/-Anomalous-Game-Engine-Python-"
        ))
        print("(put your license here)")
        Game.standard_wait()

    @staticmethod
    def newgame(): #When the user decides to make a new game
        while True:
            Terminal.clear_all()
            print("Name your character.")
            player_name = input(">")
            choice = Menu.menu(
                title = "Are you sure you want the name, '" + yellow(player_name) + "'?",
                contents = {
                    "yes":"Yes",
                    "no":"No"}
            )
            if choice == "yes":
                break
            elif choice == "no":
                continue
        player.Player.initialize(player_name) #Initialize the player class
        GameManager.newgame()
    @classmethod
    def title_screen(cls):
        state = "menu"
        Terminal.clear_all()
        while True: #state machine loop
            if state == "menu":
                state = Menu.menu(
                    title = cls.game_title_color(cls.game_title),
                    contents = {
                        "newgame":"New game",
                        "continue":"Continue",
                        "credits":"Credits",
                        "quit":"Quit"
                    }
                )
            if state == "newgame":
                cls.newgame()
                state = "menu"
            if state == "quit":
                sys.exit("Exited!")
            if state == "continue":
                GameManager.run_continue()
                state = "menu"
            if state == "credits":
                cls.help_credits()
                state = "menu"
                
        
        

    @classmethod
    def main(cls, *args, **kwargs):
        cls.game_title = kwargs["title"]
        cls.game_title_color = kwargs["color"]
        cls.show_instructions()
        cls.title_screen()
        


    ### END OF IMPORTS ###

if __name__ == '__main__':
    Main.main(
        title = game_title,
        color = game_title_color
    )