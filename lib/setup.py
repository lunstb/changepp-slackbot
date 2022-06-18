from lib.constants import *
from lib.modules.mavenlinkmodule.mavenlink import *
from lib.modules.terraformmodule.terraform import *
from pathlib import Path


def runSetup():
    admin_slack_email = ""
    admin_mavenlink_email = ""

    with open(SECRETS_JSON, "r") as read_file:
        data = json.load(read_file)
        admin_slack_email = data["ADMIN_SLACK_EMAIL"]
        admin_mavenlink_email = data["ADMIN_MAVENLINK_EMAIL"]

    # Create a machines.json file in the data directory if one does not exist
    machines_file = Path(MACHINES_JSON)
    if machines_file.is_file():
        logging.debug("Machines file already exists")
    else:
        machines_json = {
            "machines": {}
        }
        write_machine_data(machines_json)
        logging.info("Machines file created")

    # Make sure that a database file exists
    users_file = Path(USERS_DB)
    if users_file.is_file():
        logging.debug("Database file exists")
    else:
        f = open(USERS_DB, "w+")
        f.close()
        logging.debug("Database file created")

    # Now connect to the database
    db = database.instance()

    # Check if a table actually exists in the database, if not, make one
    if db.user_table_exists():
        return

    # Now create everything
    db.create_user_table()
    if get_user_id(admin_mavenlink_email) is None:
        logging.error("Hmmm... The Mavenlink email you provided didn't have a user id")
        exit()
    db.insert_user(slack_email = admin_slack_email, mavenlink_id = get_user_id(admin_mavenlink_email), is_admin = True)

    logging.info("Setup is done, the database should be ready!")
