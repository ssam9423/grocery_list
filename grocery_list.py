"""Grocery List Tracker - Created by Samantha Song - Started 2025.02.06"""
# Create a simple grocery list tracker
# Show 2 Lists - Fridge, To Buy & Past
# Add options: Sort, Add, Delete
#   Sorting Options: Alphabetical, by low, by item count, item type
# When Selecting: Move
# To Buy List -> checkbox for shopping
# Change amount

import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np

FILE_NAME = 'groceries.csv'
PATH_TO_FILE = ''
grocery_list = pd.read_csv(FILE_NAME)
in_fridge, to_buy, past_items = [], [], []

# Functions
def move(full_list, move_to, food_name):
    """Update Booleans move_to in full_list & return full_list"""
    # Most useful for moving items between is_stocked, need_to_buy and into past_items
    if is_in_list(full_list, food_name):
        index = get_index(full_list, food_name)
        full_list.at[index, 'is_stocked'] = False
        full_list.at[index, 'need_to_buy'] = False
        if move_to in full_list.columns:
            full_list.at[index, move_to] = True
    return full_list

def sort_list(which_list, sort_criteria):
    """Sorts & returns specified list depending on the sort_criteria"""
    # Most useful for food, food_type, is_low, in_cart
    if sort_criteria in which_list.columns:
        which_list = which_list.sort_values(by=sort_criteria)
    if sort_criteria == 'is_low':
        which_list = which_list.iloc[::-1]
    return which_list

def get_index(which_list, food_name):
    """Returns index of food_name in which_list"""
    return which_list.loc[which_list['food'] == food_name].index[0]

def is_in_list(which_list, food_name):
    """Searches for food name and returns Boolean if in grocery_list"""
    return np.isin(food_name, which_list['food'].values)

def is_in_cart(which_list, food_name):
    """Searches for food name and returns Boolean if is_low"""
    return which_list.at[get_index(which_list, food_name), 'in_cart']

def get_food_name(item_string):
    """Returns food_name given item_string"""
    space_index = item_string.find('   ') + 3
    return item_string[space_index:]

def add_item(full_list, new_food, new_type, stocked=False,
             low=False, buy=True, amount=1, cart=False):
    """Adds new food to grocery_list db and returns grocery_list"""
    # Check if new_food is already in full_list
    if ~is_in_list(full_list, new_food):
        new_item = [new_food, new_type, stocked, low, buy, amount, cart]
        full_list.loc[len(full_list)] = new_item
    return full_list

def delete_item(full_list, old_food):
    """Deletes old food from grocery_list db and returns grocery_list"""
    # Check if old_food is in full_list
    if is_in_list(full_list, old_food):
        index = get_index(full_list, old_food)
        full_list.drop((index), inplace=True)
    return full_list

# def switch_boolean(full_list, curr_food, column):
#     """Updates column to not column for curr_food & returns full_list"""
#     # Mostly useful for is_low and in_cart
#     if (column in full_list.columns) & is_in_list(full_list, curr_food):
#         index = get_index(full_list, curr_food)
#         full_list.at[index, column] = ~full_list.at[index, column]
#     return full_list

def update_amount(full_list, curr_food, new_amount):
    """Updates curr_food amount to new_amount in full_list & returns full_list"""
    if is_in_list(full_list, curr_food):
        index = get_index(full_list, curr_food)
        full_list.at[index, 'amount'] = new_amount
    return full_list

def update_in_cart(full_list, curr_food):
    """Updates in_cart to not in_cart & returns full_list"""
    if is_in_list(full_list, curr_food):
        index = get_index(full_list, curr_food)
        full_list.at[index, 'in_cart'] = ~is_in_cart(full_list, curr_food)
    return full_list

def update_lists(full_list):
    """Updates in_fridge, to_buy, and past_items and returns (fridge, buy, past)"""
    fridge = full_list.loc[full_list['is_stocked']]
    buy = full_list.loc[full_list['need_to_buy']]
    past = full_list.loc[~full_list['is_stocked'] &
                         ~full_list['need_to_buy']]
    return (fridge, buy, past)

def save_file(full_list):
    """Saves current grocery_list to csv"""
    full_list.to_csv(FILE_NAME, index=False)
    return 0

# Tkinter Functions Functions
def create_scroll_list(root, which_list):
    """Create a Scrollbar and Listbox"""
    frame = tk.Frame(root)
    list_scroll = tk.Scrollbar(frame)
    list_scroll.pack(side=tk.RIGHT)
    # Listboxes
    list_box = tk.Listbox(frame, yscrollcommand=list_scroll.set, selectmode='multiple')
    update_scroll_list(list_box, which_list)
    list_box.pack(side=tk.LEFT)
    list_scroll.config(command=list_box.yview)
    return frame, list_box

def update_scroll_list(which_listbox, which_list):
    """Update Listbox"""
    which_listbox.delete(0, tk.END)
    for index in range(which_list.shape[0]):
        food = which_list.iloc[index].loc['food']
        amount = which_list.iloc[index].loc['amount']
        item_count = str(amount) + "   " + str(food)
        which_listbox.insert(tk.END, item_count)
        # Highlights item as light grey if in_cart
        if is_in_cart(which_list, food):
            which_listbox.itemconfig(index, bg='#D3D3D3')
    return 0

# Main Function
def main():
    """Create the Main Window"""
    # Functions Connecting Buttons to Action Functions - Buttons don't pass values
    def add():
        """Function to add food given name and type"""
        global grocery_list
        new_food_val = new_food.get()
        new_type_val = new_type.get()
        if not new_food_val == '':
            grocery_list = add_item(grocery_list, new_food_val, new_type_val)
        update_all()

    def get_selected_items():
        """returns list selected of item names"""
        consolidated_list = []
        for _, listbox in enumerate([fridge_lb, buy_lb, past_lb]):
            indexes = listbox.curselection()
            items = [listbox.get(index) for index in indexes]
            consolidated_list.extend(items)
        return consolidated_list

    def delete():
        """Function to delete a food"""
        global grocery_list
        del_list = get_selected_items()
        for _, item in enumerate(del_list):
            food_name = get_food_name(item)
            grocery_list = delete_item(grocery_list, food_name)
        update_all()

    def change_amount():
        """Changes amount of selected items if amount is a valid integer"""
        global grocery_list
        change_list = get_selected_items()
        try:
            amount = int(new_amount.get())
            for _, item in enumerate(change_list):
                food_name = get_food_name(item)
                grocery_list = update_amount(grocery_list, food_name, amount)
            update_all()
        except ValueError:
            return 0

    def move_to(where):
        """Moves selected items to specified list"""
        global grocery_list
        move_fridge_list = get_selected_items()
        for _, item in enumerate(move_fridge_list):
            food_name = get_food_name(item)
            grocery_list = move(grocery_list, where, food_name)
        update_all()

    def move_to_fridge():
        """Moves selected items to the fridge"""
        move_to('is_stocked')

    def move_to_buy():
        """Moves selected items to the to buy list"""
        move_to('need_to_buy')

    def move_to_past():
        """Moves selected items to the past items list"""
        move_to('past_items')

    def in_cart():
        """"Function to change items to in_cart or not in_cart"""
        global grocery_list
        cart_ind = buy_lb.curselection()
        cart_list = [buy_lb.get(index) for index in cart_ind]
        for _, item in enumerate(cart_list):
            food_name = get_food_name(item)
            grocery_list = update_in_cart(grocery_list, food_name)
        update_all()
        sort()

    def sort():
        """Function to sort items in lists"""
        global grocery_list
        sort_by_val = sort_by.get()
        grocery_list = sort_list(grocery_list, sort_by_val)
        update_all()

    def update_all():
        """Function to update all Scroll Lists and dbs"""
        global in_fridge, to_buy, past_items
        in_fridge, to_buy, past_items = update_lists(grocery_list)
        update_scroll_list(fridge_lb, in_fridge)
        update_scroll_list(buy_lb, to_buy)
        update_scroll_list(past_lb, past_items)

    def save():
        """Save Lists to csv file"""
        save_file(grocery_list)

    # Initiates in_fridge, to_buy, and past_items lists
    global in_fridge, to_buy, past_items
    in_fridge, to_buy, past_items = update_lists(grocery_list)
    # Intialize Screen
    root = tk.Tk()
    root.title("Grocery List")
    screen_w = 800
    screen_h = 550
    button_w = 10
    button_h = 1
    padding = int(screen_w / 100)
    screen_size = str(screen_w) + 'x' + str(screen_h)
    root.geometry(screen_size)

    # Title - Frame, Label
    title_frame = tk.Frame(root)
    tk.Label(title_frame, text='Grocery List').pack()
    title_frame.pack()

    # Sort - Frame, Label, Combobox
    sort_frame = tk.Frame(root)
    sort_frame.pack(side=tk.TOP)
    tk.Label(sort_frame, text='Sort By: ').pack(side=tk.LEFT)
    sort_by = ttk.Combobox(sort_frame, values=['food', 'food_type', 'amount', 'is_low', 'in_cart'])
    sort_by.set('in_cart')
    sort_by.pack(side=tk.LEFT)

    # Scrollable Lists - Parent & Child Frames, Labels, Scroll Listboxes
    # Parent Frame
    list_frame = tk.Frame(root)
    list_frame.pack()
    # Children Frames for each List
    fridge_frame = tk.Frame(list_frame)
    buy_frame = tk.Frame(list_frame)
    past_frame = tk.Frame(list_frame)
    fridge_frame.pack(side=tk.LEFT, padx=padding, pady=padding)
    buy_frame.pack(side=tk.LEFT, padx=padding, pady=padding)
    past_frame.pack(side=tk.LEFT, padx=padding, pady=padding)
    # In Fridge Label & Scroll Listbox
    fridge_label = tk.Label(fridge_frame, text="Fridge")
    fridge_label.pack(side=tk.TOP)
    fridge_frame, fridge_lb = create_scroll_list(fridge_frame, in_fridge)
    fridge_frame.pack(side=tk.TOP)
    # To Buy Label & Scroll Listbox
    buy_label = tk.Label(buy_frame, text="To Buy")
    buy_label.pack(side=tk.TOP)
    buy_frame, buy_lb = create_scroll_list(buy_frame, to_buy)
    buy_frame.pack(side=tk.TOP)
    # Past Items Label and Scroll Listbox
    past_label = tk.Label(past_frame, text="Past Items")
    past_label.pack(side=tk.TOP)
    past_frame, past_lb = create_scroll_list(past_frame, past_items)
    past_frame.pack(side=tk.TOP)

    # Add Items - Frames, Entry & Labels
    add_frame = tk.Frame(root, padx=padding, pady=padding)
    add_frame.pack()
    tk.Label(add_frame, text='Food Name: ').pack(side=tk.LEFT)
    new_food = tk.Entry(add_frame)
    new_food.pack(side=tk.LEFT, padx=padding)
    tk.Label(add_frame, text='Food Type: ').pack(side=tk.LEFT)
    new_type = tk.Entry(add_frame)
    new_type.pack(side=tk.LEFT, padx=padding)
    sort()

    # Change Amount - Frame, Entry & Label
    amount_frame = tk.Frame(root, padx=padding, pady=padding)
    amount_frame.pack()
    tk.Label(amount_frame, text='Change Amount to: ').pack(side=tk.LEFT)
    new_amount = tk.Entry(amount_frame)
    new_amount.pack(side=tk.LEFT)

    # Move Items - Frame & Label
    move_frame = tk.Frame(root, padx=padding, pady=padding)
    move_frame.pack()
    tk.Label(move_frame, text='Move Items to: ').pack(side=tk.LEFT)

    # In/Out Cart, Delete, Save Buttons Frame
    button2_frame =tk.Frame(root, padx=padding, pady=padding)
    button2_frame.pack()

    # Buttons
    sort_button = tk.Button(sort_frame, text="Sort",
                       width=button_w, height=button_h, command=sort)
    sort_button.pack(side=tk.LEFT, padx=padding)

    add_button = tk.Button(add_frame, text="Add",
                       width=button_w, height=button_h, command=add)
    add_button.pack(side=tk.LEFT, padx=padding)

    amount_button = tk.Button(amount_frame, text='Change',
                              width=button_w, height=button_h, command=change_amount)
    amount_button.pack(side=tk.LEFT, padx=padding)

    fridge_button = tk.Button(move_frame, text="Fridge",
                       width=button_w, height=button_h, command=move_to_fridge)
    fridge_button.pack(side=tk.LEFT, padx=padding)
    buy_button = tk.Button(move_frame, text="To Buy",
                       width=button_w, height=button_h, command=move_to_buy)
    buy_button.pack(side=tk.LEFT, padx=padding)
    past_button = tk.Button(move_frame, text="Past Items",
                       width=button_w, height=button_h, command=move_to_past)
    past_button.pack(side=tk.LEFT, padx=padding)

    cart_button = tk.Button(button2_frame, text="In/Out Cart",
                       width=button_w, height=button_h, command=in_cart)
    cart_button.pack(side=tk.LEFT, padx=padding)
    delete_button = tk.Button(button2_frame, text="Delete",
                       width=button_w, height=button_h, command=delete)
    delete_button.pack(side=tk.LEFT, padx=padding)
    save_button = tk.Button(button2_frame, text="Save",
                       width=button_w, height=button_h, command=save)
    save_button.pack(side=tk.LEFT, padx=padding)

    root.mainloop()

if __name__ == "__main__":
    main()
