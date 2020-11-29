
import sys
import datetime

class Txn:
    amount = None
    date = None
    datetime = None
    dateformat = '%m/%d/%Y'
    desc = None
    majorCat = None
    minorCat = None
    incomeCat = 'Monthly'

    #def __init__ (self, amount, date, description):
    #    self.amount = amount
    #    self.date = date
    #    self.desc = description
    #    self.datetime = datetime.datetime.strptime(self.date, self.dateformat).date()

    def __init__ (self, amount, date, description, dateformat = '%m/%d/%Y'):
        self.amount = amount
        self.date = date
        self.desc = description
        self.dateformat = dateformat
        self.datetime = datetime.datetime.strptime(self.date, self.dateformat).date()

    def SetCategory (self, major, minor, income):
        self.majorCat = major
        self.minorCat = minor
        self.incomeCat = income

class SummaryView:
    categories = None

    def __init__(self):
        self.categories = {}

    def Update(self, category, subCategory, amount):
        if self.categories.get(category):
            if (self.categories[category].get(subCategory)):
                self.categories[category][subCategory] += amount
            else:
                self.categories[category][subCategory] = amount
        else:
            self.categories[category] = {}
            self.categories[category][subCategory] = amount

class TxnClassifier:
    regex = None
    majorCat = None
    minorCat = None

    def __init__ (self, regex, majorCat, minorCat):
        self.regex = regex
        self.majorCat = majorCat
        self.minorCat = minorCat
