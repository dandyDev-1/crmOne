
class LoginBackend(object):

    def __init__(self, frontend):
        self.frontend = frontend
        self.database = frontend.database
        self.logger = frontend.logger

    def get_user(self):
        username = self.frontend.ui.UsernameLineEdit.text()
        password = self.frontend.ui.PasswordLineEdit.text()

        if len(username) > 0 and len(password) > 0:
            with self.database as session:
                user = session.query(self.database.User).filter_by(username=username, password=password).first()
                if user:
                    return True, user
                else:
                    return False, user
