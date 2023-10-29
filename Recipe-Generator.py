import pandas as pd
pd.set_option('display.max_colwidth', None)

import json
import os


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
        with open(filepath, 'r') as f:  # open the file in read mode
            temp_dict = json.load(f)  # load the existing JSON data into a temp dictionary

        # Append new values to the temporary dictionary
        temp_dict.update(self.to_dict())  # update the temp dictionary with the new values from the recipe

        with open(filepath, 'w') as f:  # open the file in write mode
            json.dump(temp_dict, f, indent=4)  # write the updated temp dictionary to the file, with indentation


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
            # Create a temporary dictionary with the desired keys and values
            temp_dict = {
                'title': row['Title'],
                'ingredients': row['Ingredients'],
                'instructions': row['Instructions'],
                'image_name': row['Image_Name']
            }
            print(temp_dict)  # print the dictionary to console
            return row
        else:  # if no match is found
            return None


    #'Grilled Shrimp with Tamarind Sauce'



cookbook = Cookbook()
pantry = Pantry()

###########################GUI Below This#########################################

import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image
import tkinter


#Create Window
window = ctk.CTk()
window.title('Recipe Generator')
window.geometry('1200x450')


#Creates Text box for the recipe
textbox = ctk.CTkTextbox(window, width=800, height= 300)
textbox.delete('0.0', "end")
textbox.configure(state="disabled")
textbox.grid(row=1, column =0)


#Updates the text box
def update_text(food_object):
    textbox.configure(state="normal")
    textbox.delete('0.0', "end")
    textbox.insert('0.0', str(food_object.title) + '\n\n' + str(food_object.ingredients) + '\n\n' + food_object.instructions)
    textbox.configure(state="disabled")


#this is the button that generates a new recipe
def new_recipe_button():
    temp = cookbook.get_random_recipe()
    update_text(temp)
    pantry.add_previous_recipe(temp)
    pantry.previous_recipe_placeholder = 2

button = ctk.CTkButton(window, text="New Recipe", command=new_recipe_button)
button.grid(row=0, column =0)



#This is the button to return to the previous Recipe
def previous_recipe():

    #Image_path = r"archive\Food Images\Food Images\\" + previous_food.image_name + ".jpg"
    #get_image()
    if pantry.previous_recipe_placeholder < 11 and pantry.previous_recipe[pantry.previous_recipe_placeholder] != '':
        update_text(pantry.previous_recipe[pantry.previous_recipe_placeholder])
        pantry.previous_recipe_placeholder += 1
    else:
        update_text(pantry.previous_recipe[1])
        pantry.previous_recipe_placeholder = 2





button1 = ctk.CTkButton(window, text="Previous Recipe", command=previous_recipe)
button1.grid(row=2, column =0)


#sets recipe to selected saved recipe
def optionmenu_callback(choice):
    for recipe in pantry.recipes:
        if recipe.title == choice:
            delete_me = recipe
            update_text(recipe)
            Image_path = r"archive\Food Images\Food Images\\" + recipe.image_name + ".jpg"
            pantry.add_previous_recipe(recipe)
            pantry.previous_recipe_placeholder = 2
            #get_image()




#creates the dropdown menu object
optionmenu = ctk.CTkOptionMenu(window, values=[food.title for food in pantry.recipes],command=optionmenu_callback)
optionmenu.set("Saved Recipes")
optionmenu.grid(row = 3, column = 1)







#run
window.mainloop()
