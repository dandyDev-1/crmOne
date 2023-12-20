import json

from functions import (generateId, timeHandler, filter_string)


class AddCompanyBackend(object):

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

    def add_company(self):
        with self.database as session:
            meta_data = {
                "website": self.frontend.ui.WebsiteLineEdit.text(),
                "email": filter_string(self.frontend.ui.EmailAddressLineEdit.text(), email_address=True),
                'phone': filter_string(self.frontend.ui.PhoneNumberLineEdit.text(), phone=True),
                "description": self.frontend.ui.DescriptionTextEdit.toPlainText()
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
                    meta_data=json.dumps(meta_data))

            session.add(company)
            session.commit()


