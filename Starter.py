import numpy as np
import pandas as pd
import matplotlib.pyplot as pl

class Starter:
    """
    The Starter class to load, sort, clean up and filter the invoice data
    """

    def __init__(self):
        """
        initializer
        TODO: Tidy up how the dataframes are stored, have one dataframe that is unchanged throughout the functions for reference
        """
        self.path = "invoices.csv"
        self.df = self.loadInvoices()
        self.rf = self.loadInvoices()
        self.quantity = [] # Quantity dataframe
        self.ap = [] # Average price
        self.pr = [] # Price reference
        self.ps = [] # Price sensitivity
        self.ac = [] # Acreage Data
        self.ds = [] # Diesel Spending
        self.ss = [] # Diesel Spending
        self.fs = [] # Diesel Spending
        self.cs = [] # Diesel Spending
        self.ps = [] # Diesel Spending
        self.prelim()


    def loadDataframe(self, path):
        """
        Load a csv file from a given path
        Inputs: path, a string indicating the location of the csv file
        Outputs: a pandas dataframe representing the csv file
        """
        df = pd.read_csv(path, sep=',', header = 0)
        return df

    def loadInvoices(self):
        """
        Load the invoice data
        Outputs: a pandas dataframe representing the invoice.csv file
        """
        invoice = self.loadDataframe("invoices.csv")
        return invoice
    
    def sortClientDateTotal(self):
        """
        Sorts the data according to client ID, date of invoice and total spending, in that order of priority
        """
        self.df = self.df.sort_values(by=['client_id', 'invoice_date', 'total'])

    def combineYear(self):
        """
        Ignores the exact dates and just focus on the year
        """
        self.df['invoice_date'] = self.df['invoice_date'].map(lambda x: x[0:4], na_action = 'ignore')
        self.df.loc[self.df.invoice_date == '6201', 'invoice_date'] = self.df.invoice_date[self.df.invoice_date == '6201'].map(lambda x: '2016', na_action = 'ignore')
        self.rf['invoice_date'] = self.rf['invoice_date'].map(lambda x: x[0:4], na_action = 'ignore')
        self.rf.loc[self.rf.invoice_date == '6201', 'invoice_date'] = self.rf.invoice_date[self.rf.invoice_date == '6201'].map(lambda x: '2016', na_action = 'ignore')

    def extractClientDateTotal(self, lst):
        """
        Selects the most interesting columns of the dataframe
        Inputs: lst, a list of strings indicating the columns to select
        """
        self.df = self.df[lst]

    def extractClientDateItemTotal(self, lst):
        self.ap = self.rf[lst]

    def extractClientDateItemQuantity(self, lst):
        self.quantity = self.rf[lst]

    def prelim(self):
        """
        Preliminary cleanup of data to be called in the initializer.
        Sorts data according to client ID, date of invoice and total amount in that order of priority
        Ignores month and days and focuses on year of invoice
        Extracts the columns containing client ID, invoice year and total spending
        """

        self.sortClientDateTotal()
        self.combineYear()
        self.extractClientDateTotal(['client_id', 'invoice_date', 'total'])
        self.extractClientDateItemQuantity(['client_id', 'item__category__name', 'invoice_date', 'item__name', 'quantity'])         
        self.extractClientDateItemTotal(['client_id', 'item__category__name', 'invoice_date', 'item__name', 'total'])
        self.totalSpending()
        self.averagePrice()
        self.priceRef()
        self.priceSensitivity()
        self.loadAcres()
        self.itemSpending()

    def totalSpending(self):
        """
        Aggregate the total spending during a year for each client
        TODO: Incorporate the invoice date and client id
        """
        self.df = self.df.groupby(['invoice_date', 'client_id'], as_index=False).sum()


    def byClient(self):
        """
        Breaks the data into chunks according to client
        TODO: Find a faster way to group the data by changing iter into something else
        """
        return dict(iter(self.df.groupby('client_id', as_index=False)))

    def plotGraph(self, id):
        """
        Generates a sales-trend graph from a client ID
        Inputs: An int client_id
        TODO: It wouldn't make sense if 2021 data is included in the regression. Make sure to
        not include 2021 data
        """
        dic = self.byClient()
        pl.plot(dic[id].invoice_date, dic[id].total)
        pl.title("Client ID: " + str(id))
        pl.xlabel('year')
        pl.ylabel('total spending')
        pl.show()

    def averagePrice(self):
        """
        Gets the average price paid by a customer for a certain product in a particular year
        TODO: Clean up data. Some of the items are not standardized products and should be taken out of the dataframe
        """
        self.ap = self.ap.loc[self.ap.item__category__name != 'Service']
        self.ap = self.ap.loc[self.ap.item__category__name.notna()]
        self.ap = self.ap.groupby(['invoice_date', 'client_id', 'item__name'], as_index=False).sum()
        self.quantity = self.quantity.loc[self.quantity.item__category__name != 'Service']
        self.quantity = self.quantity.loc[self.quantity.item__category__name.notna()]
        self.quantity = self.quantity.groupby(['invoice_date', 'client_id', 'item__name'], as_index=False).sum()
        self.ap['quantity'] = self.quantity.groupby(['invoice_date', 'client_id', 'item__name'], as_index=False).sum().quantity        
        self.ap['average_price'] = self.rf.groupby(['invoice_date', 'client_id', 'item__name'], as_index=False).sum().total / self.quantity.groupby(['invoice_date', 'client_id', 'item__name'], as_index=False).sum().quantity
        self.ap = self.ap[['invoice_date', 'item__name', 'average_price', 'client_id']]

    def priceRef(self):
        """
        Gets the average price paid by all customers for a certain product in a particular year
        """
        self.pr = self.rf.groupby(['invoice_date', 'item__name'], as_index=False).sum()
        self.pr['quantity'] = self.quantity.groupby(['invoice_date', 'item__name'], as_index=False).sum().quantity
        self.pr['average_price_ref'] = self.rf.groupby(['invoice_date', 'item__name'], as_index=False).sum().total / self.quantity.groupby(['invoice_date', 'item__name'], as_index=False).sum().quantity
        self.pr = self.pr[['invoice_date', 'item__name', 'average_price_ref']]

    def priceSensitivity(self):
        """
        Gets the price sensitivity by comparing the individual price paid to the aggregate average price paid
        """
        self.ps = self.ap
        self.ps = self.ap.merge(self.pr, how = 'left')
        self.ps['price_sensitivity'] = self.ps.average_price/self.ps.average_price_ref

    def loadAcres(self):
        self.ac = self.loadDataframe('Claremont Acreage Data.csv')
    
    def mergeAcres(self):
        self.ac = pd.merge(self.rf, self.ac, on = 'client_id', how = 'left')

    def itemSpending(self):
        self.ds = self.rf[self.rf['item__name'].str.contains('Diesel') == True]
        self.ss = self.rf[self.rf['item__name'].str.contains('Seed') == True]
        self.fs = self.rf[self.rf['item__name'].str.contains('Fertilizer') == True]
        self.cs = self.rf[self.rf['item__name'].str.contains('Chemical') == True]        
        self.ps = self.rf[self.rf['item__name'].str.contains('Propane') == True]