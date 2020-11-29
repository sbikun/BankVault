

import sys
import csv
import sqlite3
import datetime
import xml.etree.ElementTree as ET
from bankVaultModel import Txn, SummaryView, TxnClassifier


class TxnDb:
    file = 'vault.db'
    conn = None
    currView = None

    def Open (self):
        self.conn = sqlite3.connect(self.file)
        cursor = self.conn.cursor()
        cursor.execute('''create table if not exists transactions
        (d date, description text, amount real, major text, minor text, income text)''')
        self.conn.commit()
        self.currView = SummaryView()

    def Close (self):
        assert(self.conn is not None)
        self.conn.commit()
        self.conn.close()

    def PrintTxns (self):
        cursor = self.conn.cursor()
        cursor.execute('''select * from transactions''')
        for row in cursor:
            print(row)

    def FindTxn (self, txn):
        cursor = self.conn.cursor()

        #d = datetime.datetime.strptime(txn.date, '%m/%d/%Y').date()
        d = txn.datetime

        cursor.execute('select * from transactions where d=:date and description=:desc and amount=:amount', {"date":d, "desc":txn.desc, "amount":txn.amount})
        for row in cursor:
            txn.SetCategory(row[3], row[4], row[5])

    def SaveTxn (self, txn):
        cursor = self.conn.cursor()

        #d = datetime.datetime.strptime(txn.date, '%m/%d/%Y').date()
        d = txn.datetime
        dateStr = str(d.year)
        if d.month < 10:
            dateStr = dateStr + '0'
        dateStr = dateStr + str(d.month)
        if d.day < 10:
            dateStr = dateStr + '0'
        dateStr = dateStr + str(d.day)

        cursor.execute('select * from transactions where d=:date and description=:desc and amount=:amount', {"date":d, "desc":txn.desc, "amount":txn.amount})

        i = 0
        for row in cursor:
            i = i + 1

        if i is 0:
            cursor.execute(
                'insert into transactions values (:date,:desc,:amount,:major,:minor,:income)',
                {"major": txn.majorCat, "minor":txn.minorCat, "income":txn.incomeCat, "date":d, "desc":txn.desc, "amount":txn.amount}
            )
        else:
            cursor.execute('''update transactions
                  set major=:major, minor=:minor, income=:income
                  where d=:date and description=:desc and amount=:amount''',
                  {"major": txn.majorCat, "minor":txn.minorCat, "income":txn.incomeCat, "date":d, "desc":txn.desc, "amount":txn.amount}
                )
        self.conn.commit()

    def LoadFullView (self):
        cursor = self.conn.cursor()

        cursor.execute('select * from transactions')

        self.currView.categories.clear()

        for row in cursor:
            self.currView.Update(row[3], row[4], row[2])

    def LoadView (self, start, end, incomeType):
        startDateTime = datetime.date(start.year(), start.month(), start.day())
        endDateTime = datetime.date(end.year(), end.month(), end.day())
        cursor = self.conn.cursor()
        cursor.execute('select * from transactions where d >= :start and d <= :end and income = :incomeType', {"start": startDateTime, "end": endDateTime, "incomeType": incomeType})
        #cursor.execute('select * from transactions where d >= date("now","-4 months") and d <= date("now","+1 day")')
        self.currView.categories.clear()
        for row in cursor:
            self.currView.Update(row[3], row[4], row[2])

    def GetTxns (self, start, end, incomeType):
        startDateTime = datetime.date(start.year(), start.month(), start.day())
        endDateTime = datetime.date(end.year(), end.month(), end.day())
        cursor = self.conn.cursor()
        cursor.execute('select * from transactions where d >= :start and d <= :end and income = :incomeType', {"start": startDateTime, "end": endDateTime, "incomeType": incomeType})
        txns = []
        for row in cursor:
            currTxn = Txn(row[2], row[0], row[1])
            currTxn.SetCategory(row[3], row[4], row[5])
            txns.append(currTxn)
        return txns

