import sys

from PyQt5.QtWidgets import (
    QWidget,
    QApplication
)

from functions import (
    loadUiFile, show_message
)

from ..backend import AddLeadBackend


class AddLead(QWidget):
    def __init__(self, **app):
        super(AddLead, self).__init__()

        self.ui = loadUiFile(self, "add_lead.ui")
        self.logger = app['logger']
        self.database = app['database']
        self.backend = AddLeadBackend(self)

        self.ui.AddLeadPushButton.clicked.connect(
            lambda: self.backend.add_lead())

    def refreshUi(self, task):
        if task == "show":
            self.ui.show()

    def closeEvent(self, event):
        event.accept()

