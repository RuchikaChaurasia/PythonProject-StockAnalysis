# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

# Add new stock to track
def add_stock(stock_list):
    option = ""
    while option != "0":
        pass
        
# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        pass


# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    print("Stock List: [",end="")
    pass

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    pass

# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    pass


# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    pass

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    pass

# Display Report for All Stocks
def display_report(stock_data):
    clear_screen()
    print("Stock Report ---")
    for stock in stock_data:
        pass


  


# Display Chart
def display_chart(stock_list):
    print("Stock List: [",end="")
    for stock in stock_list:
        pass

# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        pass


# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    pass

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    pass

# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()