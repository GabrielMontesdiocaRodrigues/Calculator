import math

from PySide6.QtWidgets import QLabel, QWidget, QLineEdit, QPushButton, QGridLayout
from PySide6.QtCore import Qt, Slot

from utils import isNumOrDot, isEmpty, isValidNumber
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

    def __init__(self, display: Display, info: Info, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._grid_mask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['', '0', '.', '=']
        ]

        self.display = display
        self.info = info

        self._equation = ''
        self._left = None
        self._right = None
        self._operator = None

        self.make_grid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, newEquation):
        self._equation = newEquation
        self.info.setText(newEquation)

    def make_grid(self):
        for i, row in enumerate(self._grid_mask):
            for j, buttonText in enumerate(row):

                button = Button(buttonText)
                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                self.addWidget(button, i, j)

                slot = self._makeSlot(self._insertButtonTextToDisplay, button)
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button: Button, slot: Slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button: Button):

        buttonText = button.text()
        if buttonText == 'C':
            self._connectButtonClicked(button, self._clear)

        if buttonText in '+-/*^':
            slot = self._makeSlot(self._operatorClicked, button)
            self._connectButtonClicked(button, slot)

        if buttonText == '=':
            self._connectButtonClicked(button, self._equal)

        if buttonText == '◀':
            self._connectButtonClicked(button, self.display.backspace)

    def _makeSlot(self, function, button):
        @ Slot()
        def realSlot():
            function(button)
        return realSlot

    def _insertButtonTextToDisplay(self, button: Button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText
        if not isValidNumber(newDisplayValue):
            return
        self.display.insert(buttonText)

    def _clear(self):
        self.display.clear()
        self.equation = ''
        self._left = None
        self._right = None
        self._operator = None

    def _equal(self):
        displayText = self.display.text()
        if not isValidNumber(displayText):
            return

        self._right = float(displayText)
        self.equation = f'{self._left} {self._operator} {self._right}'
        try:
            if '^' in self.equation:
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)
        except (ZeroDivisionError, OverflowError):
            result = 'error'

        self.display.clear()
        self._right = None

        if result != 'error':
            self._left = result

        self.info.setText(f'{self.equation} = {result}')

    def _operatorClicked(self, button: Button):

        displayText = self.display.text()
        buttonText = button.text()

        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            return

        if self._left is None:
            self._left = float(displayText)

        self._operator = buttonText
        self.equation = f'{self._left} {self._operator} __'
