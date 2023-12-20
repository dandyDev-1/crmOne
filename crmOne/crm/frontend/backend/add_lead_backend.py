import json

from functions import (generateId, timeHandler, filter_string)


class AddLeadBackend(object):

    def __init__(self, frontend):
        self.frontend = frontend
        self.database = frontend.database
        self.logger = frontend.logger

    def dict_to_class(self, data: dict):
        new_class = self.database.User(
            id=data['id'],
            username=data['username'],
            password=data['password'],
            meta_data=json.dumps(data['meta_data'])
        )
        return new_class

    def add_lead(self):
        with self.database as session:
            name = f"{self.frontend.ui.FNameLineEdit.text()}_{self.frontend.ui.LNameLineEdit.text()}".lower()

            contact_info = {
                "email": filter_string(self.frontend.ui.EmailAddressLineEdit.text(), email_address=True),
                'phone': filter_string(self.frontend.ui.PhoneNumberLineEdit.text(), phone=True)
            }

            meta_data = {
                "website": self.frontend.ui.WebsiteLineEdit.text(),
                "creation_date": str(timeHandler(getCurrentTime=True)),
                "description": self.frontend.ui.DescriptionTextEdit.toPlainText(),
                "priority": self.frontend.ui.PriorityComboBox.currentText()
            }

            company_var = session.query(
                self.database.Company).filter_by(
                name=self.frontend.ui.CompanyLineEdit.text().lower()).first()

            if company_var:
                company = company_var
            else:
                company = self.database.Company(
                    id=generateId("string"),
                    name=self.frontend.ui.CompanyLineEdit.text().lower(),
                    meta_data=json.dumps({
                        "entry_date": str(timeHandler(getCurrentTime=True)),
                        'email': '',
                        'website': ''
                    }))

            new_lead = self.database.Contact(
                id=generateId("string"),
                name=name,
                contact_info=json.dumps(contact_info),
                status="Lead",
                company_id=company.id,
                meta_data=json.dumps(meta_data)
            )

            session.add(company)
            session.add(new_lead)
            session.commit()


