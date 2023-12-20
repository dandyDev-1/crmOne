import sys

from PyQt5.QtWidgets import (
    QWidget,
    QApplication
)

from functions import (
    loadUiFile, show_message
)

from ..backend import SignupBackend


class Signup(QWidget):
    def __init__(self, **app):
        super(Signup, self).__init__()

        self.ui = loadUiFile(self, "signup.ui")
        self.logger = app['logger']
        self.database = app['database']
        self.backend = SignupBackend(self)

        self.ui.CreateAccountPushButton.clicked.connect(
            lambda: self.backend.create_user())

    def closeEvent(self, event):
        event.accept()

