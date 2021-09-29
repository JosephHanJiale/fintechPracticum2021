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
        """
        self.path = "invoices.csv"
        self.df = self.loadInvoices()
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

    def extractClientDateTotal(self, lst):
        """
        Selects the most interesting columns of the dataframe
        Inputs: lst, a list of strings indicating the columns to select
        """
        self.df = self.df[lst]

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
        self.totalSpending()

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



