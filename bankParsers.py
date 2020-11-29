
import sys
import csv
from bankVaultModel import Txn, SummaryView, TxnClassifier

class AMEXParser:
    transactions = []

    def __init__(self):
        pass

    def Parse (self, file):
        self.transactions.clear()

        with open(file, 'r') as csvfile:
            txnReader = csv.reader(csvfile, delimiter=',', quotechar='"')

            for row in txnReader:
                date = row[0].split(' ', 1)[0]
                cost = str(-float(row[7]))
                # -1 is to match BOA standard
                curr = Txn(cost, date, row[2])
                self.transactions.append(curr)

    def SetCategory (self, amount, date, desc, major, minor, income):
        for txn in self.transactions:
            if (txn.amount == amount and txn.date == date and txn.desc == desc):
                txn.SetCategory(major, minor, income)

class BBVAParser:
    transactions = []

    def __init__(self):
        pass

    def Parse (self, file):
        self.transactions.clear()
        i = 0

        with open(file, 'r') as csvfile:
            txnReader = csv.reader(csvfile, delimiter=',', quotechar='"')

            for row in txnReader:
                if i < 5:
                    #Skip header rows
                    pass
                else:
                    curr = Txn(row[5], row[1], row[3], '%d/%m/%Y')
                    self.transactions.append(curr)
                i = i + 1

    def SetCategory (self, amount, date, desc, major, minor, income):
        for txn in self.transactions:
            if (txn.amount == amount and txn.date == date and txn.desc == desc):
                txn.SetCategory(major, minor, income)

class BOAVisaParser:
    transactions = []

    def __init__(self):
        pass

    def Parse(self, file):
        self.transactions.clear()
        i = 0
        with open(file, 'r') as csvfile:
            txnReader = csv.reader(csvfile, delimiter=',', quotechar='"')

            for row in txnReader:
                if i < 2:
                    #Skip header row
                    pass
                else:
                    curr = Txn(row[4], row[0], row[2])
                    self.transactions.append(curr)
                i = i + 1

    def SetCategory (self, amount, date, desc, major, minor, income):
        for txn in self.transactions:
            if (txn.amount == amount and txn.date == date and txn.desc == desc):
                txn.SetCategory(major, minor, income)

class BOAParser:
    transactions = []

    def __init__(self):
        pass

    def Parse (self, file):
        self.transactions.clear()
        i = 0
        with open(file, 'r') as csvfile:
            txnReader = csv.reader(csvfile, delimiter=',', quotechar='"')

            for row in txnReader:
                if i < 8:
                    #Skip header, column names, and starting balance
                    pass
                else:
                    curr = Txn(row[2], row[0], row[1])
                    self.transactions.append(curr)
                i = i + 1

    def SetCategory (self, amount, date, desc, major, minor, income):
        for txn in self.transactions:
            if (txn.amount == amount and txn.date == date and txn.desc == desc):
                txn.SetCategory(major, minor, income)
