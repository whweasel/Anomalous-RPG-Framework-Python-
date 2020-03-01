import random 
import string
from scr import Style

yellow = Style("gold1")
  
def ran_gen(size, chars=string.ascii_uppercase + string.digits): 
    """Return a seeded string"""
    return ''.join(random.choice(chars) for x in range(size)) 

class Item(object):
    """Base class for all in-game items"""
    def __init__(self, name, description, value, interact_label, interact_action, interact_message = "Nothing"):
        self.name = name
        self.description = description
        self.value = value
        self.interact_label = interact_label
        self.interact_action = interact_action
        self.interact_message = interact_message
        self.id = (ran_gen(8, "AEIOSUMA23"))

    def __repr__(self):
        return (repr(self.name), self.id)
    def interact(self):
        """Called when Item is toggled"""
        return {
            "message":self.interact_message,
            "action":self.interact_action
        }
    def __str__(self):
        """Called when str() is used on an Item, or when it is printed"""
        return yellow("{}".format(self.name)) + "\n=====\n{}\nValue: {}".format(self.description, self.value)
class Phone(Item):
    """Nothing here"""
    def __init__(self):
        super(Phone, self).__init__(name="Phone",
                             description="An old phone, with your name written on the back.",
                             value=20,
                             interact_label = "Check",
                             interact_action = "check_phone",
                             interact_message = "No missed calls."),
class Bar(Item):
    def __init__(self):
        super(Bar, self).__init__(name="Bar",
                             description="Restores 6 HP.",
                             value=4,
                             interact_label = "Consume",
                             interact_action = "heal_6",
                             interact_message = "You consumed the Bar. 6 HP restored")
"""
class Weapon(Item):
    #Base class for all weapons
    def __init__(self, name, description, value, damage, useType, use):
        self.damage = damage
        super().__init__(name, description, value, useType = "Equip",
                             use = {"msg":"You equipped the {}".format(name), "action":"none"})
"""
""" 
class Gun(Weapon):
    def __init__(self):
        super().__init__(name="Glock 23 Gen 4", description="A capable firearm.", damage=30, value=3000, useType = "[Nothing]",
                             use = {"msg":"Be careful with this.", "action":"none"})
 """
 # NOT INCLUDED, BUT NOT REMOVED. MAY BE USED LATER.