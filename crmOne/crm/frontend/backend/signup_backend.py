import json
import bcrypt

from functions import (generateId, timeHandler, show_message)


class SignupBackend(object):

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

    def check_user(self):
        username = self.frontend.ui.UsernameLineEdit.text()

        with self.database as session:
            user = session.query(self.database.User).filter_by(username=username).first()

            if user:
                return False

            else:
                return True

    def create_user(self):
        username = self.frontend.ui.UsernameLineEdit.text()
        password = self.frontend.ui.PasswordLineEdit.text()
        password_verify = self.frontend.ui.PasswordAgainLineEdit.text()

        if len(password) >= 2 and len(password_verify) >= 2:  # todo change to 8

            if password == password_verify:

                checked_user = self.check_user()
                if checked_user is True:

                    user = {
                        'id': generateId('string'),
                        'username': username,
                        'password': password,
                        'meta_data': {
                            'creation_date': str(timeHandler(getCurrentTime=True))
                        }
                    }

                    with self.database as session:
                        session.add(self.dict_to_class(user))
                        session.commit()

                    show_message(f"successfully created user {username} ", self.frontend.ui)
                    self.frontend.ui.close()

                elif checked_user is False:
                    show_message(f"user {username} already exists", self.frontend.ui)

            else:
                show_message("The passwords have to match", self.frontend.ui)
        else:
            show_message("the password length has to be at least 2 characters", self.frontend.ui)


    def hash_password(self, password):
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        key = bcrypt.hashpw(password_bytes, salt)
        hash = {"salt": salt, "key": key}
        return hash


