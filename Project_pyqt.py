import csv
import sqlite3
import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QWidget, QTableWidgetItem, QFileDialog, \
    QPushButton
from PyQt5.QtCore import Qt, QEventLoop, QTimer
import datetime
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

from Forms import main_menu_window, game_window2, choose_music, about_game, sound_tool, \
    users_story, question1, question2, enter_name, birthday_date, inventary_form, show_inventary, info_about_planets, \
    account_of_travel, item_form, short_message, ends_gallery, info_about_ends, game_guide, loading
from PyQt5 import QtCore, QtGui

inventory = []
inventory_flag = False


class Game(QMainWindow, game_window2.Ui_MainWindow):
    def __init__(self, answer=None, end=None):
        super().__init__()
        self.setupUi(self)

        self.answer, self.end = answer, end
        self.invent_btn.clicked.connect(self.collect_inventory)
        self.invent_btn.hide()
        self.ques.clicked.connect(self.show_guide)
        for i in (self.pushButton, self.pushButton_2, self.pushButton_3):
            i.clicked.connect(self.show_planets_file)
        self.inventory_btn.clicked.connect(self.show_inventory)
        self.exit.clicked.connect(self.menu_exit)
        for i in (self.then, self.then_2, self.then_3):
            i.clicked.connect(self.next_action)
        self.action.triggered.connect(self.tool_snd)
        self.action_2.triggered.connect(self.choose_music)
        self.first = True
        for i in (self.then_2, self.then_3, self.groupBox, self.help_label, self.inventory_btn):
            i.hide()
        self.connection = sqlite3.connect('Data/Game_database.sqlite')
        self.answers = []
        self.playAudio()
        self.next_action()

    def next_action(self):
        global inventory_flag
        if isinstance(self.sender(), QPushButton) and self.sender().text() == 'Готово' and not inventory:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText('Сначала соберите инвентарь.')
            msg_box.setWindowTitle('Без вещей нельзя')
            self.set_icon(msg_box)
            msg_box.show()
            msg_box.exec()
            return
        self.cursor = self.connection.cursor()
        self.answ = self.sender().text() if not self.first else 'first'

        if not self.answer:
            self.result = self.cursor.execute(
                """ SELECT action, button, answer, inventoryItem FROM game WHERE answer = ? """,
                (self.answ,)).fetchall()
            self.first = False
            if self.result[0][2] == 'first':
                inventory.clear()
                inventory_flag = False
        else:
            if not self.end:
                self.result = self.cursor.execute(
                    """ SELECT action, button, answer, inventoryItem FROM game WHERE button = ? """,
                    (self.answer,)).fetchone()
            else:
                self.result = self.cursor.execute(
                    """ SELECT action, button, answer, inventoryItem FROM game WHERE button = ? AND end_name = ?""",
                    (self.answer, self.end)).fetchone()
                self.result += ('flag',)

            if inventory:
                self.inventory_btn.show()
            self.first, self.answer = False, None
        self.answers.append(self.result[0][2])

        if self.result[0][2] == 'В главное меню':
            self.main = MainMenu()
            self.main.show()
            self.close()
            return

        if type(self.result[0][3]) == int:
            self.item = self.cursor.execute(f""" SELECT itemName FROM inventory WHERE id = 
                          (SELECT inventoryItem FROM game WHERE answer = '{self.result[0][2]}') """).fetchone()[0]

        if len(self.result) == 2:
            if inventory_flag:
                self.result = self.result[0]
            else:
                self.result = self.result[1]
        elif len(self.result) == 1:
            self.result = self.result[0]
        background = self.cursor.execute(f""" SELECT pictureName FROM backgrounds WHERE id =
                            (SELECT background FROM game WHERE answer = '{self.result[2]}')""").fetchone()
        if background:
            self.setStyleSheet(f"""background-image: url(Images/{background[0]});""")
            for i in (self.then, self.then_2, self.then_3, self.inventory_btn):
                i.setStyleSheet(f"""background-image: url(Images/{background[0]}); color: rgb(190, 190, 190);""")

        if 'Забрать' in self.answ or self.answ == 'Взять':
            if len(inventory) == 4:
                msg_box = QMessageBox()
                msg_box.setWindowTitle('Нехватка места')
                msg_box.setText('В инвентаре 4 места. Чтобы добавить новый предмет, что-нибудь уберите.')
                self.set_icon(msg_box)
                msg_box.show()
                msg_box.exec()
                return
            else:
                inventory.append('Передающее устройство')

        if self.result[2] == 'Взять образец':
            inventory_flag = True

        if 'Использовать' in self.answ:
            if not inventory_flag:
                if self.item not in inventory:
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle('Нет предмета')
                    msg_box.setText(f'К сожалению, вы не взяли с собой {self.item.lower()}.')
                    self.set_icon(msg_box)
                    msg_box.show()
                    msg_box.exec()
                else:
                    self.result = list(self.result)
                    self.result[2] = self.answers[-2]
                    self.inv_obj = ShowInventory(self.result[2])
                    self.inv_obj.show()
                    del self.answers[-1]
                return

        self.plainTextEdit.clear()
        text = self.result[0]
        if '{name}' in text:
            name = self.cursor.execute(""" SELECT Name FROM users """).fetchall()[-1][0]
            ind = text.index('{')
            text = list(text[:text.index('{')] + text[text.index('}') + 1:])
            text.insert(ind, name)
            text = ''.join(text)

        if self.result[2] == 'Идти':
            self.help_label.show()
            self.help_label.setStyleSheet(f"""background-image: url(Images/планета1); 
                                                 color: rgb(190, 190, 190);""")
        else:
            self.help_label.hide()

        self.invent_btn.show() if 'инвентарь' in text else self.invent_btn.hide()

        if self.result[1] == 'На Планету1':
            self.groupBox.show()
        else:
            self.groupBox.hide()

        if ';' in self.result[1]:
            buttons = self.result[1].split('; ')
            btns = [self.then_2, self.then_3]
            for i in range(len(btns)):
                btns[i].setText(buttons[i])
                btns[i].show()
                if btns[i].text() == 'Отчет о путешествии':
                    btns[i].disconnect()
                    btns[i].clicked.connect(self.show_travels_file)
            self.then.hide()
        else:
            self.then.setText(self.result[1])
            self.then.show()
            for i in (self.then_2, self.then_3, self.help_label):
                i.hide()

        for i in (self.then, self.then_2, self.then_3):
            i.setFont(QFont('MS Sans Serif', 17))
            i.resize(i.sizeHint())
            i.setFont(QFont('MS Sans Serif', 14))

        end = self.cursor.execute(f""" SELECT end_name FROM game WHERE answer = '{self.result[2]}' """).fetchall()[0]
        user = self.cursor.execute(""" SELECT name, nickname FROM users  """).fetchall()[-1]
        if end[0] and 'flag' not in self.result:
            self.cursor.execute(f""" UPDATE ends SET user_nickname = '{user[1]}' WHERE id = {end[0]}""")
            self.connection.commit()

        self.get_sound()

        self.plainTextEdit.setPlainText(text)
        if self.result[3] and type(self.result[3]) == int:
            inventory_flag = False

    def show_travels_file(self):
        ending = self.cursor.execute(f""" SELECT end_name FROM ends WHERE id = 
                                      (SELECT end_name FROM game WHERE answer = '{self.result[2]}')""").fetchone()[0]
        with open('Data/accounts_of_travels.csv', 'r', encoding="utf8") as file:
            reader = csv.DictReader(file, delimiter=';')
            flag = 'True' if 'Передающее устройство' in inventory else 'False'
            for i in reader:
                if i['ending'] == ending and i['inventory_status'] == flag:
                    items = [i['title'], i['survivor'], i['isl'], i['text']]
                    break
        self.travel = TravelInfo(items)
        self.travel.setWindowModality(Qt.ApplicationModal)
        self.travel.show()

    def get_sound(self):
        sound = self.cursor.execute(f""" SELECT sound_name FROM sounds WHERE id =
                                    (SELECT soundId FROM game WHERE answer = '{self.result[2]}')""").fetchone()
        if sound:
            self.radio = QMediaPlayer()
            if sound[0] == 'Напряженная музыка':
                self.playAudio(sound[0])
            elif sound[0] == 'По умолчанию':
                self.playAudio()
            else:
                self.radio = QMediaPlayer()
                url = QUrl.fromLocalFile(f'Sounds/{sound[0]}')
                content = QMediaContent(url)
                self.radio.setMedia(content)
                if sound[0] == 'ship_sound.mp3':
                    self.playAudio()
                self.radio.play()
        if hasattr(self, 'radio') and self.result[1] == '-->':
            self.radio.setMuted(not self.radio.isMuted())

    def collect_inventory(self):
        self.obj = Inventory(self)
        self.obj.setWindowModality(Qt.ApplicationModal)
        self.obj.show()

    def show_inventory(self):
        self.inv = ShowInventory(self.result[2])
        self.inv.show()

    def show_guide(self):
        self.a = GameGuide()
        self.a.setWindowModality(Qt.ApplicationModal)
        self.a.show()

    def show_planets_file(self):
        with open('Data/planets_info.csv', 'r', encoding="utf8") as file:
            reader = csv.DictReader(file, delimiter=';')
            for i in reader:
                if i['name'] == self.sender().text():
                    text, title = i['info'], i['title']
                    break
        self.pl = PlanetsInfo(text, title)
        self.pl.setWindowModality(Qt.ApplicationModal)
        self.pl.show()

    def menu_exit(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText('Выйти в главное меню?')
        msg_box.setInformativeText('Сохранить игру?')
        msg_box.addButton('Сохранить', QMessageBox.YesRole)
        msg_box.addButton('Не сохранять', QMessageBox.NoRole)
        msg_box.addButton('Отмена', QMessageBox.NoRole)
        msg_box.setWindowTitle('Выход')
        self.set_icon(msg_box)

        msg_box.buttonClicked.connect(self.popup)
        msg_box.show()
        msg_box.exec()

    def popup(self, btn):
        if btn.text() == 'Сохранить':
            nickname = self.cursor.execute(""" SELECT name, nickname FROM users """).fetchall()[-1][1]
            self.cursor.execute(""" UPDATE users SET last_answer = ? 
                                  WHERE nickname = ?""", (self.result[1], nickname))
            self.connection.commit()
        if btn.text() != 'Отмена':
            self.close()
            self.w = MainMenu()
            self.w.show()

    def playAudio(self, audio='Спокойная музыка (по умолчанию)'):
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        if ':/' not in audio:
            url = QUrl.fromLocalFile(f'Sounds/{audio}.mp3')
        else:
            url = QUrl.fromLocalFile(audio)
        self.playlist.addMedia(QMediaContent(url))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.player.setPlaylist(self.playlist)
        if audio == 'Напряженная музыка':
            self.player.setVolume(40)
        elif audio != 'Спокойная музыка (по умолчанию)':
            self.player.setVolume(20)
        self.player.play()

    def set_volume(self, volume):
        self.player.setVolume(volume)

    def tool_snd(self):
        volume = self.player.volume()
        tool = SoundTool(volume, self.set_volume)
        tool.show()
        tool.exec()

    def choose_music(self):
        self.w = ChooseMusic(self.playAudio)
        self.w.show()

    def set_icon(self, obj):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/иконка2.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        obj.setWindowIcon(icon)

    def closeEvent(self, event):
        self.player.setMuted(not self.player.isMuted())
        if hasattr(self, 'radio'):
            self.radio.setMuted(True)
        self.connection.close()


class ChooseMusic(QWidget, choose_music.Ui_Form):
    def __init__(self, func):
        super().__init__()
        self.setupUi(self)
        self.func = func

        self.ok.clicked.connect(self.choose)
        self.ok.clicked.connect(self.close)
        self.cansel.clicked.connect(self.close)
        self.your_music.clicked.connect(self.users_music)

    def choose(self):
        if self.listWidget.selectedItems():
            self.func(self.listWidget.currentItem().text().strip())

    def users_music(self):
        file = QFileDialog.getOpenFileName(self, 'Выбрать музыку', '', '*.mp3')[0]
        if file:
            self.func(file)


class PlanetsInfo(QWidget, info_about_planets.Ui_Form):
    def __init__(self, text, title):
        super().__init__()
        self.setupUi(self)
        self.close_btn.clicked.connect(self.close)
        text = title + '\n' + '' + '\n' + text

        self.textEdit.setText(text)
        self.textEdit.setAlignment(QtCore.Qt.AlignCenter)


class TravelInfo(QWidget, account_of_travel.Ui_Form):
    def __init__(self, items):
        super().__init__()
        self.setupUi(self)
        self.closeb.clicked.connect(self.close)
        text = items[0] + '\n' + items[1] + '\n' + items[2] + '\n' + '' + '\n' + items[3]

        self.textEdit.setText(text)
        self.textEdit.setAlignment(QtCore.Qt.AlignCenter)


class Inventory(QWidget, inventary_form.Ui_Form):
    def __init__(self, obj):
        super().__init__()
        self.setupUi(self)

        self.obj = obj
        for i in range(self.gridLayout_2.count()):
            item = self.gridLayout_2.itemAt(i).widget()
            item.clicked.connect(self.run)
            if item.text() in inventory:
                item.setChecked(True)
            self.ok.clicked.connect(self.show_btn)
            self.ok.clicked.connect(self.close)
        if inventory:
            for i in inventory:
                self.invent_list.addItem(i)

    def run(self):
        if self.sender().isChecked():
            if len(inventory) == 4:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle('Что-то лишнее')
                msg_box.setText('В инвентаре 4 места.')
                msg_box.show()
                msg_box.exec()
                self.sender().setChecked(False)
                return
            self.invent_list.addItem(self.sender().text())
            inventory.append(self.sender().text())
        else:
            item = self.invent_list.takeItem(inventory.index(self.sender().text()))
            del inventory[inventory.index(self.sender().text())]
            del item

    def show_btn(self):
        if inventory:
            self.obj.inventory_btn.show()


class ShowInventory(QWidget, show_inventary.Ui_Form):
    def __init__(self, answ):
        super().__init__()
        self.setupUi(self)

        self.connect = sqlite3.connect("Data/Game_database.sqlite")
        self.answ = answ
        self.invent_list.itemDoubleClicked.connect(self.show_inv)
        for i in inventory:
            self.invent_list.addItem(i)

    def show_inv(self):
        self.obj = InvItem(self)
        cur = self.connect.cursor()
        self.item = cur.execute(f""" SELECT itemName FROM inventory WHERE id = 
                      (SELECT inventoryItem FROM game WHERE answer = '{self.answ}') """).fetchone()
        self.obj.name.setText(self.sender().currentItem().text())
        self.obj.name.setAlignment(Qt.AlignCenter)
        if self.item and self.item[0] == self.obj.name.text():
            self.obj.use.setEnabled(True)
        else:
            self.obj.use.setEnabled(False)
        self.obj.show()

    def closeEvent(self, event):
        self.connect.close()


class InvItem(QWidget, item_form.Ui_Form):
    def __init__(self, obj, answ=None):
        super().__init__()
        self.setupUi(self)

        self.obj, self.answ = obj, answ
        self.delete_2.clicked.connect(self.del_item)
        self.use.clicked.connect(self.use_item)
        self.connect = sqlite3.connect('Data/Game_database.sqlite')

    def del_item(self):
        item = self.obj.invent_list.takeItem(inventory.index(self.name.text()))
        del inventory[inventory.index(self.name.text())]
        del item
        self.obj.invent_list.clearSelection()
        self.close()

    def use_item(self):
        global inventory_flag
        cur = self.connect
        if not self.answ:
            text = cur.execute(f""" SELECT text FROM inventory WHERE id =  
                         (SELECT inventoryItem FROM game WHERE answer = '{self.obj.answ}')""").fetchone()
        else:
            text = cur.execute(f""" SELECT text FROM inventory WHERE id =  
                                     (SELECT inventoryItem FROM game WHERE answer = '{self.answ}')""").fetchone()

        self.close()
        self.obj.close()

        self.msg = ShortMessage()
        self.msg.label.setText(text[0])
        self.msg.show()
        loop = QEventLoop()
        QTimer.singleShot(1500, loop.quit)
        loop.exec_()
        self.msg.close()

        inventory_flag = True

    def closeEvent(self, event):
        self.connect.close()


class ShortMessage(QDialog, short_message.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Loading(QWidget, loading.Ui_Loading):
    def __init__(self, answ=None):
        super().__init__()
        self.setupUi(self)
        self.answ = answ
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.counter = 0
        self.run()

    def run(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(35)

    def progress(self):
        self.progressBar.setValue(self.counter)
        self.counter += 1

        if self.counter > 100:
            self.timer.stop()
            self.game = Game(self.answ) if self.answ else Game()

            self.close()
            self.game.show()


class MainMenu(QMainWindow, main_menu_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.about_game.triggered.connect(self.info_about_game)
        self.new_game.clicked.connect(self.input)
        self.users.triggered.connect(self.show_players)
        self.users.triggered.connect(self.show_players)
        self.close_game.triggered.connect(self.close)
        self.continue_2.clicked.connect(self.continue_game)
        self.ends.clicked.connect(self.gallery_ends)
        self.action.triggered.connect(self.show_guide)
        self.connect = sqlite3.connect('Data/Game_database.sqlite')
        self.first_game = True
        self.playAudio()

        self.play = QMediaPlayer()
        url = QUrl.fromLocalFile('Sounds/звук кнопка.mp3')
        content = QMediaContent(url)
        self.play.setMedia(content)

    def playAudio(self):
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        url = QUrl.fromLocalFile('Sounds/меню аудио.mp3')
        self.playlist.addMedia(QMediaContent(url))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.player.setPlaylist(self.playlist)
        self.player.play()

    def gallery_ends(self):
        self.play.play()
        self.obj = EndsGallery(self)
        self.obj.show()

    def info_about_game(self):
        self.play.play()
        a = InfoAboutGame(self.play)
        a.setWindowModality(Qt.ApplicationModal)
        a.show()
        a.exec()

    def show_guide(self):
        self.play.play()
        self.a = GameGuide(self.play)
        self.a.setWindowModality(Qt.ApplicationModal)
        self.a.show()

    def input(self):
        self.play.play()
        cursor = self.connect.cursor()
        self.res = cursor.execute(""" SELECT Name, Nickname, last_answer FROM users """).fetchall()
        if self.res:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setWindowTitle('Продолжить игру')
            msg_box.setText(f'Пройти игру с игроком {self.res[-1][1]} ещё раз?')
            msg_box.setInformativeText('Вы можете ещё раз пройти игру с текущим пользователем или сменить его. '
                                       'Вернуться к предыдущему пользователю невозможно.')
            msg_box.addButton('Сменить пользователя', QMessageBox.YesRole)
            msg_box.addButton('Продолжить', QMessageBox.YesRole)
            msg_box.addButton('Отмена', QMessageBox.NoRole)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("Images/иконка2.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            msg_box.setWindowIcon(icon)
            msg_box.buttonClicked.connect(self.popup2)
            msg_box.show()
            msg_box.exec()
        else:
            self.a = InputName(self.play, self)
            self.a.setWindowModality(Qt.ApplicationModal)
            self.a.show()

    def popup2(self, btn):
        if btn.text() == 'Сменить пользователя':
            self.a = InputName(self.play, self)
            self.a.setWindowModality(Qt.ApplicationModal)
            self.a.show()
        elif btn.text() == 'Продолжить':
            if self.res[-1][2]:
                cursor = self.connect.cursor()
                cursor.execute(f""" UPDATE users SET last_answer = NULL 
                                        WHERE Nickname = '{self.res[-1][1]}'""")
                self.connect.commit()
            self.load = Loading()
            self.load.show()
            self.close()

    def show_players(self):
        self.play.play()
        self.pl = TableOfPlayers(self.play)
        self.pl.show()

    def continue_game(self):
        self.play.play()
        self.cursor = self.connect.cursor()
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle('Нечего продолжать')
        msg_box.setText('Вы ещё не сохраняли игру')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/иконка2.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msg_box.setWindowIcon(icon)

        try:
            inf = self.cursor.execute(""" SELECT name, nickname, last_answer FROM users """).fetchall()[-1]
            if not inf[2]:
                msg_box.show()
                msg_box.exec()
            else:
                self.answ = inf[2]
                msg_box.setIcon(QMessageBox.Question)
                msg_box.setWindowTitle('Продолжить игру')
                msg_box.setText(f'Продолжить игру с игроком {inf[1]}?')
                msg_box.setInformativeText('У вас есть сохраненная игра')
                msg_box.addButton('Продолжить', QMessageBox.YesRole)
                msg_box.addButton('Отмена', QMessageBox.NoRole)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("Images/иконка2.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                msg_box.setWindowIcon(icon)
                msg_box.buttonClicked.connect(self.popup)

                msg_box.show()
                msg_box.exec()
        except:
            msg_box.show()
            msg_box.exec()

    def popup(self, btn):
        if btn.text() == 'Продолжить':
            self.load = Loading(self.answ)
            self.close()
            self.load.show()

    def closeEvent(self, event):
        self.player.setMuted(not self.player.isMuted())
        self.connect.close()


class EndsGallery(QWidget, ends_gallery.Ui_Form):
    def __init__(self, menu_obj):
        super().__init__()
        self.setupUi(self)
        self.cansel.clicked.connect(self.close)
        self.menu_obj = menu_obj
        self.connect = sqlite3.connect('Data/Game_database.sqlite')
        for btn in self.buttonGroup.buttons():
            btn.clicked.connect(self.show_end)
        self.get_enabled()

    def get_enabled(self):
        cur = self.connect.cursor()
        user = cur.execute(""" SELECT nickname, name FROM users """).fetchall()
        if user:
            user = user[-1]
            ends = cur.execute(f""" SELECT end_name FROM ends WHERE user_nickname = '{user[0]}' """).fetchall()
            ends = [i[0] for i in ends]
            btns = self.buttonGroup.buttons()
            for i in range(len(btns)):
                for j in ends:
                    if j in btns[i].text():
                        btns[i].setEnabled(True)
                        sp = list(btns[i].text())
                        sp.remove('🔒')
                        btns[i].setText(''.join(sp))

    def show_end(self):
        with open('Data/ends_info.csv', 'r', encoding="utf8") as file:
            reader = csv.DictReader(file, delimiter=';')
            for i in reader:
                if i['name'] in self.sender().text():
                    text, title, name = i['info'], i['title'], i['name']
                    break
        self.end = EndsInfo(text, title, name, self)
        self.end.setWindowModality(Qt.ApplicationModal)
        self.end.show()

    def closeEvent(self, event):
        self.connect.close()


class EndsInfo(QWidget, info_about_ends.Ui_Form):
    def __init__(self, text, title, name, obj):
        super().__init__()
        self.setupUi(self)
        self.name = name
        self.obj = obj
        self.close_.clicked.connect(self.close)
        self.go_to_end.clicked.connect(self.go)
        self.connect = sqlite3.connect('Data/Game_database.sqlite')
        text = title + '\n' + '\n' + text

        self.textEdit.setText(text)
        self.textEdit.setAlignment(QtCore.Qt.AlignCenter)

    def go(self):
        cur = self.connect.cursor()
        answ = cur.execute(f""" SELECT button, end_name FROM game WHERE end_name = 
                           (SELECT id FROM ends WHERE end_name = '{self.name}') """).fetchone()

        self.end = Game(answ[0], answ[1])
        self.end.show()
        self.close()
        self.obj.close()
        self.obj.menu_obj.close()

    def closeEvent(self, event):
        self.connect.close()


class SoundTool(QDialog, sound_tool.Ui_Dialog):
    def __init__(self, volume, func):
        super().__init__()
        self.setupUi(self)
        self.func = func
        self.ok.clicked.connect(self.close)
        self.slider.valueChanged.connect(self.run)
        self.slider.setMaximum(100)
        self.slider.setValue(volume)
        self.slider.setTickInterval(5)

    def run(self):
        self.func(self.slider.value())


class InfoAboutGame(QDialog, about_game.Ui_Dialog):
    def __init__(self, snd):
        super().__init__()
        self.setupUi(self)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.clicked.connect(snd.play)


class GameGuide(QWidget, game_guide.Ui_Form):
    def __init__(self, snd=None):
        super().__init__()
        self.setupUi(self)
        self.ok.clicked.connect(self.close)
        if snd:
            self.ok.clicked.connect(snd.play)


class TableOfPlayers(QWidget, users_story.Ui_Form):
    def __init__(self, snd):
        super().__init__()
        self.setupUi(self)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.clicked.connect(snd.play)
        self.tableWidget.hide()

        self.connection = sqlite3.connect('Data/Game_database.sqlite')
        self.complete_the_table()

    def complete_the_table(self):
        cursor = self.connection.cursor()
        result = cursor.execute(""" SELECT Nickname, Name, Gender, Game_date FROM users """).fetchall()
        if result:
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(result):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.show()


class InputName(QWidget, enter_name.Ui_Form):
    def __init__(self, snd, obj):
        super().__init__()
        self.setupUi(self)
        self.snd, self.obj = snd, obj
        self.cansel.clicked.connect(self.close)
        self.cansel.clicked.connect(self.snd.play)
        self.ques1.clicked.connect(self.quest1)
        self.ques2.clicked.connect(self.quest2)
        self.start.clicked.connect(self.start_click)
        self.date.clicked.connect(self.choose_date)
        d = [int(i) for i in self.date.text().split('.')]
        self.dt = datetime.date(d[0], d[1], d[2])
        self.snd = snd
        self.connection = sqlite3.connect('Data/Game_database.sqlite')
        self.first_game = True

    def choose_date(self):
        self.snd.play()
        self.date_ex = ChooseBthDay(self.snd)
        self.date_ex.show()
        self.date_ex.choose.clicked.connect(self.set_date)
        self.date_ex.choose.clicked.connect(self.snd.play)
        self.date_ex.exec()

    def set_date(self):
        dt = self.date_ex.calendarWidget.selectedDate()
        self.dt = datetime.date(dt.year(), dt.month(), dt.day())
        self.date.setText(f'{self.dt.year}-{self.dt.month}-{self.dt.day}')
        self.date_ex.close()

    def quest1(self):
        self.snd.play()
        a = Question1(self.snd)
        a.setWindowModality(Qt.ApplicationModal)
        a.show()
        a.exec()

    def quest2(self):
        self.snd.play()
        a = Question2(self.snd)
        a.setWindowModality(Qt.ApplicationModal)
        a.show()
        a.exec()

    def set_icon(self, obj):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/иконка2.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        obj.setWindowIcon(icon)

    def start_click(self):
        self.snd.play()
        now = datetime.date.today()
        name, nickname, gender = self.nm.text(), self.nknm.text(), self.comboBox.currentText()
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        self.set_icon(msg_box)
        f = False
        if not name:
            msg_box.setText('Введите имя')
        elif not nickname:
            msg_box.setText('Введите никнейм')
        elif self.dt.year >= now.year:
            msg_box.setText('Введена некорректная дата')
        else:
            f = True
        if not f:
            msg_box.setWindowTitle('Ошибка')
            msg_box.show()
            msg_box.exec()
            return
        else:
            self.first_game = False
            try:
                cursor = self.connection.cursor()
                # 'Внесение в базу данных пользователя'
                cursor.execute(""" INSERT INTO users (Nickname, Name, Gender, Game_date, Bth_date)
                                VALUES (?, ?, ?, ?, ?)""", (nickname, name, gender, datetime.date.today(),
                                                            (datetime.date(self.dt.year, self.dt.month, self.dt.day))))
                self.connection.commit()
                self.connection.close()

                self.load = Loading()
                self.obj.player.setMuted(self.obj.player.isMuted())
                self.obj.close()
                self.close()
                self.load.show()
            except:
                msg_box.setText('Никнейм уже используется. Введите другой')
                msg_box.setWindowTitle('Ошибка')
                self.set_icon(msg_box)
                msg_box.show()
                msg_box.exec()


class Question1(QDialog, question1.Ui_Dialog):
    def __init__(self, snd):
        super().__init__()
        self.setupUi(self)
        self.ok.clicked.connect(self.close)
        self.ok.clicked.connect(snd.play)


class Question2(QDialog, question2.Ui_Dialog):
    def __init__(self, snd):
        super().__init__()
        self.setupUi(self)
        self.ok.clicked.connect(self.close)
        self.ok.clicked.connect(snd.play)


class ChooseBthDay(QDialog, birthday_date.Ui_Dialog):
    def __init__(self, snd):
        super().__init__()
        self.setupUi(self)
        self.cansel.clicked.connect(self.close)
        self.cansel.clicked.connect(snd.play)


def exception_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    W = MainMenu()
    W.show()
    sys.excepthook = exception_hook
    sys.exit(app.exec())
