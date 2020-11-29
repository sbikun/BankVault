# ------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Steve
#
# Created:     27/04/2013
# Copyright:   (c) Steve 2013
# Licence:     <your licence>
# ------------------------------------------------------------------------------

import sys
import csv
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import datetime
import xml.etree.ElementTree as ET
from editorUi import Ui_TxnEditWidget
from viewDialogUi import Ui_ViewDialog
from bankVaultModel import Txn, SummaryView, TxnClassifier
from dblayer import TxnDb, SummaryView
from bankParsers import AMEXParser, BBVAParser, BOAParser, BOAVisaParser

#-------------------------------------------------------------------------------
#
# Globals
#
#-------------------------------------------------------------------------------
g_categoriesFile = "./Data/categories.xml"
g_classifiersFile = "./Data/classifiers.xml"

#-------------------------------------------------------------------------------
#
# Classes
#
#-------------------------------------------------------------------------------


class CategoryParser:
    majorCategories = []
    minorCategories = []

    def __init__(self):
        pass

    def parse(self, file):
        self.majorCategories.clear()
        self.minorCategories.clear()

        tree = ET.parse(file)
        root = tree.getroot()

        if root.tag != 'Categories':
            return

        for category in root.findall('MajorCategory'):
            name = category.get('name')
            self.majorCategories.append(name)
            for subCat in category.findall('MinorCategory'):
                subName = subCat.get('name')
                self.minorCategories.append(subName)

        self.majorCategories.sort()
        self.minorCategories.sort()


class AutoClassifier:
    classifiers = []

    def __init__(self):
        pass

    def Parse(self, file):
        self.classifiers.clear()

        tree = ET.parse(file)
        root = tree.getroot()

        if root.tag != "Classifiers":
            return

        for classifier in root.findall('Classifier'):
            regex = classifier.get('regex')
            majorCat = classifier.get('majorCategory')
            minorCat = classifier.get('minorCategory')
            print("Classifier Loaded! Regex: ", regex, "Cats: ", majorCat, " ", minorCat)
            self.classifiers.append(TxnClassifier(regex, majorCat, minorCat))

    def classify (self, txn):
        for classifier in self.classifiers:
            if txn.desc.find(classifier.regex) != -1:
                txn.majorCat = classifier.majorCat
                txn.minorCat = classifier.minorCat
                return True
        return False


class ViewDialog(QtGui.QDialog):
    parent = None

    def __init__(self, parent):
        self.parent = parent
        QtGui.QDialog.__init__(self, parent)
        self.ui=Ui_ViewDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.on_okButton_clicked)

    def on_okButton_clicked (self):
        startDate = self.ui.calendarWidget.selectedDate()
        endDate = self.ui.calendarWidget_2.selectedDate()
        if startDate > endDate:
            return
        self.parent.on_view_changed(startDate, endDate, self.ui.comboBox.currentText())
        pass

class TxnEditor(QtGui.QWidget):
    currTxn = None
    item = None

    def __init__ (self, parent):
        QtGui.QWidget.__init__(self,parent)
        self.ui=Ui_TxnEditWidget()
        self.ui.setupUi(self)
        self.setGeometry(375, 375, 600, 150)
        self.show()
        self.ui.buttonSave.clicked.connect(self.on_buttonSave_clicked)

    def Edit (self, txn):
        self.item = txn
        self.ui.labelDate.setText(txn.task.date)
        self.ui.labelDesc.setText(txn.task.desc)
        self.ui.labelPrice.setText(txn.task.amount)

    def SetCategories (self, categories, currMajorCat, currMinorCat, currIncomeCat):
        self.ui.comboIncomeCat.clear()
        self.ui.comboMajorCats.clear()
        self.ui.comboMinorCats.clear()

        row = 0
        majorCat = 0
        i = 0
        for cat in categories.majorCategories:
            if cat == currMajorCat:
                majorCat = i
            self.ui.comboMajorCats.addItem(cat)
            i = i + 1

        minorCat = 0
        i = 0
        for cat in categories.minorCategories:
            if cat == currMinorCat:
                minorCat = i
            self.ui.comboMinorCats.addItem(cat)
            i = i + 1

        self.ui.comboIncomeCat.addItem('Monthly')
        self.ui.comboIncomeCat.addItem('Yearly')
        self.ui.comboIncomeCat.addItem('Bonus')

        self.ui.comboMajorCats.setCurrentIndex(majorCat)
        self.ui.comboMinorCats.setCurrentIndex(minorCat)


    def on_buttonSave_clicked (self):
        if self.item is None:
            return
        self.item.task.majorCat = self.ui.comboMajorCats.currentText()
        self.item.task.minorCat = self.ui.comboMinorCats.currentText()
        self.item.task.incomeCat = self.ui.comboIncomeCat.currentText()
        self.item.setText(3, self.item.task.majorCat)
        self.item.setText(4, self.item.task.minorCat)
        self.item.setText(5, self.item.task.incomeCat)


class MainWindow(QtGui.QMainWindow):
    currFile = None
    currIncomeType = None
    categoryParser = None
    db = None
    endDate = None
    endDateLabel = None
    startDate = None
    startDateLabel = None
    txnClassifier = None
    txnEditor = None
    txnParser = None
    txnTree = None
    viewDialog = None

    def __init__(self):
        super(MainWindow, self).__init__()

        self.db = TxnDb()
        self.db.Open()
        self.db.LoadFullView()
        self.init_ui()
        self.init_summary_table()
        self.init_txn_table()
        self.categoryParser = CategoryParser()
        self.categoryParser.parse(g_categoriesFile)
        self.txnClassifier = AutoClassifier()
        self.txnClassifier.Parse(g_classifiersFile)
        self.txnEditor = TxnEditor(self)

    def init_ui(self):
        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.start_close)

        saveAction = QtGui.QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save transactions')
        saveAction.triggered.connect(self.saveTxns)

        openAction = QtGui.QAction('Open BOA', self)
        openAction.setStatusTip('Open a file')
        openAction.triggered.connect(self.open_file)

        openAmexAction = QtGui.QAction('Open AMEX', self)
        openAmexAction.setStatusTip('Open a file')
        openAmexAction.triggered.connect(self.open_amex_file)

        openBbvaAction = QtGui.QAction('Open BBVA', self)
        openBbvaAction.setStatusTip('Open a file')
        openBbvaAction.triggered.connect(self.open_bbva_file)

        openBoaVisaAction = QtGui.QAction('Open BOA Visa', self)
        openBoaVisaAction.setStatusTip('Open a file')
        openBoaVisaAction.triggered.connect(self.open_boavisa_file)

        reloadAction = QtGui.QAction('Reload', self)
        reloadAction.setShortcut('Ctrl+R')
        reloadAction.setStatusTip('Reload current category file')
        reloadAction.triggered.connect(self.reload_categories)

        reloadClassifiersAction = QtGui.QAction('Reload Classifiers', self)
        reloadClassifiersAction.setStatusTip('Reload current classifier file')
        reloadClassifiersAction.triggered.connect(self.reload_classifiers)

        autoClassifyAction = QtGui.QAction('Auto Classify', self)
        autoClassifyAction.setStatusTip('Auto classify current loaded transactions')
        autoClassifyAction.triggered.connect(self.autoClassify)

        exportAction = QtGui.QAction('Export', self)
        exportAction.setStatusTip('Export current view to .csv')
        exportAction.triggered.connect(self.exportCurrView)

        exportYearAction = QtGui.QAction('Export Year', self)
        exportYearAction.setStatusTip('Export view of major categories for the year')
        exportYearAction.triggered.connect(self.exportYearView)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(openAction)
        file_menu.addAction(openAmexAction)
        file_menu.addAction(openBbvaAction)
        file_menu.addAction(openBoaVisaAction)
        file_menu.addAction(saveAction)
        file_menu.addAction(exitAction)
        file_menu.addAction(exportAction)
        file_menu.addAction(exportYearAction)
        cat_menu = menu_bar.addMenu('&Categories')
        cat_menu.addAction(reloadAction)
        classify_menu = menu_bar.addMenu('&Classify')
        classify_menu.addAction(reloadClassifiersAction)
        classify_menu.addAction(autoClassifyAction)
        cat_menu.addAction(reloadClassifiersAction)

        self.resize(320*4+135, 240*2)
        self.setWindowTitle("BankVault")
        self.show()

    def init_summary_table(self):
        self.startDateLabel = QLabel('Start:', self)
        self.startDateLabel.setGeometry(30, 25, 150, 20)
        self.startDateLabel.show()
        self.endDateLabel = QLabel('End:', self)
        self.endDateLabel.setGeometry(170, 25, 150, 20)
        self.endDateLabel.show()
        self.viewButton = QPushButton(self)
        self.viewButton.setGeometry(300, 25, 20, 20)
        self.viewButton.show()
        self.viewButton.clicked.connect(self.on_viewButton_clicked)

        self.summaryTable = QTableWidget(50, 3, self)

        table_headers = ['Category', 'Goal', 'Actual']
        self.summaryTable.setHorizontalHeaderLabels(table_headers)
        self.summaryTable.setGeometry(0, 50, 324, self.height()-20)
        self.summaryTable.show()

        self.display_summary_view()

    def display_summary_view(self):
        self.summaryTable.clearContents()
        row = 0
        for mainCat, subCats in self.db.currView.categories.items():
            self.summaryTable.setItem(row, 0, QtGui.QTableWidgetItem(mainCat))
            row += 1
            for subCatName, amount in subCats.items():
                self.summaryTable.setItem(row, 0, QtGui.QTableWidgetItem(subCatName))
                self.summaryTable.setItem(row, 2, QtGui.QTableWidgetItem(str(-amount)))
                row += 1
            row += 1  # skip a row

    def init_txn_table(self):
        tree = QTreeWidget(self)
        tree.setColumnWidth(1, 500)

        self.txnTree = QTreeWidget(self)
        self.txnTree.setColumnCount(6)
        self.txnTree.setColumnWidth(1, 500)
        self.txnTree.setAlternatingRowColors(True)
        self.txnTree.show()
        txn_tree_x = self.summaryTable.width() + 50
        txn_tree_y = 25
        txn_tree_width = self.width() - self.summaryTable.width() - 50
        txn_tree_height = self.height() - 150
        self.txnTree.setGeometry(txn_tree_x, txn_tree_y, txn_tree_width, txn_tree_height)
        self.txnTree.itemClicked.connect(self.on_txn_tree_item_clicked)

        table_headers = ['Date', 'Description', 'Amount', 'Major Category', 'Minor Category', 'Income Class']
        self.txnTree.setHeaderLabels(table_headers)

    def on_txn_tree_item_clicked(self, item, column):
        self.txnEditor.Edit(item)
        self.txnEditor.SetCategories(self.categoryParser, item.task.majorCat, item.task.minorCat, item.task.incomeCat)

    def on_viewButton_clicked(self):
        self.viewDialog = ViewDialog(self)
        self.viewDialog.show()

    def on_view_changed (self, startDate, endDate, incomeType):
        self.currIncomeType = incomeType
        self.startDate = startDate
        self.endDate = endDate
        self.startDateLabel.setText('Start: ' + startDate.toString())
        self.endDateLabel.setText('End: ' + endDate.toString())
        self.db.LoadView(startDate, endDate, incomeType)
        self.display_summary_view()

    def start_close(self):
        self.db.Close()
        self.close()

    def open_file(self):
        fileName = QFileDialog.getOpenFileName(
            self,
            "Open Statement",
            "/home/steve",
            "CSV files (*.csv)"
        )
        self.txnTree.clear()
        self.txnParser = BOAParser()
        self.txnParser.Parse(fileName)

        for txn in self.txnParser.transactions:
            self.db.FindTxn(txn)
            item = QtGui.QTreeWidgetItem([txn.date, txn.desc, txn.amount, txn.majorCat, txn.minorCat, txn.incomeCat])
            item.task = txn
            self.txnTree.addTopLevelItem(item)

    def open_amex_file(self):
        fileName = QFileDialog.getOpenFileName(
            self,
            "Open Statement",
            "/home/steve",
            "CSV files (*.csv)"
        )
        self.txnTree.clear()
        self.txnParser = AMEXParser()
        self.txnParser.Parse(fileName)

        for txn in self.txnParser.transactions:
            self.db.FindTxn(txn)
            item = QtGui.QTreeWidgetItem([txn.date, txn.desc, txn.amount, txn.majorCat, txn.minorCat, txn.incomeCat])
            item.task = txn
            self.txnTree.addTopLevelItem(item)

    def open_bbva_file(self):
        fileName = QFileDialog.getOpenFileName(
            self,
            "Open Statement",
            "/home/steve",
            "CSV files (*.csv)"
        )
        self.txnTree.clear()
        self.txnParser = BBVAParser()
        self.txnParser.Parse(fileName)

        for txn in self.txnParser.transactions:
            self.db.FindTxn(txn)
            item = QtGui.QTreeWidgetItem([txn.date, txn.desc, txn.amount, txn.majorCat, txn.minorCat, txn.incomeCat])
            item.task = txn
            self.txnTree.addTopLevelItem(item)

    def open_boavisa_file(self):
        fileName = QFileDialog.getOpenFileName(
            self,
            "Open Statement",
            "/home/steve",
            "CSV files (*.csv)"
        )
        self.txnTree.clear()
        self.txnParser = BOAVisaParser()
        self.txnParser.Parse(fileName)

        for txn in self.txnParser.transactions:
            self.db.FindTxn(txn)
            item = QtGui.QTreeWidgetItem([txn.date, txn.desc, txn.amount, txn.majorCat, txn.minorCat, txn.incomeCat])
            item.task = txn
            self.txnTree.addTopLevelItem(item)

    def reload_categories(self):
        self.categoryParser.parse(g_categoriesFile)
        # revalidate current entries
            # highlight incorrect entries

    def reload_classifiers(self):
        self.txnClassifier.Parse(g_classifiersFile)
        # classify current entries

    def autoClassify(self):
        iter = QTreeWidgetItemIterator(self.txnTree)
        while iter.value():
            if iter.value().task.majorCat is None and iter.value().task.minorCat is None:
                print('Classify attempt on ', iter.value().task.desc.encode('utf-8'))
                print('Classify result: ', self.txnClassifier.classify(iter.value().task))
                if (self.txnClassifier.classify(iter.value().task)):
                    iter.value().setText(3, iter.value().task.majorCat)
                    iter.value().setText(4, iter.value().task.minorCat)

            iter += 1

    def saveTxns(self):
        iter = QTreeWidgetItemIterator(self.txnTree)
        while iter.value():
            if iter.value().task.majorCat is not None and iter.value().task.minorCat is not None:
                try:
                    self.categoryParser.majorCategories.index(iter.value().task.majorCat)
                    self.categoryParser.minorCategories.index(iter.value().task.minorCat)
                    self.db.SaveTxn(iter.value().task)
                except ValueError as e:
                    print("Invalid category submitted! ")
            iter += 1
        if self.startDate is None:
            self.db.LoadFullView()
        else:
            self.db.LoadView(self.startDate, self.endDate, self.currIncomeType)
        self.display_summary_view()

    def exportCurrView (self):
        path = QtGui.QFileDialog.getSaveFileName(None, u"????????? ???????", "", ".csv(*.csv)")
        #if not path.isEmpty():
        with open(path, 'w', newline='', encoding='utf8') as stream:
            writer = csv.writer(stream, dialect='excel')
            for row in range(self.summaryTable.rowCount()):
                rowdata = []
                for column in range(self.summaryTable.columnCount()):
                    item = self.summaryTable.item(row, column)
                    if item is not None:
                        rowdata.append(item.text())
                    else:
                        rowdata.append('')
                writer.writerow(rowdata)

    def exportYearView (self):
        path = QtGui.QFileDialog.getSaveFileName(None, u"????????? ???????", "", ".csv(*.csv)")

        with open(path, 'w', newline='', encoding='utf8') as stream:
            writer = csv.writer(stream, dialect='excel')
            txns = self.db.GetTxns(self.startDate, self.endDate, self.currIncomeType)
            yearView = SummaryView()

            for txn in txns:
                d = datetime.datetime.strptime(txn.date, '%Y-%m-%d').date()
                yearView.Update(txn.majorCat, str(d.month), txn.amount)

            #write header row
            writer.writerow(['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
            #write all months
            for category in yearView.categories:
                rowdata = []
                rowdata.append(category)
                for month in range(1,12):
                    if str(month) in yearView.categories[category]:
                        rowdata.append(yearView.categories[category][str(month)])
                    else:
                        rowdata.append('')
                writer.writerow(rowdata)
            #write net row
            rowdata = []
            rowdata.append('Net')
            for column in range(ord('B'), ord('B')+12):
                columnName = chr(column)
                netStr = '=' + columnName + '2'
                for row in range(3,len(yearView.categories)+2):
                    netStr += '+'+columnName+str(row)
                rowdata.append(netStr)
            writer.writerow(rowdata)

def main():
    a = QApplication(sys.argv)
    w = MainWindow()

    #categories = CategoryParser()
    #categories.Parse(g_categoriesFile)

    parser = BOAParser()

    t = QTableWidget(1, 3)

    sys.exit(a.exec_())

main()




