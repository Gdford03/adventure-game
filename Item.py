'''
Garrett Langford This was the start of the project and It describes what an item is. There are descriptions and
other functions to help signify what each item can do

I certify that this code is mine, and mine alone, in accordance with GVSU academic honesty policy.

December 6th 2023
'''



''''
This class identifies what an item is and what an item can do.

'''''


class Item:
    def __init__(self, name, desc, weight, edible):
        self.name = name
        self.desc = desc
        self.weight = weight
        self.edible = edible

    # returns the string desc
    def __str__(self):
        return self.desc

    # checks to see if you can eat an item
    def set_edible(self, edible):
        self.edible = edible

    #
    def is_edible(self): # return True if the item is edible. Otherwise, return False
        return self.edible

    # returns the weight of an item
    def get_weight(self): #return the item weight
        return self.weight

    # returns the name of the item
    def get_name(self): # – return the item name
        return self.name

    # returns the description of the item
    def get_description(self):
        return self.desc

    # update the item weight
    def set_weight(self, weight):
        self.weight = weight

    # sets the items name
    def set_name(self, name):
        self.name = name
