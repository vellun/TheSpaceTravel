# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'users_story.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(750, 471)
        Form.setStyleSheet("color: rgb(53, 53, 53);")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(0, 0, 753, 471))
        self.widget.setMinimumSize(QtCore.QSize(753, 471))
        self.widget.setMaximumSize(QtCore.QSize(753, 471))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/иконка2.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.widget.setStyleSheet("background-image: url(Images/1.jpg);")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(280, 10, 211, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setStyleSheet("\n"
"color: rgb(217, 217, 217);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(260, 180, 281, 61))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(211, 211, 211);")
        self.label_2.setObjectName("label_2")
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 50, 711, 331))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        self.tableWidget.setFont(font)
        self.tableWidget.setAutoFillBackground(True)
        self.tableWidget.setStyleSheet("background-image: url(Images/1.jpg);\n"
"color: rgb(218, 218, 218);")
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        item.setFont(font)
        item.setBackground(QtGui.QColor(27, 34, 40))
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        item.setFont(font)
        item.setBackground(QtGui.QColor(27, 34, 40))
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        item.setFont(font)
        item.setBackground(QtGui.QColor(27, 34, 40))
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        item.setFont(font)
        item.setBackground(QtGui.QColor(27, 34, 40))
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(170)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(9)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.close_btn = QtWidgets.QPushButton(self.widget)
        self.close_btn.setGeometry(QtCore.QRect(580, 400, 151, 51))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        self.close_btn.setFont(font)
        self.close_btn.setStyleSheet("color: rgb(180, 180, 180);")
        self.close_btn.setObjectName("close_btn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "История пользователей"))
        self.label.setText(_translate("Form", "История игроков"))
        self.label_2.setText(_translate("Form", "Список игроков пуст."))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Пользователь"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Имя"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Пол"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Дата"))
        self.close_btn.setText(_translate("Form", "Закрыть"))
        self.close_btn.setShortcut(_translate("Form", "Return"))
