
import pandas as pd
pd.set_option('display.max_colwidth', None)

import json
import os
from PIL import Image, ImageQt



class Recipe:
    """Represents a recipe with title, ingredients, instructions, and image name"""

    def __init__(self, title, ingredients, instructions, image_name):
        """Initializes a new Recipe object

        Parameters:
            title (str): The title of the recipe
            ingredients (str): A list of ingredients, separated by commas
            instructions (str): A list of instructions, separated by line breaks
            image_name (str): The name of the image associated with the recipe
        """
        self.title = str(title)  # stores the title of the recipe
        self.ingredients = str(ingredients)  # stores the ingredients as a string
        self.instructions = str(instructions)  # stores the instructions as a string
        self.image_name = str(image_name)  # stores the name of the image associated with the recipe



class Pantry:
    def __init__(self):
        self.recipes = []
        self.previous_recipe = {i: "" for i in range(1, 11)}
        self.load_saved_recipes()
        self.previous_recipe_placeholder = 1

    def add_recipe(self, recipe):
        """Add a new recipe to the collection"""
        self.recipes.append(recipe)  # add the recipe to the list of recipes
        print(recipe.title)

    def get_recipe(self, title):
        """Find a recipe by title and return it, or None if not found"""
        for recipe in self.recipes:  # iterate over the recipes
            if recipe.title == title:  # check if the title matches
                return recipe  # return the matching recipe
        return None  # if no match is found, return None

    def remove_recipe(self, title):
        """Remove a recipe by title and return True if successful, or False if not found"""
        for i, recipe in enumerate(self.recipes):  # iterate over the recipes with indices
            if recipe.title == title:  # check if the title matches
                del self.recipes[i]  # delete the matching recipe
                return True  # return True if the recipe was removed
        return False  # if no match is found, return False


    def to_dict(self):
        """Converts the recipe list to a dictionary"""
        recipe_dict = {}  # initialize an empty dictionary
        for recipe in self.recipes:  # iterate over the recipes
            recipe_info = {  # create a dictionary to store the recipe info
                'title': recipe.title,  # add the title
                'ingredients': recipe.ingredients,  # add the ingredients
                'instructions': recipe.instructions,  # add the instructions
                'image_name': recipe.image_name  # add the image name
            }
            recipe_dict[recipe.title] = recipe_info  # add the recipe info to the main dictionary
        return recipe_dict  # return the completed dictionary


    def write_recipe_dict_to_json(self):
        """Writes the recipe dictionary to a JSON file"""
        filepath = r"archive\Sample.json"  # path to the JSON file

        with open(filepath, 'w') as f:  # open the file in write mode
            json.dump(self.to_dict(), f, indent=4)  # write the updated temp dictionary to the file, with indentation


    def load_saved_recipes(self):
        filepath = r"archive\Sample.json"  # path to the JSON file

        # Open the file in read mode
        with open(filepath, 'r') as f:
            # Load the JSON data into a dictionary
            recipe_dict = json.load(f)

        # Clear the existing recipes list
        self.recipes = []

        # Iterate over the recipes in the dictionary
        for title, recipe_info in recipe_dict.items():
            # Create a new Recipe object from the dictionary values
            recipe = Recipe(title, recipe_info['ingredients'], recipe_info['instructions'], recipe_info['image_name'])

            # Add the new recipe to the list
            self.recipes.append(recipe)


    def remove_recipe_from_json(self, title):
        """Removes a recipe from a JSON file"""
        filepath = r"archive\Sample.json"  # path to the JSON file
        with open(filepath, 'r') as f:  # open the file in read mode
            recipe_dict = json.load(f)  # load the JSON data into a dictionary

        if title in recipe_dict:  # check if the title is in the dictionary
            del recipe_dict[title]  # remove the recipe with the given title

        with open(filepath, 'w') as f:  # open the file in write mode
            json.dump(recipe_dict, f, indent=4)  # write the updated dictionary to the file, with indentation



    def add_previous_recipe(self, input_value):
        """
        Increments all key values in pevious_recipe_dictionary by one.
        Then assigns the input value to the first slot in the previous_recipe dictionary,
        """

        for key in reversed(range(1, 11)):
            temp_dict = self.previous_recipe.copy()
            if key > 1:
                temp_dict[key] = self.previous_recipe[key - 1]  # shift values down
            self.previous_recipe = temp_dict

        self.previous_recipe[1] = input_value  # assign the input value to the "wrapped around" slot

        return


    def __len__(self):
        return len(self.recipes)

    def __getitem__(self, index):
        return self.recipes[index]






class Cookbook:
    def __init__(self, dataframe=None):  # initialize the class with an optional dataframe parameter
        csv_loc = r"archive\Food Ingredients and Recipe Dataset with Image Name Mapping.csv"  # path to the CSV file
        self.dataframe = pd.read_csv(csv_loc, index_col=False)  # read the CSV file into a Pandas dataframe

    def print_database(self):  # print the entire dataframe
        print(self.dataframe)

    def get_random_recipe(self):
        """Fetch a random recipe from the dataframe"""
        random_row = self.dataframe.sample(1)  # sample a single row from the dataframe
        random_row = random_row.replace('\n', ' ', regex=True)  # replace newlines with spaces
        title = random_row['Title'].to_string(index=False)  # extract the title
        ingredients = random_row['Ingredients'].to_string(index=False)  # extract the ingredients
        instructions = random_row['Instructions'].to_string(index=False)  # extract the instructions
        image_name = random_row['Image_Name'].to_string(index=False)  # extract the image name
        recipe = Recipe(title, ingredients, instructions, image_name)  # create a Recipe object
        return recipe

    def search_recipes(self, search_term):
        """Search for recipe titles containing the given term using regex"""
        pattern = r"(?i)" + re.escape(search_term)  # ignore case and escape special chars
        matches = self.dataframe['Title'].str.contains(pattern, na=False)  # find matches in the Title column
        return list(self.dataframe['Title'][matches].values)  # return a list of matching titles

    def fetch_specific_recipe(self, title):
        """Fetch a specific recipe by title using exact regex match"""
        pattern = r"\b" + re.escape(title) + r"\b"  # word boundary escaping
        match = self.dataframe['Title'].str.match(pattern, na=False)  # find an exact match in the Title column
        if match.any():  # if there's at least one match
            row = self.dataframe[match].iloc[0]  # return the first match

            row = row.replace('\n', ' ', regex=True)  # replace newlines with spaces
            title = row['Title']  # extract the title
            ingredients = row['Ingredients'] # extract the ingredients
            instructions = row['Instructions']  # extract the instructions
            image_name = row['Image_Name'] # extract the image name
            recipe = Recipe(title, ingredients, instructions, image_name)  # create a Recipe object
            return recipe
        else:  # if no match is found
            return None

    def get_random_recipes(self, num_recipes):
        """Get specified number of random recipes"""

        recipes = []
        for i in range(num_recipes):
            recipe = self.get_random_recipe()
            recipes.append(recipe)

        return recipes


    #'Grilled Shrimp with Tamarind Sauce'



cookbook = Cookbook()
pantry = Pantry()





#########################################Gui Below This##################################################






import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QMessageBox, QListWidget,QTextEdit
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QPixmap
import glob
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QApplication, QWidget

from functools import partial
import re
from PyQt5 import QtWidgets

from PyQt5.QtGui import QColor, QPalette


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.recipe_list = []
        self.current_page = 0
        self.recipes_per_page = 99

        self.recipe_list = cookbook.get_random_recipes(1000)

        self.initUI()

    def initUI(self):
        try:
            self.setGeometry(500, 200, 1200, 1000)
            self.setWindowTitle('PyQt5 Button')

            # Set the color scheme
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(240, 240, 240))  # Gray background
            palette.setColor(QPalette.WindowText, QColor(50, 50, 50))  # Dark gray text
            palette.setColor(QPalette.Base, QColor(240, 240, 240))  # Gray background for widgets
            palette.setColor(QPalette.AlternateBase, QColor(220, 220, 220))  # Light gray background for alternating rows in lists
            palette.setColor(QPalette.Text, QColor(50, 50, 50))  # Dark gray text for widgets
            palette.setColor(QPalette.Button, QColor(240, 240, 240))  # Gray background for buttons
            palette.setColor(QPalette.ButtonText, QColor(50, 50, 50))  # Dark gray text for buttons
            self.setPalette(palette)

            # Remove the clean button and hello button
            # self.clean_button = QtWidgets.QPushButton('Clean', self)
            # self.clean_button.move(200, 70)
            # self.clean_button.clicked.connect(self.clean_frame)

            #self.button = QtWidgets.QPushButton('Hello', self)
            #self.button.move(100, 70)
            #self.button.clicked.connect(self.print_hello)



            self.entry_box = QtWidgets.QLineEdit(self)
            self.entry_box.move(300, 70)

            self.new_button = QtWidgets.QPushButton('New', self)
            self.new_button.move(400, 70)
            self.new_button.clicked.connect(self.print_new)

            self.option_menu = QtWidgets.QComboBox(self)
            self.option_menu.move(500, 70)
            self.option_menu.addItems(["Saved Recipes", "Browse Recipes"])
            self.option_menu.currentIndexChanged.connect(self.option_changed)

            self.scroll_area = QtWidgets.QScrollArea(self)
            self.scroll_area.setGeometry(0, 100, 300, 150)
            self.scroll_area.setWidgetResizable(True)

            self.frame = QtWidgets.QFrame()
            self.frame.setLayout(QtWidgets.QVBoxLayout())
            self.scroll_area.setWidget(self.frame)

            self.show()

            # Call print_hello here
            self.print_hello()

        except Exception as e:
            print("Error has occured:",e)

    def create_prev_next_buttons(self):
        if self.frame.layout() == None:
            self.frame.setLayout(QtWidgets.QHBoxLayout())
        else:
            self.frame.layout().addWidget(QtWidgets.QPushButton("Previous", self, clicked=self.prev_button_clicked))
            self.frame.layout().addWidget(QtWidgets.QPushButton("Next", self, clicked=self.next_button_clicked))

        self.frame.layout().addStretch(1)

    def prev_button_clicked(self):
        # Decrement the current page number if it is greater than 0
        if self.current_page > 0:
            self.current_page -= 1
        # Print "Hello" to the console
        self.print_hello()

    def next_button_clicked(self):
        # Increment the current page number
        self.current_page += 1
        # Print "Hello" to the console
        self.print_hello()



    def option_changed(self, index):
        if index == 0:
            try:
                self.load_saved_recipes()
                self.print_hello()
            except Exception as e:
                print("Error loading saved recipes:", e)
        elif index == 1:
            try:
                self.recipe_list = cookbook.get_random_recipes(500)
                self.print_hello()
            except Exception as e:
                print("Error getting random recipes:", e)

    def print_new(self):
        try:
            self.current_page = 0
            results = cookbook.search_recipes(self.entry_box.text())
            recipe_objects = []
            for recipe_name in results:
                recipe_objects.append(cookbook.fetch_specific_recipe(recipe_name))

            self.recipe_list = recipe_objects

            self.clean_frame()
            print(self.recipe_list)
            self.print_hello()

        except Exception as e:
            print(e)


    def print_hello(self):

        try:
            self.clean_frame()
            #directory = QFileDialog.getExistingDirectory(self, "Select Directory")
            if True == True:
                images, buttons = self.create_recipe_buttons_with_image_paths()

                if images is None:
                    self.current_page = 0
                    self.print_hello()
                    return

                if images:
                    # Create a grid layout to display the images
                    grid = QGridLayout()
                    self.frame.layout().addLayout(grid)

                    # Create a vertical layout for each image and button pair
                    for i, (image, button) in enumerate(zip(images, buttons)):
                        vbox = QVBoxLayout()

                        # Add the image to the vertical layout
                        label = QLabel(self)
                        label.setPixmap(QPixmap(image))
                        vbox.addWidget(label, alignment=Qt.AlignCenter)

                        # Add the button to the vertical layout
                        vbox.addWidget(button, alignment=Qt.AlignCenter)

                        # Add the vertical layout to the grid layout
                        grid.addLayout(vbox, i // 3, 2 * (i % 3))
                    self.create_prev_next_buttons()
                else:
                    print("No images found.")
            else:
                print("No directory selected.")
        except Exception as e:
            print("An error occurred:", e)



    def create_recipe_buttons_with_image_paths(self):
        buttons = []
        image_paths = []

        # Create a new variable to hold the filtered recipe list
        filtered_recipes = self.recipe_list[self.current_page*self.recipes_per_page:(self.current_page+1)*self.recipes_per_page]

        # Check if there are any recipes in the filtered list
        if len(filtered_recipes) == 0:
            return None, None
        else:
            try:
                for recipe in filtered_recipes:
                    # Create a new button for the recipe
                    button = QPushButton(recipe.title, self)

                    # Connect the button's clicked signal to a lambda function that prints the text of the button
                    button.clicked.connect(partial(self.start_recipe_generator, recipe))

                    # Append the button to the buttons list
                    buttons.append(button)

                    # Construct the image path for the recipe
                    image_path = os.path.join("archive", "Food Images", recipe.image_name + ".jpg")

                    # Append the image path to the image_paths list
                    image_paths.append(image_path)

            except Exception as e:
                print("An error occurred: {}".format(e))

        # Return both the buttons list and the image_paths list
        return image_paths, buttons







    def load_saved_recipes(self):
        """
        Loads saved recipes from a JSON file into the recipes list.

        Opens the specified JSON file in read mode, loads the data into a dictionary,
        and then iterates over the recipes in the dictionary. For each recipe, creates
        a new Recipe object from the dictionary values and adds it to the recipes list.
        """

        filepath = r"archive\Sample.json"  # path to the JSON file

        # Open the file in read mode
        with open(filepath, 'r') as f:
            # Load the JSON data into a dictionary
            recipe_dict = json.load(f)

        # Clear the existing recipes list
        self.recipe_list = []

        # Iterate over the recipes in the dictionary
        for title, recipe_info in recipe_dict.items():
            # Create a new Recipe object from the dictionary values
            recipe = Recipe(title, recipe_info['ingredients'], recipe_info['instructions'], recipe_info['image_name'])

            # Add the new recipe to the list
            self.recipe_list.append(recipe)





    def clean_frame(self):
        # Delete all widgets in the frame except the scroll area
        for widget in self.frame.findChildren(QWidget):
            if widget != self.scroll_area:
                widget.deleteLater()
        self.frame.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scroll_area.setGeometry(0, 100, self.width(), self.height() - 100)




    def start_recipe_generator(self,recipe):
        trimmed_string = recipe.ingredients[1:-1]
        recipe_list = re.split(",(?=(?:[^'']*'[^'']*')*[^'']*$)", trimmed_string)
        try:
            self.new_window = RecipeViewer()
            self.new_window.recipe = recipe
            self.new_window.populateIngredients()
            self.new_window.populateInstructions()
            #self.new_window.printImageName()
            self.new_window.setImage()
            self.new_window.is_recipe_in_pantry()
            self.new_window.show()
        except Exception as e:
            print(e)




###################### Recipe Viewer Class ###################################################################

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QHBoxLayout

class RecipeViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.recipe = None
        self.pantry = Pantry()

    def initUI(self):
        self.setWindowTitle("Recipe Viewer")
        self.resize(800, 600)

        # Set the color scheme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))  # Gray background
        palette.setColor(QPalette.WindowText, QColor(50, 50, 50))  # Dark gray text
        palette.setColor(QPalette.Base, QColor(240, 240, 240))  # Gray background for widgets
        palette.setColor(QPalette.AlternateBase, QColor(220, 220, 220))  # Light gray background for alternating rows in lists
        palette.setColor(QPalette.Text, QColor(50, 50, 50))  # Dark gray text for widgets
        palette.setColor(QPalette.Button, QColor(240, 240, 240))  # Gray background for buttons
        palette.setColor(QPalette.ButtonText, QColor(50, 50, 50))  # Dark gray text for buttons
        self.setPalette(palette)

        self.listbox = QListWidget(self)
        self.listbox.setMinimumHeight(300)

        # Add image label
        self.image_label = QLabel(self)
        self.image_label.setFixedHeight(self.listbox.height())
        self.image_label.setMaximumWidth(self.listbox.width())

        # Horizontal layout for listbox and image
        hbox = QHBoxLayout()
        hbox.addWidget(self.listbox)
        hbox.addWidget(self.image_label)

        self.textbox = QTextEdit(self)
        self.textbox.setMinimumHeight(300)
        self.textbox.setMinimumWidth(600)

        # Add Save Recipe button
        #self.save_button = QPushButton("Save Recipe", self)
        #self.save_button.setFixedHeight(50)
        #self.save_button.clicked.connect(self.saveRecipe)

        # Use stretch factor to make button take up half the width
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(hbox)
        self.vbox.addWidget(self.textbox)
        #self.vbox.addWidget(self.save_button, stretch=1)

        self.setLayout(self.vbox)
        self.clearAll()

    def saveRecipe(self):
        """
        Save a recipe to the pantry and write the pantry's recipe dictionary to a JSON file.
        Also updates the main gui to reflect any changes made in saved recipes.
        """
        try:
            self.pantry.add_recipe(self.recipe)              # Add Recipe to the pantry

            self.pantry.write_recipe_dict_to_json()          # Write the pantry's recipe dictionary to a JSON file

            option_text = window.option_menu.currentText()   # Get the current text of the option menu from main window

            # If the current text is "Saved Recipes", Refresh the Gui. this is so the newly saved recipe is visibile.
            if option_text == "Saved Recipes":
                window.load_saved_recipes()    #reload recipes in main gui
                window.print_hello()           #reload the widgets in main gui


            self.save_button.deleteLater() # Delete the save button

            self.is_recipe_in_pantry() #Changes the save button to un-save button

        except Exception as e:
            print(e)


    def is_recipe_in_pantry(self):
        """
        Checks if the current recipe is already saved in the pantry.
        If the recipe is in the pantry, it adds a "Un-Save Recipe" button to the GUI and returns True.
        If the recipe is not in the pantry, it adds a "Save Recipe" button to the GUI and returns False.
        Returns:
            bool: True if the recipe is in the pantry, False otherwise.
        """
        # Check if the recipe is already in the pantry
        if self.recipe.title in [recipe.title for recipe in self.pantry.recipes]:

            # If it is, add a "Un-Save Recipe" button to the GUI
            self.unsave_button = QPushButton("Un-Save Recipe", self)
            self.unsave_button.setFixedHeight(50)
            self.unsave_button.clicked.connect(self.remove_recipe_from_saved)
            self.vbox.addWidget(self.unsave_button, stretch=1)

            # Return True to indicate that the recipe is already saved
            return True

        else:
            # If it's not in the pantry, add a "Save Recipe" button to the GUI
            self.save_button = QPushButton("Save Recipe", self)
            self.save_button.setFixedHeight(50)
            self.save_button.clicked.connect(self.saveRecipe)
            self.vbox.addWidget(self.save_button, stretch=1)

            # Return False to indicate that the recipe is not yet saved
            return False



    def remove_recipe_from_saved(self):
        """

        """
        try:
            #Removes the recipe from the pantry recipe list and then from the json where the recpies are saved.
            self.pantry.remove_recipe(self.recipe.title)
            self.pantry.remove_recipe_from_json(self.recipe.title)

            #Update the Main gui. Reloads the recipe list and then the widgets
            window.load_saved_recipes()
            window.print_hello()

            #Remove the un-save button
            self.unsave_button.deleteLater()

            #Change to the save button
            self.is_recipe_in_pantry()

        except Exception as e:
            print("Error removing recipe from pantry:", e)

    def clearAll(self):
        """
        Simple Function that insures all the gui is clear
        """
        self.listbox.clear()
        self.textbox.clear()
        self.image_label.clear()

    def populateIngredients(self):
        self.listbox.addItem("Ingredients:")
        trimmed_string = self.recipe.ingredients[1:-1]
        recipe_list = re.split(",(?=(?:[^'']*'[^'']*')*[^'']*$)", trimmed_string)
        for ingredient in recipe_list:
            self.listbox.addItem(f"{ingredient}")

    def populateInstructions(self):
        self.textbox.setText('')
        self.textbox.append(self.recipe.instructions)

    def setImage(self):
        # Construct the image path for the recipe
        image_path = os.path.join("archive", "Food Images", self.recipe.image_name + ".jpg")
        self.image_label.setPixmap(QPixmap(image_path))
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(self.image_label.sizeHint())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())