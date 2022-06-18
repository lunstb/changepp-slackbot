"""This script handles database interaction

The database consists of a single users table with the properties email, mavenlink_id, and is_admin as follows:

+--------+--------------+----------+----------+---------------------------+
| email  | mavenlink_id | is_admin |  pubkey  | instance_destruction_date |
+--------+--------------+----------+----------+---------------------------+
|  TEXT  |     TEXT     | INTEGER  |   TEXT   |        TIMESTAMP          |
+--------+--------------+----------+----------+---------------------------+

Note that even though users are created using their mavenlink email, the only time that email is relevant is on the creation because after that only the mavenlink id is used"""

import datetime
import logging
import sqlite3


class database:
    _instance = None

    def __init__(self):
        raise RuntimeError('call instance() instead')

    @classmethod
    def instance(self):
        """Returns an instance"""

        if self._instance is None:
            self._instance = self.__new__(self)
            self._instance.initialize()
        return self._instance

    def initialize(self):
        """Initializes the database and ensures that a database file exists"""

        logging.debug("Attempting to connect to sqlite database")
        self.con = sqlite3.connect("data/users.db", detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
        self.cur = self.con.cursor()
        logging.debug("Successfully connected to sqlite database, now making sure that there is a table")
        if not self.user_table_exists():
            logging.error("Database not initialized")
        else:
            logging.debug("Valid database available for interaction")

    def user_table_exists(self):
        """Returns whether the 'user' table exists or not """

        self.cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' and name='users'")
        return self.cur.fetchone() is not None

    def create_user_table(self):
        """Creates the user table, only used in setup """

        self.cur.execute(
            "CREATE TABLE users (email TEXT, mavenlink_id TEXT, is_admin INTEGER, pubkey TEXT, instance_destruction_date TIMESTAMP)")
        self.con.commit()
        logging.info("User table created")

    def drop_user_table(self):
        """Drops the user table, only used in setup """

        self.cur.execute("DROP TABLE users")
        self.con.commit()
        logging.info("Dropping user table")

    def get_mavenlink_id(self, slack_email):
        """Gets the mavenlink_id of a user from their slack email"""

        self.cur.execute(
            "SELECT mavenlink_id FROM users WHERE email is ?", (slack_email,))
        return self.cur.fetchone()[0]


    def check_user_is_admin(self, slack_email):
        """Checks whether the user correlating to the supplied slack_email is an admin"""

        self.cur.execute(
            "SELECT is_admin FROM users WHERE email is ?", (slack_email,))
        return self.cur.fetchone()[0]

    def update_user_is_admin(self, slack_email, is_admin):
        """Updates the admin status of the user with the supplied slack_email """

        self.cur.execute(
            "UPDATE users SET is_admin = ? WHERE email is ?", (is_admin, slack_email))
        self.con.commit()

    def get_user_pubkey(self, slack_email):
        """Gets the public key for the supplied slack_email"""

        self.cur.execute(
            "SELECT pubkey FROM users WHERE email is ?", (slack_email,))
        return self.cur.fetchone()[0]

    def set_user_pubkey(self, slack_email, pubkey):
        """Sets the default pubkey of the user with the supplied slack_email """

        self.cur.execute(
            "UPDATE users SET pubkey = ? WHERE email is ?", (pubkey, slack_email))
        self.con.commit()
        logging.debug(f"SSH pubkey of {slack_email} updated")

    def get_all_user_pubkeys(self):
        """Get all users in the db which have pubkeys"""

        self.cur.execute(
            "SELECT email, pubkey FROM users WHERE pubkey is NOT NULL")
        return self.cur.fetchall()

    def insert_user(self, slack_email, mavenlink_id, is_admin):
        """Inserts a user into the database with the specified parameters """

        self.cur.execute("INSERT INTO users VALUES (?,?,?,?,?)",
                         (slack_email, mavenlink_id, is_admin, "", None))
        self.con.commit()
        logging.debug(f"User with slack email {slack_email} inserted into users table")

    def get_users(self):
        """Returns all of the users from the database """

        self.cur.execute("SELECT mavenlink_id, email, is_admin FROM users")
        return self.cur.fetchall()

    def remove_user(self, slack_email):
        """Removes the user with the supplied slack email"""

        self.cur.execute("DELETE FROM users WHERE email is ?", (slack_email,))
        self.con.commit()

    def check_user_exists(self, slack_email):
        """Checks whether or not there is a user with the supplied slack_email in the database"""

        self.cur.execute(
            "SELECT is_admin FROM users WHERE email is ?", (slack_email,))
        return self.cur.fetchone() is not None

    def get_instance_destruction_date(self, slack_email):
        """Returns the date that the instance will be destroyed"""

        self.cur.execute(
            "SELECT instance_destruction_date FROM users WHERE email is ?", (slack_email,))

        response = self.cur.fetchone()
        return response[1]

    def extend_instance_destruction_date(self, slack_email, days=3):
        """Extends the destruction date of an instance to X days from now"""

        new_deadline = datetime.datetime.now() + datetime.timedelta(days)
        self.cur.execute(
            "UPDATE users SET instance_destruction_date = ? WHERE email is ?", (new_deadline, slack_email,))
        self.con.commit()

        return new_deadline

    def clear_instance_destruction_date(self, slack_email):
        """Set the destruction date of a consultant's instance to NULL as they no longer have an active instance"""

        self.cur.execute(
            "UPDATE users SET instance_destruction_date = ? WHERE email is ?", (None, slack_email,))
        self.con.commit()

