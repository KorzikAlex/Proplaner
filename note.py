import sys
import sqlite3

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import QTimer
from note_designer import Ui_note_app


class ProgramNote(QWidget, Ui_note_app):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.insert_delete_Button.clicked.connect(self.insert_image)
        self.saveButton.clicked.connect(self.save_files)

    def insert_image(self) -> None:
        name_image = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg)')[0]

        if name_image:
            self.setFixedSize(593, 670)
            self.image = QPixmap(name_image)
            self.labelImage.setPixmap(self.image)
            self.labelImage.show()

            self.insert_delete_Button.setText('Удалить изображение')
            self.insert_delete_Button.disconnect()
            self.insert_delete_Button.clicked.connect(self.delete_image)

    def delete_image(self) -> None:
        self.labelImage.clear()
        self.insert_delete_Button.setText('Загрузить изображение')
        self.setFixedSize(593, 370)
        self.insert_delete_Button.disconnect()
        self.insert_delete_Button.clicked.connect(self.insert_image)

    def save_files(self):
        if self.text.toPlainText() != '':
            image_path = ''

            txt_file = open(f'pfiles\ptext\{self.windowTitle()}.txt', 'w', encoding='UTF-8')
            txt_file.write(self.text.toPlainText())
            txt_file.close()

            name_note = self.windowTitle()
            text_path = f'pfiles\ptext\{self.windowTitle()}.txt'

            if self.labelImage.pixmap():
                self.image.save(f'pfiles\pimages\{self.windowTitle()}.jpg')
                image_path = f'pfiles\pimages\{self.windowTitle()}.jpg'
            try:
                if image_path != '':
                    action = f'''UPDATE notes SET text_path = '{text_path}', image_path = '{image_path}'
                    WHERE name_note = "{name_note}"'''
                else:
                    action = f'''UPDATE notes SET text_path = '{text_path}', image_path = NULL 
                    WHERE name_note = "{name_note}"'''

                connect = sqlite3.connect('note_and_file.db')
                cursor = connect.cursor()
                check_arg = cursor.execute(f'''SELECT text_path FROM notes 
                                WHERE name_note LIKE "{name_note}"''').fetchall()[0][0]

                cursor.execute(action)
                connect.commit()

                connect.close()
            except IndexError:
                if image_path != '':
                    action = f'''INSERT INTO notes(name_note, text_path, image_path) 
                    VALUES('{name_note}', '{text_path}', '{image_path}')'''
                else:
                    action = f'''INSERT INTO notes(name_note, text_path) VALUES('{name_note}', '{text_path}')'''

                connect = sqlite3.connect('note_and_file.db')
                cursor = connect.cursor()
                cursor.execute(action)

                connect.commit()
                connect.close()

            self.savelabel.setText('Сохранение успешно')
            timer_save = QTimer(self)
            timer_save.timeout.connect(self.show_timer_save)
            timer_save.start(2000)

        elif self.labelImage.pixmap() and self.text.toPlainText() == '':
            self.warning_file_image()
        else:
            self.warning_file()

    def warning_file(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Ошибка')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msgBox.setWindowIcon(icon)
        msgBox.setText("Ничего не введено")
        msgBox.setIcon(QMessageBox.Warning)

        msgBox.exec_()

    def warning_file_image(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Ошибка')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msgBox.setWindowIcon(icon)
        msgBox.setText("Введите текст")
        msgBox.setIcon(QMessageBox.Warning)

        msgBox.exec_()

    def show_timer_save(self):
        self.savelabel.setText('')

    def closeEvent(self, event) -> None:
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Выход')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msgBox.setWindowIcon(icon)
        msgBox.setText("Вы уверены что хотите выйти?")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        result = msgBox.exec_()

        if result == QMessageBox.Ok:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    ex = ProgramNote()
    ex.show()
    sys.exit(app.exec_())
