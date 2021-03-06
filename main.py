from app import WelcomeWindow
import sys
from PySide2 import QtCore, QtGui, QtWidgets
from db_manager import db_manager, populate_countries


if __name__ == '__main__':
    if not db_manager.are_countries_populated():
        populate_countries()
    app = QtWidgets.QApplication(sys.argv)

    window = WelcomeWindow()
    if window.runnable():
        window.show()
        sys.exit(app.exec_())
