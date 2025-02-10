# Grocery List
## Description
A simple python program using tkinter to keep track of groceries. 
The groceries are sorted into 3 lists: 
  - Fridge: Items that the user has in their fridge
  - To Buy: Items that the user needs to buy
  - Past Items: Items that the user had in the past, but is not currently in the fridge or the user needs to buy.

The user can easily sort the lists by the following:
  - `food`: alphabetically
  - `food_type`: alphabetically by food type
  - `amount`: ascending
  - `in_cart`: for items in To Buy, items that are in the user's cart get sent to the bottom of the list
By default, the lists are sorted by `in_cart`

The user can also easily add items. By default, the item is added to the To Buy list, with an amount of 1.

The user can also change the following aspects of item(s) by selecting item(s) within a list:
  - Amount: the amount of each selected item
  - Move Items to Fridge, To Buy, or Past Items: move selected items to the selected list
  - In/Out Cart: switch whether or not each item is in or out of the user's cart
  - Delete: deletes the item from all lists
  - Save: saves information to the CSV file

## CSV File Requirements - Grocery List
The csv file for requires the following column names:
  - `food`: (`String`) the name of the food item
  - `food_type`: (`String`) the type of the food item
  - `is_stocked`: (`Boolean`) if the item is in the fridge
  - `need_to_buy`: (`Boolean`) if the user needs to buy the item
  - `amount`: (`int`) amount of the item
  - `in_cart`: (`Boolean`) if the item is in the user's cart

## Adapting the Code
Adapting the code is simple, the user just needs to change the `FILE_NAME` to the name of their csv file.
When saving, the file is overwritten.

```
FILE_NAME = 'groceries.csv'
grocery_list = pd.read_csv(FILE_NAME)
```
