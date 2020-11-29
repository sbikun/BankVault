# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewDialog.ui'
#
# Created: Thu Jun 20 19:33:48 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ViewDialog(object):
    def setupUi(self, ViewDialog):
        ViewDialog.setObjectName(_fromUtf8("ViewDialog"))
        ViewDialog.resize(647, 300)
        self.buttonBox = QtGui.QDialogButtonBox(ViewDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.calendarWidget = QtGui.QCalendarWidget(ViewDialog)
        self.calendarWidget.setGeometry(QtCore.QRect(20, 40, 256, 155))
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))
        self.calendarWidget_2 = QtGui.QCalendarWidget(ViewDialog)
        self.calendarWidget_2.setGeometry(QtCore.QRect(330, 40, 256, 155))
        self.calendarWidget_2.setObjectName(_fromUtf8("calendarWidget_2"))
        self.label = QtGui.QLabel(ViewDialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(ViewDialog)
        self.label_2.setGeometry(QtCore.QRect(330, 20, 46, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_incomeType = QtGui.QLabel(ViewDialog)
        self.label_incomeType.setGeometry(QtCore.QRect(30, 220, 71, 21))
        self.label_incomeType.setObjectName(_fromUtf8("label_incomeType"))
        self.comboBox = QtGui.QComboBox(ViewDialog)
        self.comboBox.setGeometry(QtCore.QRect(100, 220, 69, 22))
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))

        self.retranslateUi(ViewDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ViewDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ViewDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ViewDialog)

    def retranslateUi(self, ViewDialog):
        ViewDialog.setWindowTitle(_translate("ViewDialog", "Dialog", None))
        self.label.setText(_translate("ViewDialog", "Start Date", None))
        self.label_2.setText(_translate("ViewDialog", "End Date", None))
        self.label_incomeType.setText(_translate("ViewDialog", "Income Type:", None))
        self.comboBox.setItemText(0, _translate("ViewDialog", "Monthly", None))
        self.comboBox.setItemText(1, _translate("ViewDialog", "Yearly", None))
        self.comboBox.setItemText(2, _translate("ViewDialog", "Bonus", None))

