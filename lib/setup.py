import json

from lib.constants import *
from lib.modules.databasemodule.database import *
from pathlib import Path


def run_setup():
    admin_slack_email = ""
    first_name = ""
    last_name = ""
    user_type = ""
    graduation_year = 0

    with open(SECRETS_JSON, "r") as read_file:
        data = json.load(read_file)
        admin_slack_email = data["ADMIN_SLACK_EMAIL"]
        first_name = data["FIRST_NAME"]
        last_name = data["LAST_NAME"]
        user_type = data["USER_TYPE"]
        graduation_year = data["GRADUATION_YEAR"]

    users_file = Path(DB_NAME)

    # If the database file doesn't exist, create it
    users_file.parent.mkdir(parents=True, exist_ok=True)

    # Now connect to the database
    db = database.instance()

    # Create the tables if they don't exist
    db.create_user_table_if_not_exists()
    db.create_resume_table_if_not_exists()
    db.create_books_table_if_not_exists()
    db.create_networking_table_if_not_exists()
    db.create_intern_table_if_not_exists()

    db.insert_user(slack_email=admin_slack_email,
                   first_name=first_name,
                   last_name=last_name,
                   user_type=user_type,
                   graduation_year=graduation_year,
                   is_admin=True)

    logging.info("Setup is done, the database should be ready!")
