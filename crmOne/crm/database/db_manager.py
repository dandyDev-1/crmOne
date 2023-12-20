from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from .db_models import (
    Base,
    Setting,
    User,
    Contact,
    Company,
    Interaction,
    Sale
)


class DatabaseManager(object):
    def __init__(self, database_file):
        self.engine = create_engine(
            f"sqlite:///{database_file}",
            connect_args={'check_same_thread': False}
        )

        self.Setting = Setting
        self.Contact = Contact
        self.Company = Company
        self.Interaction = Interaction
        self.User = User
        self.setTables()

    def __enter__(self):
        session_factory = sessionmaker(bind=self.engine)
        session = scoped_session(session_factory)
        self.session = session()
        return self.session

    def __exit__(self, ext_type, exc_value, traceback):
        self.session.close()
        if isinstance(exc_value, Exception):
            self.session.rollback()
            print(f"ERROR OCCURRED. ROLLED BACK CHANGES")
        else:
            self.session.commit()
        self.session.close()

    def setTables(self):
        Base.metadata.create_all(self.engine)