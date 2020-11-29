# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editor.ui'
#
# Created: Mon Jun  3 09:00:47 2013
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

class Ui_TxnEditWidget(object):
    def setupUi(self, TxnEditWidget):
        TxnEditWidget.setObjectName(_fromUtf8("TxnEditWidget"))
        TxnEditWidget.resize(790, 117)
        self.labelDate = QtGui.QLabel(TxnEditWidget)
        self.labelDate.setGeometry(QtCore.QRect(10, 40, 46, 13))
        self.labelDate.setObjectName(_fromUtf8("labelDate"))
        self.labelPrice = QtGui.QLabel(TxnEditWidget)
        self.labelPrice.setGeometry(QtCore.QRect(90, 40, 46, 13))
        self.labelPrice.setObjectName(_fromUtf8("labelPrice"))
        self.labelDesc = QtGui.QLabel(TxnEditWidget)
        self.labelDesc.setGeometry(QtCore.QRect(10, 10, 651, 16))
        self.labelDesc.setObjectName(_fromUtf8("labelDesc"))
        self.comboMajorCats = QtGui.QComboBox(TxnEditWidget)
        self.comboMajorCats.setGeometry(QtCore.QRect(10, 70, 91, 22))
        self.comboMajorCats.setObjectName(_fromUtf8("comboMajorCats"))
        self.comboMinorCats = QtGui.QComboBox(TxnEditWidget)
        self.comboMinorCats.setGeometry(QtCore.QRect(140, 70, 161, 22))
        self.comboMinorCats.setObjectName(_fromUtf8("comboMinorCats"))
        self.comboIncomeCat = QtGui.QComboBox(TxnEditWidget)
        self.comboIncomeCat.setGeometry(QtCore.QRect(340, 70, 91, 22))
        self.comboIncomeCat.setObjectName(_fromUtf8("comboIncomeCat"))
        self.buttonSave = QtGui.QPushButton(TxnEditWidget)
        self.buttonSave.setGeometry(QtCore.QRect(460, 70, 75, 23))
        self.buttonSave.setObjectName(_fromUtf8("buttonSave"))

        self.retranslateUi(TxnEditWidget)
        QtCore.QMetaObject.connectSlotsByName(TxnEditWidget)

    def retranslateUi(self, TxnEditWidget):
        TxnEditWidget.setWindowTitle(_translate("TxnEditWidget", "Editor", None))
        self.labelDate.setText(_translate("TxnEditWidget", "Date", None))
        self.labelPrice.setText(_translate("TxnEditWidget", "Amount", None))
        self.labelDesc.setText(_translate("TxnEditWidget", "Description", None))
        self.buttonSave.setText(_translate("TxnEditWidget", "Save", None))

