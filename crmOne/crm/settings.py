import os
from dotenv import dotenv_values


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_NAME = ROOT_DIR.split("/")[-1]

FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
UI_DIR = os.path.join(FRONTEND_DIR, "ui")

DATABASE_DIR = os.path.join(ROOT_DIR, "database")
DATABASE = os.path.join(DATABASE_DIR, "database.db")

LOG_DIR = os.path.join(DATABASE_DIR, "logs")
APP_LOG = os.path.join(LOG_DIR, "app.log")
DATABASE_LOG = os.path.join(LOG_DIR, "database.log")

CORE_DIR = os.path.join(ROOT_DIR, 'core')
ENV_FILE = os.path.join(CORE_DIR, '.env')
CREDENTIALS = dict(dotenv_values(ENV_FILE))

CURRENT_USER = None


def checkDirs():
    directories = [
        ROOT_DIR,
        DATABASE_DIR,
        LOG_DIR,
        FRONTEND_DIR,
        UI_DIR
    ]

    files = [
        DATABASE,
        APP_LOG,
        DATABASE_LOG,
        ENV_FILE
    ]

    for Dir in directories:
        if not os.path.exists(Dir):
            os.mkdir(Dir)
            print(f"CREATED {Dir}")

    for file in files:
        if not os.path.exists(file):
            open(file, "a").close()
            print(f"CREATED {file}")


checkDirs()
