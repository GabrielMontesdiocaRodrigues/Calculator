
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from components import Display, Info, ButtonsGrid


class MainWindow(QMainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()) -> None:
        super().__init__(parent, flags)

        # Window Setting
        self.cWidget = QWidget()
        self.mLayout = QVBoxLayout()
        self.cWidget.setLayout(self.mLayout)

        # Creating Window
        self.mLayout.addWidget(Info(''))
        display = Display()
        self.mLayout.addWidget(display)
        self.mLayout.addLayout(ButtonsGrid(display))

        self.setWindowTitle("Calculator")
        self.setCentralWidget(self.cWidget)

    def adjustFixedSize(self) -> None:
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
