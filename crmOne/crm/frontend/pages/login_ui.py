import sys

from PyQt5.QtWidgets import (
    QWidget,
    QApplication
)

from functions import (
    loadUiFile, show_message
)

import settings

from .signup_ui import Signup
from ..backend import LoginBackend


class Login(QWidget):
    def __init__(self, **app):
        super(Login, self).__init__()

        self.ui = loadUiFile(self, "login.ui")
        self.logger = app['logger']
        self.database = app['database']
        self.dashboard = app['frontend']
        self.backend = LoginBackend(self)

        self.SignupWindow = None
        self.ui.SignUpPushButton.clicked.connect(
            lambda: self.openWindow('signup'))

        self.ui.LoginPushButton.clicked.connect(
            lambda: self.login())

    def login(self):
        user = self.backend.get_user()
        if user[0] is True:
            self.ui.close()

            settings.CURRENT_USER = user[1]
            self.dashboard.backend.load_leads()
            self.dashboard.ui.show()

        elif user[0] is False:
            show_message('username or password is incorrect', self.ui)

        else:
            pass

    def refreshUi(self, task):
        if task == "show":
            self.ui.show()

    def openWindow(self, source):
        try:
            if source == "signup":
                if not self.SignupWindow:
                    self.SignupWindow = Signup(
                        logger=self.logger,
                        database=self.database
                    )
                    self.SignupWindow.ui.show()
                else:
                    self.SignupWindow.ui.show()

        except Exception as e:
            self.logger.log(f"Error opening window {source}: {e}", severity="error")

        finally:
            pass

    def closeEvent(self, event):
        event.accept()

