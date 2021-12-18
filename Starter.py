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
        self.s = self.loadInvoices()
        self.df = self.loadInvoices()
        self.rf = self.loadInvoices()
        self.mo = [] # Monthly Data
        self.se = [] # Seasonal Data
        self.seavg = [] # Seasonal monthly average
        self.mows_12 = [] # months with sales in the past 12 months
        self.mows_36 = [] # months with sales in the past 36 months
        self.mows_12r = [] # recency of the months with sales in the past 12 months
        self.mows_36r = [] # recency of the months with sales in the past 36 months  
        self.quantity = [] # Quantity dataframe
        self.ap = [] # Average price
        self.pr = [] # Price reference
        self.ps = [] # Price sensitivity
        self.spend16 = [] # spending in 2016
        self.spend20 = [] # spending in 2020
        self.change = [] # change in spending
        self.ac = [] # Acreage Data
        self.ds = [] # Diesel Spending
        self.ss = [] # Seeds Spending
        self.fs = [] # Fuel Spending
        self.cs = [] # Chemical Spending
        self.prs = [] # Propane Spending
        self.ws = [] # Wallet Share
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

    def combineMonth(self):
        """
        Ignores the exact dates and just focus on the month
        """        
        self.mo = self.s
        self.mo['invoice_date'] = self.s['invoice_date'].map(lambda x: x[0:7], na_action = 'ignore')
        self.mo.loc[self.mo.invoice_date.str.contains('6201'), 'invoice_date'] = self.mo.invoice_date[self.mo.invoice_date.str.contains('6201')].map(lambda x: '2016-' + x[5:], na_action = 'ignore')
     
    def getSeason(self, string):
        if ('-03' in string or '-04' in string or '-05' in string):
            return '-1'
        elif ('-06' in string or '-07' in string or '-08' in string):
            return '-2'
        elif ('-09' in string or '-10' in string or '-11' in string):
            return '-3'
        elif ('-12' in string or '-01' in string or '-02' in string):
            return '-4'           

    def monthlystd(self):
        self.mostd = self.mo[['invoice_id', 'line_number', 'client_id', 'invoice_date', 'total']].groupby(['client_id', 'invoice_date'], as_index = True).std(1)
        self.mostd = self.mostd['total']
        self.mostd = self.mostd.reset_index()
        self.mostd.to_csv('monthly std.csv')

    def combineSeason(self):
        """
        Ignores the exact dates and just focus on the month
        """        
        self.se = self.mo
        self.se['invoice_date'] = self.se['invoice_date'].map(lambda x: x[0:4] + self.getSeason(x), na_action = 'ignore')
     
    def seasonalavg(self):
        self.seavg = self.se[['invoice_id', 'line_number', 'client_id', 'invoice_date', 'total']].groupby(['client_id', 'invoice_date'], as_index = True).mean()/3
        self.seavg = self.seavg.reset_index(level= ['client_id', 'invoice_date'])
        self.seavg = self.seavg.rename(columns = {"total": "average"})
        self.seavg = self.seavg[['invoice_date', 'client_id', 'average']]
        self.seavg[self.seavg.invoice_date.str.contains('-1')].to_csv('winter average.csv')
        self.seavg[self.seavg.invoice_date.str.contains('-2')].to_csv('spring average.csv')
        self.seavg[self.seavg.invoice_date.str.contains('-3')].to_csv('summer average.csv')
        self.seavg[self.seavg.invoice_date.str.contains('-4')].to_csv('autumn average.csv')

    def monthsHelper(self, client_1, date_1, client_2, date_2, year):
        if (client_1 == client_2): 
            intYear_1 = int(date_1[0:4])
            intYear_2 = int(date_2[0:4])
            intMonth_1 = int(date_1[5:])
            intMonth_2 = int(date_2[5:])
            if (abs(intYear_1 - intYear_2) < year):
                return 1
            elif (abs(intYear_1 - intYear_2) == year and ((intMonth_1 - intMonth_2) < 0)):
                return 1
            return 0
        return 0

    def getMonths(self, date_1, date_2):
        intYear_1 = int(date_1[0:4])
        intYear_2 = int(date_2[0:4])
        intMonth_1 = int(date_1[5:])
        intMonth_2 = int(date_2[5:])    
        return (intYear_1 - intYear_2) * 12 + (intMonth_1 - intMonth_2)    

    def clientMonth_unique(self):
        temp_1 = self.mo[['invoice_date', 'client_id']].drop_duplicates()
        temp_1 = temp_1.sort_values(by = ['client_id', 'invoice_date'], ascending = True)
        temp_1.loc[len(temp_1)] = ['0000-00', 0]
        temp_1 = temp_1.reset_index()[['index', 'invoice_date', 'client_id']]
        temp_2 = self.mo[['invoice_date', 'client_id']].drop_duplicates()
        temp_2 = temp_2.sort_values(by = ['client_id', 'invoice_date'], ascending = True)
        temp_2 = pd.concat([pd.DataFrame({'invoice_date': '0000-00','client_id': 0} , index = [0]), temp_2]).reset_index(drop = True)
        temp_2 = temp_2.reset_index()
        temp_3 = pd.concat([temp_1, temp_2], axis = 1, ignore_index = True)
        temp_4 = pd.concat([temp_1, temp_2], axis = 1, ignore_index = True)
        temp_3['Previous_month'] = temp_3.apply(lambda x: self.monthsHelper(x[2], x[1], x[5], x[4], 1), axis = 1)
        temp_4['Previous_month'] = temp_4.apply(lambda x: self.monthsHelper(x[2], x[1], x[5], x[4], 3), axis = 1)
        self.mows_12 = pd.DataFrame(temp_3.copy().iloc[:, 6])
        self.mows_12['client_id'] = temp_3.copy().iloc[:, 2]
        self.mows_12['invoice_date'] = temp_3.copy().iloc[:, 1]
        self.mows_36 = pd.DataFrame(temp_4.copy().iloc[:, 6])
        self.mows_36['client_id'] = temp_4.copy().iloc[:, 2]
        self.mows_36['invoice_date'] = temp_4.copy().iloc[:, 1]
        self.mows_12r = self.mows_12.groupby(by = 'client_id', as_index = False).sum()
        self.mows_36r = self.mows_36.groupby(by = 'client_id', as_index = False).sum()
        self.mows_12['recency'] = self.mows_12.apply(lambda x: self.getMonths("2021-11", x[2]), axis = 1)
        self.mows_36['recency'] = self.mows_36.apply(lambda x: self.getMonths("2021-11", x[2]), axis = 1)
        self.mows_12r['recency'] = self.mows_12.groupby(by = 'client_id').min()['recency']
        self.mows_36r['recency'] = self.mows_36.groupby(by = 'client_id').min()['recency']
        
        # self.mows_12.to_csv('months with purchase in past 12 months.csv')
        # self.mows_36.to_csv('months with purchase in past 36 months.csv')


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
        self.combineMonth()
        self.combineSeason()
        self.seasonalavg()
        self.monthlystd()
        self.totalSpending()
        self.percentageChange()
        self.averagePrice()
        self.priceRef()
        self.priceSensitivity()
        self.loadAcres()
        self.mergeAcres()
        self.itemSpending()

    def totalSpending(self):
        """
        Aggregate the total spending during a year for each client
        TODO: Incorporate the invoice date and client id
        """
        self.df = self.df.groupby(['invoice_date', 'client_id'], as_index=False).sum()

    def percentageChange(self):
        """
        TODO: Weed out negative changes, make discounting a for loop 
        """
        self.spend16 = self.df[self.df.invoice_date == '2016']
        self.spend20 = self.df[self.df.invoice_date == '2020']
        self.change = pd.merge(self.spend20, self.spend16, on = "client_id", how = 'outer')
        self.change = self.change.rename(columns = {"total_x": "total_20"})
        self.change = self.change.rename(columns = {"invoice_date_x": "date_20"})
        self.change = self.change.rename(columns = {"total_y": "total_16"})
        self.change = self.change.rename(columns = {"invoice_date_y": "date_16"})
        self.change = pd.merge(self.change, self.df[self.df.invoice_date == '2017'], on = 'client_id', how = 'outer')
        self.change = self.change.rename(columns = {"total": "total_17"})
        self.change = self.change.rename(columns = {"invoice_date": "date_17"})
        self.change = pd.merge(self.change, self.df[self.df.invoice_date == '2018'], on = 'client_id', how = 'outer')
        self.change = self.change.rename(columns = {"total": "total_18"})
        self.change = self.change.rename(columns = {"invoice_date": "date_18"})
        self.change = pd.merge(self.change, self.df[self.df.invoice_date == '2019'], on = 'client_id', how = 'outer')
        self.change = self.change.rename(columns = {"total": "total_19"})
        self.change = self.change.rename(columns = {"invoice_date": "date_19"})
        self.change['change17'] = (self.change.total_17/self.change.total_16).fillna(0)
        self.change['change18'] = (self.change.total_18/self.change.total_17).fillna(0)
        self.change['change19'] = (self.change.total_19/self.change.total_18).fillna(0)
        self.change['change20'] = (self.change.total_20/self.change.total_19).fillna(0)
        self.change.replace([np.inf, -np.inf], np.nan, inplace = True)
        self.change['aggChange'] = self.change.change20 + self.change.change19/1.1 + self.change.change18/1.1**2 + self.change.change17/1.1**3
        self.change['percentile'] = self.change.aggChange.rank(pct = True)

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
        self.ap = self.ap[['invoice_date', 'item__name', 'quantity', 'average_price', 'client_id']]

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
        """TODO: Remove "adj" and "discount" from items included"""
        self.ds = self.rf[self.rf['item__name'].str.contains('Diesel') == True]
        self.ss = self.rf[self.rf['item__name'].str.contains('Seed') == True]
        self.fs = self.rf[self.rf['item__name'].str.contains('Fertilizer') == True]
        self.cs = self.rf[self.rf['item__name'].str.contains('Chemical') == True]   
        self.prs = self.rf[self.rf['item__category__name'].str.contains('Propane') == True]
        self.ds = self.ds.rename(columns = {"total": "Diesel"})
        self.ss = self.ss.rename(columns = {"total": "Seed"})
        self.fs = self.fs.rename(columns = {"total": "Fertilizer"})
        self.cs = self.cs.rename(columns = {"total": "Chemical"})     
        self.prs = self.prs.rename(columns = {"total": "Propane"})
        self.ds = self.ds.groupby(['invoice_date', 'client_id'], as_index=False).sum()
        self.ss = self.ss.groupby(['invoice_date', 'client_id'], as_index=False).sum()
        self.fs = self.fs.groupby(['invoice_date', 'client_id'], as_index=False).sum()
        self.cs = self.cs.groupby(['invoice_date', 'client_id'], as_index=False).sum()
        # self.prs = self.prs.groupby(['invoice_date', 'client_id'], as_index=False).sum()
        self.ws = self.rf[['client_id', 'invoice_date']] # TODO: modularize this
        return pd.merge(self.ws, self.ds, how = "left", left_on = ["client_id", "invoice_date"], right_on = ["client_id", "invoice_date"])