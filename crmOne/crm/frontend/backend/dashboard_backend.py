import json

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


class DashboardBackend(object):

    def __init__(self, frontend):
        self.frontend = frontend
        self.database = frontend.database
        self.logger = frontend.logger

    def load_leads(self):
        with self.database as session:
            leads = session.query(self.database.Contact).filter_by(status="Lead").all()

            new_leads = []
            for contact in leads:
                contact.name = ' '.join(contact.name.split('_'))
                contact.meta_data = json.loads(contact.meta_data)
                contact.contact_info = json.loads(contact.contact_info)
                new_leads.append(contact)

            self.frontend.ui.LeadsTreeWidget.clear()
            self.frontend.ui.LeadsTreeWidget.setHeaderLabels(["Name", "Email", "Priority", "Company"])
            self.frontend.ui.LeadsTreeWidget.header().setSectionResizeMode(QHeaderView.Stretch)
            self.frontend.ui.LeadsTreeWidget.setContextMenuPolicy(Qt.CustomContextMenu)

            for lead in new_leads:
                item = QTreeWidgetItem([lead.name, lead.contact_info['email'], lead.meta_data['priority'], lead.company_id])

                if lead.meta_data['priority'] == "HIGH":
                    item.setForeground(2, QColor("#38761d"))

                if lead.meta_data['priority'] == "MEDIUM":
                    item.setForeground(2, QColor("#bd9e06"))

                if lead.meta_data['priority'] == "LOW":
                    item.setForeground(2, QColor("#990000"))

                item.setData(0, Qt.UserRole, lead)
                self.frontend.ui.LeadsTreeWidget.addTopLevelItem(item)

    def load_companies(self):
        with self.database as session:
            companies = session.query(self.database.Company).all()

            new_companies = []
            for company in companies:
                company.meta_data = json.loads(company.meta_data)
                new_companies.append(company)

            self.frontend.ui.CompaniesTreeWidget.clear()
            self.frontend.ui.CompaniesTreeWidget.setHeaderLabels(["Name", "Contact Information"])
            self.frontend.ui.CompaniesTreeWidget.header().setSectionResizeMode(QHeaderView.Stretch)
            self.frontend.ui.CompaniesTreeWidget.setContextMenuPolicy(Qt.CustomContextMenu)

            for business in new_companies:
                item = QTreeWidgetItem([business.name, business.meta_data['email']])

                # if lead.meta_data['priority'] == "HIGH":
                #     item.setForeground(2, QColor("#38761d"))
                #
                # if lead.meta_data['priority'] == "MEDIUM":
                #     item.setForeground(2, QColor("#bd9e06"))
                #
                # if lead.meta_data['priority'] == "LOW":
                #     item.setForeground(2, QColor("#990000"))

                item.setData(0, Qt.UserRole, business)
                self.frontend.ui.CompaniesTreeWidget.addTopLevelItem(item)






