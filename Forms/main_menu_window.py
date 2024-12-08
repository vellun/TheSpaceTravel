# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_menu_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(740, 780)
        MainWindow.setMinimumSize(QtCore.QSize(740, 780))
        MainWindow.setMaximumSize(QtCore.QSize(740, 780))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/иконка2.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-image: url(Images/фон_меню.jpg);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.new_game = QtWidgets.QPushButton(self.centralwidget)
        self.new_game.setGeometry(QtCore.QRect(420, 520, 201, 61))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.new_game.setFont(font)
        self.new_game.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.new_game.setStyleSheet("color: rgb(159, 163, 127);\n"
"QPushButton::pressed\n"
"{\n"
"background-color: rgb(255, 217, 198);\n"
"}")
        self.new_game.setObjectName("new_game")
        self.continue_2 = QtWidgets.QPushButton(self.centralwidget)
        self.continue_2.setGeometry(QtCore.QRect(120, 520, 201, 61))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.continue_2.setFont(font)
        self.continue_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.continue_2.setStyleSheet("color: rgb(184, 184, 184);")
        self.continue_2.setObjectName("continue_2")
        self.ends = QtWidgets.QPushButton(self.centralwidget)
        self.ends.setGeometry(QtCore.QRect(250, 620, 231, 61))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.ends.setFont(font)
        self.ends.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ends.setStyleSheet("color: rgb(184, 184, 184);")
        self.ends.setObjectName("ends")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 740, 35))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.menubar.setFont(font)
        self.menubar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.menubar.setStyleSheet("color: rgb(184, 184, 184);")
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setGeometry(QtCore.QRect(543, 200, 347, 213))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.menu.setFont(font)
        self.menu.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.menu.setStyleSheet("color: rgb(184, 184, 184);")
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.users = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.users.setFont(font)
        self.users.setShortcutContext(QtCore.Qt.WidgetShortcut)
        self.users.setObjectName("users")
        self.about_game = QtWidgets.QAction(MainWindow)
        self.about_game.setObjectName("about_game")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.close_game = QtWidgets.QAction(MainWindow)
        self.close_game.setObjectName("close_game")
        self.menu.addAction(self.about_game)
        self.menu.addAction(self.action)
        self.menu.addAction(self.users)
        self.menu.addSeparator()
        self.menu.addAction(self.close_game)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Главное меню"))
        self.new_game.setText(_translate("MainWindow", "Новая игра"))
        self.new_game.setShortcut(_translate("MainWindow", "Return"))
        self.continue_2.setText(_translate("MainWindow", "Продолжить"))
        self.ends.setText(_translate("MainWindow", "Галерея концовок"))
        self.menu.setTitle(_translate("MainWindow", "Помощь"))
        self.users.setText(_translate("MainWindow", "История пользователей"))
        self.about_game.setText(_translate("MainWindow", "Об игре"))
        self.about_game.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.action.setText(_translate("MainWindow", "Руководство к игре"))
        self.close_game.setText(_translate("MainWindow", "Выйти из игры"))
