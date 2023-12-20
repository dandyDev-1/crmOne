import sys

from PyQt5.QtWidgets import QApplication

import settings

from functions import Logger
from frontend import DashBoard
from database import DatabaseManager


class Application:
    def __init__(self):
        self.database = DatabaseManager(settings.DATABASE)
        self.logger = Logger()

    def run_app(self):
        try:
            app = QApplication(sys.argv)
            dashboard = DashBoard(database=self.database, logger=self.logger)
            self.logger.log("Application initialized")
            sys.exit(app.exec_())

        except Exception as e:
            self.logger.log(f"Application initialization error :{e}", severity="error")


if __name__ == "__main__":
    App = Application()
    App.run_app()
