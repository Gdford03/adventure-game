
'''
Garrett Langford
This code is for my game class and will be used to make locations for the game.

I certify that this code is mine, and mine alone, in accordance with GVSU academic honesty policy.

December 6th 2023
'''
from Item import Item
"""
This class is used for the games location and determines what a location is and what is in the location.
This function is used to set the locations in the game.
"""
class Location:
    def __init__(self, desc, thing=None):
        self.desc = desc
        self.thing = thing
        self.neighbors = {}

    # returns item
    def get_item(self):
        return self.thing

    # sets an item in the location
    def set_item(self, thing):
        self.thing = thing

    # returns the description of the location
    def get_description(self):
        return self.desc

    # returns the item in location
    def has_item(self):
        return self.thing

    # adds a location next to the current location
    def add_neighbor(self, dir, loc):
        self.neighbors[dir] = loc

    # returns a locations neighbors
    def get_neighbor(self, dir):
        return self.neighbors.get(dir, None)

    # removes an item from a location
    def remove_item(self):
        remove = self.thing
        self.thing = None
        return remove



    # gives a sting for game function
    def __str__(self):
        full_desc = f'You are {self.desc}'

        # check if there is a thing in the location and changes full_description
        if self.thing != None:
            full_desc = f'You are {self.desc} \nYou see {self.thing.name} '
        return full_desc
