'''
================================================
                    Menus.py
================================================
Module for handling the different menus to
be displayed
================================================
'''

from Game import Game

# Parent class for the different menu types
class Menu(object):
    def __init__(self):
        self.menu_title = None
        self.active = False
        self.options = {}

    # Default start method
    # Loop which displays the menu until an option is selected
    def start(self):
        self.active = True
        while self.active:
            self.display()
            self.chooseOption()

    # Default toggleActive method
    # Inverts the active state
    def toggleActive(self):
        self.active = not self.active

    # Default display method
    # Iterates through the options dictionary and returns the keys
    def display(self):
        print(self.menu_title)
        for option in self.options.keys():
            print(option)
        print()

    # Default chooseOption method
    # Prompts the user to input one of the displayed options and executes if it is valid
    def chooseOption(self):
        option = input()
        try:
            keys = list(self.options)
            self.options[keys[int(option) - 1]]()
        except IndexError or KeyError:
            print("That is not a valid option, please enter the correct number for your choice.")
            chooseOption()

    # Default close method
    # Confirms the user wishes to exit and if so, exit the menu
    def close(self):
        check_user_is_sure = input("Are you sure you would like to quit? (y/n): ")
        if check_user_is_sure.lower() == "y":
            self.toggleActive()
            quit()
        elif check_user_is_sure.lower() == "n":
            self.display()
        else:
            print("Invalid option, please try again.\n")
            self.close()

# Child of Menu class
# Responsible for the Main Menu
class MainMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self.menu_title = "Main Menu"
        self.options = {
            "1. Start game" : self.startGame,
            "2. Quit" : self.close
        }

    def startGame(self):
        intro_choice_menu = IntroChoiceMenu()
        intro_choice_menu.start()

# Child of Menu class
# Responsible for the intro choice menu
class IntroChoiceMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self.menu_title = "Intro Choice"
        self.options = {
            "1. Fantasy" : self.startGame,
            "2. Quit" : self.close

        }
        self.intro_prompts = [
            "You enter a dungeon in a fantasy world."
        ]

    # Overridden chooseOption method
    # Prompts the user to input one of the displayed options and executes if it is valid
    def chooseOption(self):
        option = input()
        index = int(option) - 1
        try:
            keys = list(self.options)
            self.options[keys[index]](self.intro_prompts[index])
        except ValueError or IndexError or KeyError:
            try:
                keys = list(self.options)
                self.options[keys[index]]()
            except IndexError or KeyError:
                print("That is not a valid option, please enter the correct number for your choice.")
                chooseOption()

    def startGame(self, intro_choice):
        print("Intro: " + intro_choice)
        game_menu = GameMenu(Game(intro_choice))
        game_menu.start()

# Child of Menu class
# Responsible for the Game Menu
class GameMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self)
        self.game = game
        self.menu_title = "Game Menu"
        self.options = {
            "1. Prompt" : self.promptComputer,
            "2. Exit Game" : self.close
        }

    # Method which gives the user an interface with the machine learning algorithm
    def promptComputer(self):
        prompt = input("You: ")
        # Give prompt to the machine learning algorithm
        self.game.text_model.generate(prompt)
        print(self.game.text_model.getPrompts())

    # Override the close method to make it not quit() and instead just return
    # (in the loop this should simply go back to the main menu)
    def close(self):
        check_user_is_sure = input("Are you sure you would like to exit? (y/n): ")
        if check_user_is_sure.lower() == "y":
            self.toggleActive()
        elif check_user_is_sure.lower() == "n":
            self.display()
        else:
            print("Invalid option, please try again.\n")
            self.close()