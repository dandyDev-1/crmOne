import sys

from PyQt5.QtWidgets import (
    QWidget,
    QApplication
)

from functions import (
    loadUiFile, show_message
)

from ..backend import AddCompanyBackend


class AddCompany(QWidget):
    def __init__(self, **app):
        super(AddCompany, self).__init__()

        self.ui = loadUiFile(self, "add_company.ui")
        self.logger = app['logger']
        self.database = app['database']
        self.backend = AddCompanyBackend(self)

        self.ui.AddCompanyPushButton.clicked.connect(
            lambda: print('add company'))

    def refreshUi(self, task):
        if task == "show":
            self.ui.show()

    def closeEvent(self, event):
        event.accept()

