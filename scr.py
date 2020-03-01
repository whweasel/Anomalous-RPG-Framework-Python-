#The game engine's CORE features.
from blessed import Terminal as Blessed
t = Blessed()
import re #used for the escape_ansi() method
import pickle

def raw_print(string):
    print(string, end='', flush=True)

class classproperty(object):
    def __init__(self, f):
        self.f = classmethod(f)
    def __get__(self, *a):
        return self.f.__get__(*a)()

class _Globals:
    standard_keys = ["KEY_ENTER", "Z".lower()]

class Style(str):
    """Styling"""
    def __init__(self, style):
        self.style = style
        self.raw_style = getattr(t, style)
    def __apply__(self, string):
        """Apply the style to a string"""
        return self.raw_style(string)
    def __repr__(self):
        return repr(self.raw_style)
    def __str__(self):
        return self.raw_style
    def __call__(self, string):
        """Gateway to __call__()"""
        return self.__apply__(string)
class Utility:
    """Utility methods, used for general things"""
    @staticmethod
    def strip_ansi(string):
        """Remove ANSI escape codes from a string, leaving behind just text"""
        return re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]').sub('', string) 
    @classmethod
    def splitstring(cls, string, length):
        newstr = cls.strip_ansi(string).splitlines()
        newstr1 = []
        for string in newstr:
            newstr1.extend([string[i:i+length] for i in range(0, len(string), length)])
        return newstr1
    @staticmethod
    def ms(milliseconds):
        """convert milliseconds to seconds"""
        return milliseconds/1000
    @staticmethod
    def strip_string(string, query):
        if query:
            while string.startswith(query):
                string = string[len(query):]
            while string.endswith(query):
                string = string[:-len(query)]
        return string
    @staticmethod
    def dict_to_object(obj, dict):
        for item in dict.items():
            setattr(
                obj,
                item[0],
                item[1]
            )
class Terminal:
    @staticmethod
    def sleep(seconds):
        """sleep, better alternative to SDL's time.sleep()"""
        with t.cbreak():
            t.inkey(timeout=seconds)
    @staticmethod
    def move_up(units = 1):
        raw_print(t.move_up(units))

    @staticmethod
    def move_down(units = 1):
        raw_print(t.move_down(units))

    @staticmethod
    def move_left(units = 1):
        raw_print(t.move_left(units))

    @staticmethod
    def move_right(units = 1):
        raw_print(t.move_right(units))

    @staticmethod
    def move_x(x):
        raw_print(t.move_x(x))
    
    @staticmethod
    def move_y(y):
        raw_print(t.move_y(y))
    
    @staticmethod
    def move_xy(x, y):
        raw_print(t.move_xy(x, y))
    
    @staticmethod
    def move_yx(y, x):
        raw_print(t.move_xy(y, x))
    
    @staticmethod
    def home():
        raw_print(t.home)
    
    @staticmethod
    def clear():
        """Clear the whole screen."""
        raw_print(t.clear)
    
    @staticmethod
    def clear_eol():
        """Clear to the end of the line."""
        raw_print(t.clear_eol)
    
    @staticmethod
    def clear_bol():
        """Clear backward to the beginning of the line."""
        raw_print(t.clear_bol)
    
    @staticmethod
    def clear_eos():
        """Clear to the end of screen."""
        raw_print(t.clear_eos)
    @staticmethod
    def clear_all():
        """Return cursor and clear screen"""
        raw_print(t.clear + t.home)

    @classproperty
    def width(cls):
        """The width of the terminal window"""
        return t.width

    @classproperty
    def height(cls):
        """The height of the terminal window"""
        return t.width

    @classproperty
    def number_of_colors(cls):
        """The number of colors by name"""
        return t.number_of_colors
class Keyboard:
    @staticmethod
    def getkey(timeout = None):
        """Keyboard input checking"""
        with t.cbreak():
            value = t.inkey(timeout = timeout)
            if value.is_sequence:
                value = value.name
        return value

    @classmethod
    def wait_for_keys(cls, keys):
        """Wait for a key in a list of keys to e pressed"""
        pressed_key = ''
        while pressed_key not in keys:
            pressed_key = Keyboard.getkey()
        return pressed_key
    
    @classmethod
    def wait_for_key(cls, key):
        """Wait for a specified key to be pressed"""
        pressed_key = ''
        while key != pressed_key:
            pressed_key = Keyboard.getkey()
        return pressed_key
class Data:
    queue = [] #empty list...
    @classmethod
    def queue_append(cls, object):
        """Append an object to the queue."""
        cls.queue.append(object)
    
    @classmethod
    def queue_remove(cls, object):
        cls.queue.remove(object)
    
    @classmethod
    def queue_clear(cls):
        cls.queue = []
    
    @classmethod
    def queue_dump(cls, filename):
        with open(filename, "wb") as f:
            pickle.dump(
                obj = cls.queue,
                file = f
            )
    
    @staticmethod
    def object_dump(object, filename):
        with open(filename, "wb") as f:
            pickle.dump(
                obj = object,
                file = f
            )
    
    @staticmethod
    def raw_load(filename):
        with open(filename, "rb") as f:
            return pickle.load(file = f)

    @staticmethod
    def load_as_object(filename, obj):
        with open(filename, "rb") as f:
            dict = pickle.load(file = f)
        Utility.dict_to_object(obj, dict)
class Menu:
    """Generate a menu"""
    highlight_style = Style("gold1")
    @classmethod
    def menu(cls, title, contents, delay=Utility.ms(27)):
        Keyboard.getkey(timeout = Utility.ms(27))
        print(t.home + t.clear, end='', flush=True)
        if type(contents) != dict:
            raise TypeError("Menu contents must be a dict.")
        with t.cbreak(): #event loop
            cursor_position = 1
            print(title)
            titlelen = Utility.splitstring(title, Terminal.width)
            while True:
                Terminal.move_y(len(titlelen))
                current_iter = 0
                for item in contents.items():
                    current_iter += 1
                    if current_iter == cursor_position:
                        print("  " + str(cls.highlight_style(item[1])), flush=True)
                        selected_choice = item[0]
                    elif current_iter != cursor_position:
                        print("  " + str(item[1]), flush=True)
                del item
                pressed_key = Keyboard.getkey()
                if pressed_key == "KEY_UP":
                    if cursor_position == 1:
                        cursor_position = len(contents)
                    elif cursor_position != 1:
                        cursor_position -= 1
                elif pressed_key == "KEY_DOWN":
                    if cursor_position == len(contents):
                        cursor_position = 1
                    elif cursor_position != len(contents):
                        cursor_position += 1
                elif pressed_key in ["KEY_ENTER", "Z".lower()]:
                    return selected_choice
class Game:
    @staticmethod
    def standard_wait():
        Keyboard.wait_for_keys(_Globals.standard_keys)
    
    @classmethod
    def dialogue(cls, character, msg):
        Terminal.clear_all()
        print("{char}:".format(char = character), flush=True)
        print("="*len(character), flush=True)
        print(msg, flush=True)
        cls.standard_wait()

    @classmethod
    def flavor_text(cls, msg):
        Terminal.clear_all()
        print(msg)
        cls.standard_wait()

    @classmethod
    def decormenu(cls, title, contents):
        """Customizable menu"""
        orig_contents = contents.copy()
        #You can define keys here, and then you can add
        contents = {}
        contents["helo"] = "Hi!"
        #end
        shallow_contents = contents.copy()
        contents.update(orig_contents)
        val = "{}{}{}{}FK"
        while val in list(shallow_contents.items())[0] or val == "{}{}{}{}FK":
            val = Menu.menu(title, contents)
        return val
