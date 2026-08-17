import sys, os
from sys import path

import PySide6
from PySide6.QtCore import Qt, QSettings
from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QIcon, QAction

from PySide6.QtWidgets import(
QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QLabel,
QMenuBar,
QTextEdit,
QDialog,
)
from PySide6.QtPrintSupport import QPrinter, QPrintDialog






class MainWindow(QtWidgets.QWidget):

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_path, relative_path)

    def open_explorer(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Documents (*.txt *.md *.py);;All Files (*)"
        )

        if path:
            self.open_file(path)

    def save_file(self):
        if self.first_open:
            return

        text = self.text.toPlainText()

        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(text)

    def print_file(self):
        if self.first_open:
            return
        print("печатаю")
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        document = self.text.document()
        result = dialog.exec()

        if result == QDialog.Accepted:
            document.print_(printer)

    def open_file(self, path):
        with open(path, "r", encoding="utf-8") as file:
            text = file.read()

        self.file_path = path
        self.settings.setValue("last_file", path)

        file_name = os.path.basename(path)
        self.setWindowTitle(file_name + " - Блокнот")

        if self.first_open:
            self.layout.removeWidget(self.path_label)
            self.path_label.deleteLater()

            self.first_open = False

            self.layout.addWidget(self.text)

            # кнопка сохранить
            self.layout.addWidget(self.save)
            self.save.clicked.connect(self.save_file)

        self.text.setText(text)




    def __init__(self):
        super().__init__()

        self.settings = QSettings("MyNotepad", "MyNotepad")

        icon_path = self.resource_path("icon.png")
        self.setWindowIcon(QIcon(icon_path))



        #заголовок
        file_name = "NULL"
        zagolovok = file_name + " - Блокнот"
        self.setWindowTitle(zagolovok)
        self.resize(1000, 800)
        #лейаут
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        #кнопки меню
        self.menu_bar = QMenuBar()
        self.menu_bar.setFixedHeight(30)
        self.file_menu = self.menu_bar.addMenu("Файл")
        self.menu_bar.setStyleSheet(
            "QMenuBar::item { border: 1px solid black; padding: 5px; }"
        )
        open_action = QAction("Открыть", self)
        self.file_menu.addAction(open_action)
        self.first_open = True
        open_action.triggered.connect(self.open_explorer)

        print_action = QAction("Печать", self)

        self.file_menu.addAction(print_action)
        print_action.triggered.connect(self.print_file)
        #поле для текста
        self.path_label = QLabel("Файл не выбран")
        #текст
        self.text = QTextEdit()
        # кнопка сохранить
        self.save = QPushButton("Сохранить")






        #кнопки в лейаут
        self.layout.addWidget(self.menu_bar)
        self.layout.addWidget(self.path_label)
        self.layout.setAlignment(Qt.AlignTop)







        last_file = self.settings.value("last_file", "")

        if last_file and os.path.exists(last_file):
            self.open_file(last_file)









app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()


app.exec()