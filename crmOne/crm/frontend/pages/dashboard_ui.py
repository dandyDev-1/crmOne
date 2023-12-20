import sys

from PyQt5.QtGui import (
    QColor
)

from PyQt5.QtWidgets import (
    QMainWindow,
    QTreeWidgetItem,
    QHeaderView
)

from PyQt5.QtCore import (
    QThreadPool,
    Qt
)

from functions import (
    loadUiFile,
    show_message
)

from .login_ui import Login
from .add_lead_ui import AddLead
from .add_company_ui import AddCompany
from ..backend import DashboardBackend


class DashBoard(QMainWindow):
    def __init__(self, **app):
        super(DashBoard, self).__init__()

        self.ui = loadUiFile(self, "dashboard.ui")
        self.database = app['database']
        self.logger = app['logger']
        self.backend = DashboardBackend(self)

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(80)

        self.current_user = None
        self.AddLeadWindow = None
        self.AddCompanyWindow = None

        self.ui.AddLeadPushButton.clicked.connect(
            lambda: self.openWindow("add_lead")
        )

        self.ui.AddCompanyPushButton.clicked.connect(
            lambda: self.openWindow("add_company")
        )

        self.ui.SubjectTabWidget.currentChanged.connect(
            lambda x: self.tabChanged(x)
        )

        self.refreshUi(task="login")

    def tabChanged(self, index):
        if index == 0:
            self.backend.load_leads()

        elif index == 1:
            self.backend.load_companies()

    def openWindow(self, source):
        try:
            if source == "add_lead":
                if not self.AddLeadWindow:
                    self.AddLeadWindow = AddLead(
                        logger=self.logger,
                        database=self.database
                    )
                    self.AddLeadWindow.ui.show()
                else:
                    self.AddLeadWindow.ui.show()

            elif source == "add_company":
                if not self.AddCompanyWindow:
                    self.AddCompanyWindow = AddCompany(
                        logger=self.logger,
                        database=self.database
                    )
                    self.AddCompanyWindow.ui.show()
                else:
                    self.AddCompanyWindow.ui.show()

        except Exception as e:
            self.logger.log(f"Error opening window {source}: {e}", severity="error")

        finally:
            pass

    def refreshUi(self, task: str):
        if task == "login":
            login_window = Login(database=self.database, logger=self.logger, frontend=self)
            login_window.refreshUi("show")

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Return:
            if len(self.ui.SearchLineEdit.text()) > 0:
                self.handleList(task="add_item", value=self.ui.SearchLineEdit.text())
        else:
            super().keyPressEvent(qKeyEvent)

    def closeEvent(self, event):
        reply = show_message("Are you sure you want to quit?", self, message_type="question")
        if reply is True:
            event.accept()
            self.logger.log("Closing Application")
            sys.exit()
        else:
            event.ignore()

