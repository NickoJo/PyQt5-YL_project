import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        layout = QVBoxLayout()
        self.editor = QPlainTextEdit()

        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        self.path = None
        # self.path содержит путь до нашего конретного txt файла, если None, то файл не открыт

        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        file_toolbar = QToolBar("Файл")
        file_toolbar.setIconSize(QSize(17, 17))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&Файл")

        open_file_action = QAction(QIcon(os.path.join('icons', 'open.png')), "Открыть", self)
        open_file_action.setStatusTip("Открыть файл")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('icons', 'save.png')), "Сохранить", self)
        save_file_action.setStatusTip("Сохранить текущую страницу")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('icons', 'saveas.png')), "Сохранить как...", self)
        saveas_file_action.setStatusTip("Сохранить текущую страницу в указанный путь")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon(os.path.join('icons', 'print.png')), "Печать", self)
        print_action.setStatusTip("Распечатать текущую страницу")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Изменить")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Изменить")

        undo_action = QAction(QIcon(os.path.join('icons', 'undo.png')), "Отменить", self)
        undo_action.setStatusTip("Отменить последнее изменение")
        undo_action.triggered.connect(self.editor.undo)
        edit_toolbar.addAction(undo_action)
        edit_menu.addAction(undo_action)
        edit_menu.addSeparator()

        cut_action = QAction(QIcon(os.path.join('icons', 'cut.png')), "Вырезать", self)
        cut_action.setStatusTip("Вырезать выделенное")
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon(os.path.join('icons', 'copy.png')), "Скопировать", self)
        copy_action.setStatusTip("Скопировать выделенное")
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join('icons', 'paste.png')), "Вставить", self)
        paste_action.setStatusTip("Вставить из буфера обмена")
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join('icons', 'selectall.png')), "Выбрать все", self)
        select_action.setStatusTip("Выбрать весь текст")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()
        self.update_title()
        self.show()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "(*.txt)")
        try:
            with open(path) as f:
                text = f.read()
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.editor.setPlainText(text)
            self.update_title()

    def file_save(self):
        if self.path is None:
            return self.file_saveas()
            # если конкретного файла нет, то программа перекидывает на функцию "Сохранить как"
        text = self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить как", "", "(*.txt)")
        text = self.editor.toPlainText()
        if not path:
            return
        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s — Блокнотик" % (os.path.basename(self.path) if self.path else "Безымянный"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Блокнотик")
    window = MainWindow()
    app.exec_()
