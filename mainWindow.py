
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from display import Display
from info import Info


class MainWindow(QMainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()) -> None:
        super().__init__(parent, flags)

        # Window Setting
        self.cWidget = QWidget()
        self.mLayout = QVBoxLayout()
        self.cWidget.setLayout(self.mLayout)

        # Creating Window
        self.mLayout.addWidget(Info('2.0 ^ 10.0 = 1024'))
        self.mLayout.addWidget(Display())

        self.setWindowTitle("Calculator")
        self.setCentralWidget(self.cWidget)

    def adjustFixedSize(self) -> None:
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
