'''Garrett Langford This is the game. Many functions to let the player play the game with the hopes of completions.
Either by staving or by escaping with the grapple hook.

I certify that this code is mine, and mine alone, in accordance with GVSU academic honesty policy.

December 6th 2023
'''

from Item import Item
from Location import Location

'''' 
This is the final code for the game and will be what the player will see. There are all the main functions and 
they all can be used to the player to help the escape the tunnel system
'''


class Game:

    # stuff the game needs to run
    def __init__(self):
        self.list_items = []
        self.list_locations = []
        self.create_world()
        self.current_location = self.starting_location
        self.msg = ""
        self.welcome_message = ("You fell in a hole and are trying to escape, be careful on how much you move because "
                                "each time you change location, you become more and more hungry")
        self.Item = Item
        self.loc = Location
        self.hunger = 100
        self.auto_win_msg = ''

    # eat function allows items in the players inventory to be eaten and also rests the played food bar to 100
    def eat(self, name):
        item_to_eat = self.search_pouch(name)

        # checks to make sure the player actually has items
        if item_to_eat is None:
            self.msg = f"You are not holding {name}."

        # if play has items allows the items to be eaten
        else:

            # checks if the item is edible and returns the item that got ate and rests the played hunger.
            if item_to_eat.is_edible():
                self.hunger = 100
                self.list_items.remove(item_to_eat)
                self.msg = f"You successfully ate the {item_to_eat.get_name()} and are no longer holding it."

            # if the item isn't edible updates the game message to that the item isn't edible
            else:
                self.msg = f"The {item_to_eat.get_name()} is not edible."
        return self.msg

    # takes 10 points from hunger
    def strave(self):
        self.hunger = self.hunger - 10

    # main function that the player uses to play the game
    def start(self):
        print(self.get_message())
        print(f"your hunger level is {self.hunger}")

        # Loops untill the player either wins or loses
        while True:
            first, second = self.parse_command()

            # lets the player us the go funtion and prints the corresponding message
            if first == "go":
                self.go(second)
                self.strave()
                print(self.msg)
                print(self.current_location.__str__())

            # lets the player use the look functions and prints the corresponding message
            elif first == "look":
                self.look()
                print(self.msg)

            # lets the player use the list funtion and prints the corresponding message
            elif first == "list":
                self.list()
                print(self.msg)

            # lets the player use the pickup funtion and prints the corresponding message
            elif first == "pickup":
                self.pickup()
                print(self.msg)
            # lets the player use the go funtion and prints the corresponding message
            elif first == "drop":
                self.drop(second)
                print(self.msg)

            # lets the player use the go funtion and prints the corresponding message
            elif first == "search_pouch":
                self.search_pouch(second)
                print(self.msg)

            # lets the player use the eat funtion and prints the corresponding message
            elif first == "eat":
                self.eat(second)
                print(f"Your hunger is at {self.get_hunger()}")
                print(self.msg)

            # checks to see if the game is over before restarting the loop
            if self.game_over() == True:
                break
        print(self.msg)

    #  Go updates the players location to the direction the player wants to go,
    #  it also locks the blocked room from being accessible without placing tnt
    def go(self, dir):

        # checks to see if players location is none trying to eliminate erros I was getting
        if self.current_location is not None:
            new_location = self.current_location.get_neighbor(dir)

            # chskcs if players location is Deposits_continued
            if self.current_location == self.Deposits_continued:

                # checks if player is trying to go east into the blocked room
                if dir == 'east':

                    # if player is trying to go to The blocked room and makes sure that the tnt is placed
                    if self.current_location.get_item() == self.tnt:
                        new_location = self.The_blocked_room
                        self.current_location = new_location

                        self.msg = f'Your hunger is at {self.get_hunger()}'
                        self.auto_win_msg = f"You are now in {new_location}"

                    # if player doesnt have tnt updates game message
                    else:
                        self.msg = f'you cant go that way you need tnt'

                # if player isnt in thr Deposits_continued allows them to move to the rest of the map
                else:
                    new_location = self.current_location.get_neighbor(dir)
                    self.current_location = new_location
                    self.msg = f'Your hunger is at {self.get_hunger()}'
                    self.auto_win_msg = f"You are now in {new_location}"

            # trying to prevent players direction to becoming none
            elif new_location is not None:
                new_location = self.current_location.get_neighbor(dir)
                self.current_location = new_location
                self.msg = f'Your hunger is at {self.get_hunger()}'
                self.auto_win_msg = f"You are now in {new_location}"

            # updates message if player is trying to go a direction that they cant go
            else:
                self.msg = "You can't go that way"

        # updates message if player is trying to go a direction that they cant go
        else:
            self.msg = "You can't go that way"

    # returns hunger level
    def get_hunger(self):
        return self.hunger

    # determines the conditions of when the game is over
    def game_over(self):

        # if player hunger is 0 then the game is over switched it from == to <
        # because the game was ending when hunger was at 10 for some reason, The player loses if this happens
        if self.hunger < 0:
            self.msg = 'You starved!'
            return True

        #  if they are in the main pit
        if self.get_current_location() == self.Main_pit:

            # detriments if the play has the grapple hook
            for item in self.list_items:

                # if they do then game is over
                if item.get_name() == "grapple hook":
                    self.msg = "You have successfully escaped the cave!"
                    return True

            # games not over
            else:
                return False

        # games not over
        return False

    # tells the play the win conditions
    def help(self):
        self.msg = 'you need to find the grapple hook and be in the main pit to get out of here'

    # checks if player has an item
    def search_pouch(self, name):
        for item in self.list_items:
            if item.get_name() == name:
                return item
        return None

    # picks up an item from the current location
    def pickup(self):
        self.current_location = self.get_current_location()

        # makes sure location has item
        if self.current_location.has_item():
            item_to_pickup = self.current_location.get_item()

            # makes sure items weight isn't too heavy
            if item_to_pickup.get_weight() >= 50:
                self.msg = f"The {item_to_pickup.get_name()} is too heavy"
                return self.msg

            # if item is too heavy then its not picked up
            else:
                self.list_items.append(item_to_pickup)
                self.current_location.remove_item()
                self.msg = f"You are now holding the {item_to_pickup.get_name()}."
                return self.msg

        # if there is no item this is returned
        else:
            self.msg = "There is no item here to pick up."
            return self.msg

    # Drops an item in the current location
    def drop(self, name):
        item_drop = None

        # a for loop to check items in the list for the name of the item
        for item in self.list_items:
            if item.get_name() == name:
                item_drop = item
                break

        # checks to maksure you have an item
        if item_drop is not None:
            self.current_location.set_item(item_drop)
            self.list_items.remove(item_drop)
            self.msg = f"Dropped {item_drop.get_name()} at {self.current_location.get_description()}."

        # if item isnt in the players inventory then this message appears
        else:
            self.msg = "Item not found in your inventory."
        return self.msg

    # sets the welcome message at the begging of the game
    def set_welcome_message(self):
        self.welcome_message = "You fell in a hole and are try to escape be carful on how much you movie because each time you change location you become more and more hungry"

    # returns the welcome message
    def get_message(self):
        return self.welcome_message

    # This command was given to me by the instructions and is used in the start function to run the game.
    def parse_command(self):
        words = input("Enter>>> ").split()
        first = words[0]
        if len(words) > 1:
            second = words[1]
        else:
            second = None
        return first, second

    # returns the players current location
    def get_current_location(self):
        return self.current_location

    # returns the current locations description
    def look(self):
        self.msg = self.current_location.get_description()

    # creates all the items and all the locations with their neighbors and item inside that location.
    def create_world(self):

        # Items
        self.Beans = Item("beans", "The good stuff, last forever", 1, True)
        self.Copper_ore = Item("copper ore", 'Going to be worth a lot of $', 99, False)
        self.Grapple_hook = Item("grapple hook", "used to climb", 1, False)
        self.tnt = Item("tnt", "Old explosives, definitly still works", 5, False)
        self.Flint = Item("flint", "Used to excavate", 1, False)
        self.Knife = Item('old Knife', 'An old knife could be used to break somthing', 2, False)

        # Locations
        self.Main_pit = Location("Main pit", None)
        self.Deposits = Location("Deposits, Shiny ore on the walls must be copper", self.Copper_ore)
        self.Deposits_continued = Location(
            "Deposits continued, it ends here but it looks like theres more east but I need something to open the "
            "wall up a little",
            None)
        self.The_blocked_room = Location("The blocked room, its very dutsy from the rumble", self.Grapple_hook)
        self.Machinery_storage = Location("Machinery storage, a closet filled with old machines", self.Knife)
        self.Elevator_room = Location(
            "Elevator room, the elevator to the top doesn't work ", self.Flint)
        self.Sleep_quarters = Location("Sleeping quarters, These must be where the workers once lived", self.Beans)
        self.Locked_explosives_room = Location(
            "Locked explosives room, a bunch of shelves lined up filled with TNT better be careful", self.tnt)

        # adding neighbors
        self.Main_pit.add_neighbor("north", self.Deposits)
        self.Main_pit.add_neighbor("east", self.Elevator_room)
        self.Main_pit.add_neighbor("west", self.Machinery_storage)

        self.Deposits.add_neighbor("north", self.Deposits_continued)
        self.Deposits.add_neighbor("south", self.Main_pit)

        self.Deposits_continued.add_neighbor("south", self.Deposits)
        self.Deposits_continued.add_neighbor("east", self.The_blocked_room)

        self.The_blocked_room.add_neighbor("west", self.Deposits_continued)

        self.Machinery_storage.add_neighbor("north", self.Locked_explosives_room)
        self.Machinery_storage.add_neighbor("east", self.Main_pit)

        self.Elevator_room.add_neighbor("south", self.Sleep_quarters)
        self.Elevator_room.add_neighbor("west", self.Main_pit)

        self.Sleep_quarters.add_neighbor("north", self.Elevator_room)

        self.Locked_explosives_room.add_neighbor("south", self.Machinery_storage)

        # starting point
        self.starting_location = self.Main_pit

    # does what is need to be done to win fast
    def auto_win(self):
        g = Game()
        print(g.get_message())

        g.go('east')
        print(g.auto_win_msg)
        g.go('south')
        print(g.auto_win_msg)
        g.pickup()
        g.go('north')
        print(g.auto_win_msg)
        g.go('west')
        print(g.auto_win_msg)
        g.go('west')
        print(g.auto_win_msg)
        g.go('north')
        print(g.auto_win_msg)
        g.pickup()
        g.go('south')
        print(g.auto_win_msg)
        g.go('east')
        print(g.auto_win_msg)
        g.go('north')
        print(g.auto_win_msg)
        g.go('north')
        print(g.auto_win_msg)
        g.eat('beans')
        print(g.auto_win_msg)
        g.drop('tnt')
        print(g.auto_win_msg)
        g.go('east')
        print(g.auto_win_msg)
        g.go('west')
        print(g.auto_win_msg)
        g.go('south')
        print(g.auto_win_msg)
        g.go('south')
        print(g.auto_win_msg)
        g.game_over()
        print(g.msg)

    # returns a list of the players inventory
    def list(self):
        items_str = ""

        # go through the things the player has
        for item in self.list_items:
            items_str += f"- {item.get_name()}\n"

        # checks to see if item str undated and prints appropriate
        if items_str != '':
            self.msg = f"Your inventory:\n{items_str}"
        else:
            self.msg = "Your inventory is empty."

# code testing
if __name__ == '__main__':
    g = Game()
    g.start()
   # g.auto_win()
