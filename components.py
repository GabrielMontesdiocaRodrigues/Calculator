from PySide6.QtWidgets import QLabel, QWidget, QLineEdit, QPushButton, QGridLayout
from PySide6.QtCore import Qt, Slot

from utils import isNumOrDot, isEmpty
from variables import SMALL_FONT_SIZE, TEXT_MARGIN, MINIMUN_WIDTH, BIG_FONT_SIZE, MEDIUM_FONT_SIZE


class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None):
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)


class Display(QLineEdit):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        margins = [TEXT_MARGIN for _ in range(4)]
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUN_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)


class Button(QPushButton):

    def __init__(self, text: str, parent: QWidget | None = None):
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        font.setBold(True)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):

    def __init__(self, display: Display, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._grid_mask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['', '0', '.', '=']
        ]

        self.display = display

        self.make_grid()

    def make_grid(self):
        for i, row in enumerate(self._grid_mask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)
                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                self.addWidget(button, i, j)

                button.clicked.connect(
                    self._makeButtonDisplaySlot(
                        self._insertButtonTextToDisplay, button
                    )
                )

    def _makeButtonDisplaySlot(self, function, button):
        @Slot()
        def realSlot():
            function(button)
        return realSlot

    def _insertButtonTextToDisplay(self, button: Button):
        self.display.insert(button.text())
