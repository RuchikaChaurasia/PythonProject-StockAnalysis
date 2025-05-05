# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData

class StockApp:
    def __init__(self):
        self.stock_list = []
        #check for database, create if not exists
        if path.exists("stocks.db") == False:
            stock_data.create_database()

 # This section creates the user interface

        # Create Window
        self.root = Tk()
        self.root.title("(Ruchika_Chaurasia) Stock Manager") #Replace with a suitable name for your program


        # Add Menubar
        self.menubar = Menu(self.root)

        # Add File Menu
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Load", command=self.load)
        filemenu.add_command(label="Save", command=self.save)
        self.menubar.add_cascade(label="File", menu=filemenu)

        # Add Web Menu 
        webmenu = Menu(self.menubar, tearoff=0)
        webmenu.add_command(label="Scrape Data from Yahoo! Finance", command=self.scrape_web_data)
        webmenu.add_command(label="Import CSV from Yahoo! Finance", command=self.importCSV_web_data)
        self.menubar.add_cascade(label="Web", menu=webmenu)  

        # Add Chart Menu
        chartmenu = Menu(self.menubar, tearoff=0)
        chartmenu.add_command(label="Display Chart", command=self.display_chart)
        self.menubar.add_cascade(label="Chart", menu=chartmenu)

        # Add menus to window       
        self.root.config(menu=self.menubar)

        # Add heading information
        self.headingLabel = Label(self.root, text="Stock Information", font=("Arial", 14))
        self.headingLabel.pack()
        

        # Add stock list
        self.stockList = Listbox(self.root)
        self.stockList.pack()
        self.stockList.bind("<<ListboxSelect>>", self.update_data)
        
        
        # Add Tabs
        self.tabControl = ttk.Notebook(self.root)
        self.tabMain = Frame(self.tabControl)
        self.tabHistory = Frame(self.tabControl)
        self.tabReport = Frame(self.tabControl)

        self.tabControl.add(self.tabMain, text='Main')
        self.tabControl.add(self.tabHistory, text='History')
        self.tabControl.add(self.tabReport, text='Report')
        self.tabControl.pack(expand=1, fill="both")
        

        # Set Up Main Tab
        Label(self.tabMain, text="Symbol").pack()
        self.addSymbolEntry = Entry(self.tabMain)
        self.addSymbolEntry.pack()
        Label(self.tabMain, text="Name").pack()
        self.addNameEntry = Entry(self.tabMain)
        self.addNameEntry.pack()
        Label(self.tabMain, text="Shares").pack()
        self.addSharesEntry = Entry(self.tabMain)
        self.addSharesEntry.pack()
        Button(self.tabMain, text="Add Stock", command=self.add_stock).pack()
        Label(self.tabMain, text="Update Shares").pack()
        self.updateSharesEntry = Entry(self.tabMain)
        self.updateSharesEntry.pack()
        Button(self.tabMain, text="Buy", command=self.buy_shares).pack()
        Button(self.tabMain, text="Sell", command=self.sell_shares).pack()
        Button(self.tabMain, text="Delete Stock", command=self.delete_stock).pack()

        # Setup History Tab
        self.dailyDataList = Text(self.tabHistory)
        self.dailyDataList.pack(expand=1, fill="both")
        
        
        # Setup Report Tab
        self.stockReport = Text(self.tabReport)
        self.stockReport.pack(expand=1, fill="both")

        ## Call MainLoop
        self.root.mainloop()

# This section provides the functionality
       
    # Load stocks and history from database.
    def load(self):
        self.stockList.delete(0,END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END,stock.symbol)
        messagebox.showinfo("Load Data","Data Loaded")

    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data","Data Saved")

    # Refresh history and report tabs
    def update_data(self, evt):
        self.display_stock_data()

    # Display stock price and volume history.
    def display_stock_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                self.dailyDataList.delete("1.0",END)
                self.stockReport.delete("1.0",END)
                self.dailyDataList.insert(END,"- Date -   - Price -   - Volume -\n")
                self.dailyDataList.insert(END,"=================================\n")
                for daily_data in stock.DataList:
                    row = daily_data.date.strftime("%m/%d/%y") + "   " +  '${:0,.2f}'.format(daily_data.close) + "   " + str(daily_data.volume) + "\n"
                    self.dailyDataList.insert(END,row)

                #display report
                if stock.DataList:
                    # Summary statistics
                    closes = [d.close for d in stock.DataList]
                    volumes = [d.volume for d in stock.DataList]
                    total_days = len(closes)
                    first_close = closes[0]
                    last_close = closes[-1]
                    percent_change = ((last_close - first_close) / first_close) * 100

                    summary = f"""📈 Performance Summary for {stock.name}
            ----------------------------------------
            Symbol: {stock.symbol}
            Total Days Tracked: {total_days}
            Starting Price: ${first_close:.2f}
            Latest Price: ${last_close:.2f}
            % Change: {percent_change:.2f}%
            Highest Close: ${max(closes):.2f}
            Lowest Close: ${min(closes):.2f}
            Average Close: ${sum(closes)/total_days:.2f}
            Total Volume: {int(sum(volumes)):,}

            Daily Price & Volume History
            -----------------------------
            """

                self.stockReport.insert(END, summary)

                # Daily rows
                for d in stock.DataList:
                    row = f"{d.date.strftime('%m/%d/%y')}: ${d.close:.2f}, Vol: {int(d.volume)}\n"
                    self.stockReport.insert(END, row)


    # Add new stock to track.
    def add_stock(self):
        new_stock = Stock(self.addSymbolEntry.get(),self.addNameEntry.get(),float(str(self.addSharesEntry.get())))
        self.stock_list.append(new_stock)
        self.stockList.insert(END,self.addSymbolEntry.get())
        self.addSymbolEntry.delete(0,END)
        self.addNameEntry.delete(0,END)
        self.addSharesEntry.delete(0,END)

    # Buy shares of stock.
    def buy_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Buy Shares","Shares Purchased")
        self.updateSharesEntry.delete(0,END)

    # Sell shares of stock.
    def sell_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Sell Shares","Shares Sold")
        self.updateSharesEntry.delete(0,END)

    # Remove stock and all history from being tracked.
    def delete_stock(self):
        if not self.stockList.curselection():
            return  # No stock selected

        symbol = self.stockList.get(self.stockList.curselection())

        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.stock_list.remove(stock)
                self.stockList.delete(self.stockList.curselection())
                self.dailyDataList.delete("1.0", END)
                self.stockReport.delete("1.0", END)
                self.headingLabel['text'] = "Stock Information"
                messagebox.showinfo("Delete Stock", f"{symbol} deleted successfully.")
                return  # ← cleaner than break


    # Get data from web scraping.
    def scrape_web_data(self):
        dateFrom = simpledialog.askstring("Starting Date","Enter Starting Date (m/d/yy)")
        dateTo = simpledialog.askstring("Ending Date","Enter Ending Date (m/d/yy")
        try:
            stock_data.retrieve_stock_web(dateFrom,dateTo,self.stock_list)
        except:
            messagebox.showerror("Cannot Get Data from Web","Check Path for Chrome Driver")
            return
        self.display_stock_data()
        messagebox.showinfo("Get Data From Web","Data Retrieved")

    # Import CSV stock history file.
    def importCSV_web_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(title="Select " + symbol + " File to Import",filetypes=[('Yahoo Finance! CSV','*.csv')])
        if filename != "":
            stock_data.import_stock_web_csv(self.stock_list,symbol,filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete",symbol + "Import Complete")   
    
    # Display stock price chart.
    def display_chart(self):
        symbol = self.stockList.get(self.stockList.curselection())
        display_stock_chart(self.stock_list,symbol)


def main():
        app = StockApp()
        

if __name__ == "__main__":
    # execute only if run as a script
    main()