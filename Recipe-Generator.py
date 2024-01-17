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

###########################GUI Below This#########################################

import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image
import tkinter as tk
from tkinter import messagebox
import re
from CTkListbox import *





class recipeGUI:
    def __init__(self, window):
        #Create Window

        window.title('Recipe Generator')
        window.geometry('1400x700')
        #Create a fullscreen window
        self.init_ui()


    def init_ui(self):

        ############Adding ListBox for ingredients###################

        # Create a new Listbox widget
        self.listbox = CTkListbox(window, width=780, height= 50)

        # Add the Listbox to the window
        self.listbox.grid(row=2, column=0)

        ############Title#############
        self.label1 = ctk.CTkLabel(window, text="Recipe Generator:", font=('Times New Roman',30))
        self.label1.grid(row=1, column=0)

        ########### Buttons ###########
        self.segemented_button = ctk.CTkSegmentedButton(window,border_width=20,corner_radius=10,unselected_hover_color="gray", values=["Previous Recipe","New Recipe", "Save Recipe", "Remove Recipe"],command=self.segmented_button_callback)
        #self.segemented_button.set("Value 1")
        self.segemented_button.grid(row=4, column=0)

        ####### Creates Text box for the recipe #########
        self.textbox = ctk.CTkTextbox(window, width=800, height= 280)
        self.textbox.delete('0.0', "end")
        self.textbox.insert('0.0', "Welcome to the Recipe Generator!")
        self.textbox.configure(state="disabled")
        self.textbox.grid(row=3, column=0)


        ######## creates the dropdown menu object ###########
        self.optionmenu = ctk.CTkOptionMenu(window, values=[food.title for food in pantry.recipes],command=self.optionmenu_callback)
        self.optionmenu.set("Saved Recipes")
        self.optionmenu.grid(row = 4, column = 1)


        ######## Combobox creation ########
        n = ctk.StringVar()
        self.menulist = ctk.CTkComboBox(window, width = 750, variable = "n",values=["Search Recipes Here"],command=self.combobox_callback)

        self.menulist.grid(column = 0, row = 0)


        ######## Search button #######
        self.search_button = ctk.CTkButton(window, text="Search", command=self.search_recipe)
        self.search_button.grid(row = 0, column = 1)


        ######## Initializes the Image #########
        self.your_image = ctk.CTkImage(light_image=Image.open(os.path.join(r"archive\first_image.jpg")), size=(500 , 500))
        self.label = ctk.CTkLabel(master=window, image=self.your_image, text='')
        self.label.grid(column=1, row=2, rowspan=2)

        # create an instance of the ImageDisplayer class
        #image_displayer = ImageDisplayer()

        #Create a button to open the random recipe viewer
        self.saved_recipes_button = ctk.CTkButton(window, text="Saved Recipes",command=lambda: ImageDisplayer().mainloop())
        self.saved_recipes_button.grid(column=1, row=6)

        # create a button to open the saved recipe viewer
        self.browse_recipe_button = ctk.CTkButton(window, text="Browse Recipes", command=lambda: ImageDisplayer(cookbook.get_random_recipes(500)).mainloop())
        self.browse_recipe_button.grid(column=1, row=7)





    #####Multi-Button Callback ########
    def segmented_button_callback(self,value):

        if value == "New Recipe":
            self.new_recipe_button()
            self.segemented_button.set("Value 1")

        elif value == "Previous Recipe":
            self.previous_recipe()
            self.segemented_button.set("Value 1")

        elif value == "Save Recipe":
            self.save_current_recipe()
            self.segemented_button.set("Value 1")

        elif value == "Remove Recipe":
            self.delete_recipe_from_json()
            self.segemented_button.set("Value 1")





    #updates image
    def get_image(self,image_name):
        Image_path = r"archive\Food Images\\" + image_name + ".jpg"
        self.your_image.configure(light_image=Image.open(os.path.join(Image_path)))

    #Updates the text box
    def update_text(self,food_object):
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', "end")
        if isinstance(food_object, str):  # Check if food_object is a string
            return  # If it's a string, don't try to access ingredients
        self.textbox.insert('0.0', "Instructions:" + '\n\n' + food_object.instructions)
        self.update_listbox(food_object.ingredients)
        self.get_image(str(food_object.image_name))
        self.textbox.configure(state="disabled")
        self.label1.configure(text=str(food_object.title))


    #this is the button that generates a new recipe
    def new_recipe_button(self):
        temp = cookbook.get_random_recipe()
        self.update_text(temp)
        pantry.add_previous_recipe(temp)
        pantry.previous_recipe_placeholder = 2


    #This is the button to return to the previous Recipe
    def previous_recipe(self):


        if pantry.previous_recipe_placeholder < 11 and pantry.previous_recipe[pantry.previous_recipe_placeholder] != '':
            self.update_text(pantry.previous_recipe[pantry.previous_recipe_placeholder])
            pantry.previous_recipe_placeholder += 1
        else:
            self.update_text(pantry.previous_recipe[1])
            pantry.previous_recipe_placeholder = 2



    #This button saves the current recipe and updates the dropdown menu
    def save_current_recipe(self):

        pantry_recipe_titles = [item.title for item in pantry.recipes]

        if pantry.previous_recipe_placeholder == 2 and pantry.previous_recipe[1].title not in pantry_recipe_titles:

            pantry.add_recipe(pantry.previous_recipe[1])
            print(f"Recipe saved: {pantry.previous_recipe[1].title}")
            pantry.write_recipe_dict_to_json()

        elif pantry.previous_recipe_placeholder == 2 and pantry.previous_recipe[1].title in pantry_recipe_titles:
            print(f"You already have this recipe saved: {pantry.previous_recipe[1].title}")

        elif pantry.previous_recipe_placeholder != 2 and pantry.previous_recipe[pantry.previous_recipe_placeholder - 1].title in pantry_recipe_titles:
            print(f"You already have this recipe saved: {pantry.previous_recipe[pantry.previous_recipe_placeholder - 1].title}")

        else:
            pantry.add_recipe(pantry.previous_recipe[pantry.previous_recipe_placeholder - 1])
            print(f"Recipe saved: {pantry.previous_recipe[pantry.previous_recipe_placeholder - 1].title}")
            pantry.write_recipe_dict_to_json()


        self.optionmenu.configure(values=[food.title for food in pantry.recipes])




    #Deletes the selected recipe.
    def delete_recipe_from_json(self):

        current_recipe = pantry.previous_recipe[pantry.previous_recipe_placeholder-1].title


        if current_recipe in [recipe.title for recipe in pantry.recipes]:
            pantry.remove_recipe(current_recipe)
            self.optionmenu.configure(values=[food.title for food in pantry.recipes])
            pantry.write_recipe_dict_to_json()
            print(f"Recipe removed: {current_recipe}")
        else:
            print(f"Recipe has not been saved: {current_recipe}")



    #sets recipe to selected saved recipe
    def optionmenu_callback(self,choice):
        for recipe in pantry.recipes:
            if recipe.title == choice:
                delete_me = recipe
                self.update_text(recipe)
                pantry.add_previous_recipe(recipe)
                pantry.previous_recipe_placeholder = 2


    def combobox_callback(self,search_term):
        # Updates the text box based on the search item clicked
        search_term = self.menulist.get()
        if search_term != None and search_term != "Search Recipes Here":
            recipe = cookbook.fetch_specific_recipe(search_term)
            print(recipe)
            if recipe is not None:
                self.update_text(recipe)
                pantry.add_previous_recipe(recipe)
                pantry.previous_recipe_placeholder = 2
            else:
                messagebox.showinfo("No recipe found", f"No recipe found with title '{search_term}'")
        else:
            pass


    def search_recipe(self):
        #Gets the search parameter and searches for the recipe.
        search_term = self.menulist.get()
        results = cookbook.search_recipes(search_term)

        #Set Menu entrys to search results
        self.menulist.configure(values=results)

        # If no results, display message
        if not results:
            if search_term:
                messagebox.showinfo("No recipe found", f"No recipe found with title '{search_term}'")
            else:
                messagebox.showinfo("Error", "Please enter a search term")

    def update_listbox(self, recipe):
        if self.listbox.size() > 0:
            self.listbox.delete(0, ctk.END)
        self.listbox.insert(ctk.END, "Ingredients:")
        trimmed_string = recipe[1:-1]
        recipe_list = trimmed_string.split(",")
        for item in recipe_list:
            self.listbox.insert(ctk.END, item)

import PIL.Image as Image
import PIL.ImageTk as ImageTk


class ImageDisplayer:
    """
    This class creates a GUI window that displays images and buttons for recipes in a grid pattern
    for easier browsing of recipes.The selected recipe will be displayed in the parent window recipeGui.


    Key Methods:
        - __init__: Initializes the ImageDisplayer class.
        - on_mouse_wheel: Handles mouse wheel events.
        - button_clicked: Populates the GUI with images and buttons for each recipe.
        - load_saved_recipes: Loads saved recipes from a JSON file.
        - check_window_size_and_call_button_clicked: Checks if the window size has changed and updates the GUI accordingly.
        - button_clicked2: Displays the chosen recipe when a button is clicked.
        - mainloop: Starts the GUI event loop.
    """
    def __init__(self,recipes=None):
        """
            Initializes the ImageDisplayer class.

            Description:
                This method creates the Toplevel GUI window and sets up its components, including a frame, canvas, and scrollbar. It also binds events to the mouse wheel and configure events.

            Key Actions:
                - Creates the Toplevel Tkinter window with a title, geometry, and resizable properties.
                - Creates a frame, canvas, and scrollbar inside the main window.
                - Configures the canvas to have a scrollable frame inside.
                - Binds the mouse wheel event to the on_mouse_wheel method.
                - Binds the configure event to the check_window_size_and_call_button_clicked method (commented out).
                - Initializes lists for images, recipe buttons, and recipes.
                - Calls the load_saved_recipes method to poplulate self.recipes
                - Calls the button_clicked method to populate the scrollable frame.

            Notes:
                - The gui is set to only allow changing the size vertically. Increasing size horizontally made the gui look awful.
                - The method uses the Tkinter library. I may switch this all to customTkinter in the future to match the parent gui.
        """
        self.root = tk.Toplevel()
        self.master = self.root
        self.master.title("Three Frames")
        self.master.geometry("1210x900")
        self.master.resizable(False, True)

        # Create a frame
        self.frame = tk.Frame(self.master)


        # Create a canvas inside the frame
        self.canvas = tk.Canvas(self.frame)


        # Create a scrollbar inside the frame
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)

        # Create a scrollable frame inside the canvas
        self.scrollable_frame = tk.Frame(self.canvas)

        # Configure the scrollable frame to update the canvas scroll region
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the frame, canvas, and scrollbar
        self.frame.pack(fill="both", expand=True)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind the mouse wheel event to the on_mouse_wheel method
        self.master.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Create a list of images
        self.images = []
        self.recipe_buttons = []
        self.recipes = []

        if recipes:
            self.recipes = recipes
        else:
            self.load_saved_recipes()

        # Call the button_clicked function
        self.button_clicked()


        # Initialize the variables to store the last known window width and height
        self.last_width = 0
        self.last_height = 0

        # Bind the configure event to the check_window_size_and_call_button_clicked method
        #self.master.bind('<Configure>', self.check_window_size_and_call_button_clicked)



    def on_mouse_wheel(self, event):
        """Manages the Scrolling of the scrollable frame"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def button_clicked(self):
        """
        This function populates the scrollable frame with images and buttons for each recipe.
        It uses a grid layout to arrange the images and buttons in a 3xN configuration.

        The function iterates through the list of recipes and for each recipe:
        - Opens the image file using Pillow
        - Resizes the image to a fixed size (400x400)
        - Converts the resized image to a PhotoImage for Tkinter
        - Creates a label and button for each image and adds them to the frame
        - Appends the image and button to their respective lists

        The function also updates the scroll region of the canvas to include all the images and buttons.
        """
        # Set the image size to a fixed size
        image_width = 400
        image_height = 400

        # Initialize row and column variables to track the position of the images and buttons
        row = 0
        column = 0

        # Iterate through the list of recipes
        for recipe in self.recipes:
            # Get the image name and path
            image_name = recipe.image_name
            Image_path = os.path.join("archive", "Food Images", image_name + ".jpg")

            # Open the image and resize it using Pillow
            image = Image.open(Image_path)
            image = image.resize((image_width, image_height), Image.BICUBIC)

            # Convert the resized image to a PhotoImage for Tkinter
            image_tk = ImageTk.PhotoImage(image)

            # Create a label and button for each image
            label = tk.Label(self.scrollable_frame, image=image_tk)
            label.grid(row=row, column=column, sticky="nsew")

            recipe_button = tk.Button(self.scrollable_frame, text=recipe.title, height=2)
            recipe_button.config(command=lambda recipe_button=recipe_button: self.button_clicked2(recipe_button))
            recipe_button.grid(row=row+1, column=column, sticky="nsew")

            #When the column variable exceeds 3 (i.e., the maximum number of columns), the row variable is incremented by 2 to create a new row,
            # and the column variable is reset to 0. This ensures that the images and buttons are properly aligned in the grid layout.
            column += 1
            if column >= 3:
                row += 2
                column = 0

            # Append the image and button to their respective lists
            #This is necessary to prevent tkinter garbage collecting the widgets
            self.images.append(image_tk)
            self.recipe_buttons.append(recipe_button)

        # Update the scroll region to include all the images and buttons
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))




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
        self.recipes = []

        # Iterate over the recipes in the dictionary
        for title, recipe_info in recipe_dict.items():
            # Create a new Recipe object from the dictionary values
            recipe = Recipe(title, recipe_info['ingredients'], recipe_info['instructions'], recipe_info['image_name'])

            # Add the new recipe to the list
            self.recipes.append(recipe)

    def check_window_size_and_call_button_clicked(self, event):
        """
        Checks if the window size has changed and calls the button_clicked function if necessary.

        Gets the current window width and height, and compares them to the last known values.
        If the width or height has changed, updates the last known values and calls the button_clicked function.

        :param event: the event that triggered the function (not used in this implementation)
        """
        # Get the current window width and height
        current_width = self.master.winfo_width()
        current_height = self.master.winfo_height()

        # Check if the window width or height has changed since the last time the function ran
        if self.last_width != current_width or self.last_height != current_height:
            # Update the variables to reflect the changes
            self.last_width = current_width
            self.last_height = current_height

            # Call the button_clicked function
            self.button_clicked()

    def button_clicked2(self, recipe_button):
        """
        Gets the name of the button, And finds the matching recipe in self.recipes,
        It then sends the recipe to the update_text function of the recipeGui to display the chosen recipe
        Args:
            recipe_button: The button object that was clicked
        """
        for recipe in self.recipes:
            if recipe.title == recipe_button.cget("text"):
                # Assuming 'window' is an instance of the other class
                gui.update_text(recipe)
                break

    def mainloop(self):
        """Starts the gui's main loop"""
        self.master.mainloop()

window = ctk.CTk()
gui = recipeGUI(window)
#run
window.mainloop()
