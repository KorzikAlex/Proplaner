import sys
import sqlite3

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QTime

from proplaner_designer import Ui_MainWindow
from note import ProgramNote


class Program(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.program = ''

        # вывод текущего времени
        timer_for_now_time = QTimer(self)
        timer_for_now_time.timeout.connect(self.show_now_time)
        timer_for_now_time.start(1000)
        self.show_now_time()

        self.listAllNotes.setSortingEnabled(True)
        self.add_items_alllist()
        self.add_items_recentlist()

        self.listAllNotes.doubleClicked.connect(self.open_file)
        self.listRecentNotes.doubleClicked.connect(self.open_file)

        self.createButton.clicked.connect(self.create_run)
        self.create_note.triggered.connect(self.create_run)

        self.references_action.triggered.connect(self.reference_box)

    def add_items_alllist(self):
        try:
            connect = sqlite3.connect('note_and_file.db')
            cursor = connect.cursor()
            res_name = cursor.execute('''SELECT name_note FROM notes''').fetchall()

            for i in res_name:
                self.listAllNotes.addItem(i[0])

            connect.close()
        except IndexError:
            pass

    def add_items_recentlist(self):
        try:
            connect = sqlite3.connect('note_and_file.db')
            cursor = connect.cursor()
            res_name = cursor.execute('''SELECT name_note FROM notes''').fetchall()
            res_name.reverse()

            for i in res_name:
                self.listRecentNotes.addItem(i[0])

            connect.close()
        except IndexError:
            pass

    def create_run(self):
        if self.lineName.text() != '':
            self.hide()
            self.program = ProgramNote()
            self.program.show()

            self.program.setWindowTitle(self.lineName.text())
        else:
            if self.sender() == self.create_note:
                input_result = self.input_box()
                if input_result:
                    self.hide()
                    self.program = ProgramNote()
                    self.program.show()

                    self.program.setWindowTitle(input_result)
            else:
                self.warning_box()

    def open_file(self):
        name_note = self.sender().currentItem().text()
        connect = sqlite3.connect('note_and_file.db')
        cursor = connect.cursor()
        text_path = cursor.execute(f'''SELECT text_path FROM notes 
                WHERE name_note LIKE "{name_note}"''').fetchall()[0][0]
        connect.close()
        try:
            text_file = open(text_path, 'r', encoding='UTF-8')
            text_file.close()
        except FileNotFoundError:
            self.warning_files()
        else:
            self.hide()
            self.program = ProgramNote()
            self.program.show()

            self.program.setWindowTitle(name_note)

            connect = sqlite3.connect('note_and_file.db')
            cursor = connect.cursor()
            image_path = cursor.execute(f'''SELECT image_path FROM notes 
            WHERE name_note LIKE "{name_note}"''').fetchall()[0][0]
            connect.close()
            text_file = open(text_path, 'r', encoding='UTF-8')
            self.program.text.setPlainText(text_file.read())
            text_file.close()

            if image_path:
                self.program.setFixedSize(593, 670)
                self.program.image = QPixmap(image_path)
                self.program.labelImage.setPixmap(self.program.image)
                self.program.labelImage.show()
                self.program.insert_delete_Button.setText('Удалить изображение')
                self.program.insert_delete_Button.disconnect()
                self.program.insert_delete_Button.clicked.connect(self.program.delete_image)

    def warning_box(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Ошибка')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msgBox.setWindowIcon(icon)
        msgBox.setText("Введите название заметки")
        msgBox.setIcon(QMessageBox.Warning)

        msgBox.exec_()

    def input_box(self):
        name_of_note, ok_pressed = QInputDialog.getText(self, "Создать заметку",
                                                        "Назовите заметку:")
        if ok_pressed:
            return name_of_note

    def reference_box(self):
        refBox = QMessageBox()
        refBox.setWindowTitle('О программе')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        refBox.setWindowIcon(icon)
        refBox.setText("ProPlaner v 0.2")
        refBox.setInformativeText('Разработал Коршков Александр Александрович, ученик Яндекс Лицея')
        refBox.setIcon(QMessageBox.Information)

        refBox.exec_()

    def warning_files(self):
        refBox = QMessageBox()
        refBox.setWindowTitle('Ошибка')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        refBox.setWindowIcon(icon)
        refBox.setText("Невозможно открыть этот файл")
        refBox.setInformativeText('Возможно, его составляющие файлы утеряны или удалены')
        refBox.setIcon(QMessageBox.Warning)

        refBox.exec_()

    def show_now_time(self):
        current_time = QTime.currentTime()
        display_txt = current_time.toString('hh:mm')
        self.Widgettime.display(display_txt)


if __name__ == '__main__':
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    ex = Program()
    ex.show()
    sys.exit(app.exec_())
