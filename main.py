
from PySide6.QtGui import QIcon
from variables import ICON_PATH
from PySide6.QtWidgets import QApplication
from mainWindow import MainWindow
from style import setupTheme

if __name__ == '__main__':
    # Creating Window
    app = QApplication()
    # Application Style
    setupTheme(app)

    window = MainWindow()

    # Setting the icon for the calculator
    window.setWindowIcon(QIcon(str(ICON_PATH)))
    app.setWindowIcon(QIcon(str(ICON_PATH)))

    # Running the window
    window.adjustFixedSize()
    window.show()
    app.exec()
