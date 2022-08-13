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
import uuid

#from lib.modules.modulehelpers import get_book_name_from_isbn


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
            "CREATE TABLE users (email TEXT, first_name TEXT, last_name TEXT, user_type TEXT, graduation_year INTEGER, is_admin INTEGER)")
        self.con.commit()
        logging.info("User table created")

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

    def get_user_year(self, slack_email):
        """Returns the graduation year of the user with the supplied slack_email"""

        self.cur.execute(
            "SELECT graduation_year FROM users WHERE email is ?", (slack_email,))
        return self.cur.fetchone()[0]

    # FIXME: do we need user_type and is_admin?
    def insert_user(self, slack_email, first_name, last_name, user_type, graduation_year, is_admin):
        """Inserts a user into the database with the specified parameters """

        self.cur.execute("INSERT INTO users VALUES (?,?,?,?,?,?)",
                         (slack_email, first_name, last_name, user_type, graduation_year, is_admin))
        self.con.commit()
        logging.debug(f"User with slack email {slack_email} inserted into users table")

    def get_users(self):
        """Returns all of the users from the database """

        self.cur.execute("SELECT email, is_admin FROM users")
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

    def drop_user_table(self):
        """Drops the user table, only used in setup """

        self.cur.execute("DROP TABLE users")
        self.con.commit()
        logging.info("Dropping user table")

    def create_books_table(self):
        """Creates the books table, only used in setup"""

        self.cur.execute(
            "CREATE TABLE books (ID TEXT, ISBN TEXT, name TEXT, original_owner_email TEXT, owner_email TEXT, last_transaction_date TIMESTAMP)"
        )
        self.con.commit()
        logging.info("Books table created")

    def add_book(self, ISBN, name, email):
        """Adds a book to the book table"""

        # Generate ID
        book_id = uuid.uuid4()

        self.cur.execute(
            "INSERT INTO books VALUES (?, ?, ?, ?, ?)", (book_id, ISBN, name, email, email, None)
        )
        self.con.commit()
        logging.info(f"Book with ISBN {ISBN} into books table")

    def remove_book(self, book_id):
        """Removes a book from the book table"""

        self.cur.execute(
            f"DELETE FROM books WHERE book_id = {book_id}"
        )
        self.con.commit()
        logging.info("Book removed from books table")

    def trade_book(self, book_id, owner_email):
        """Trades a book with book_id to owner_email"""

        # I need to also update the transaction date

        self.cur.execute(
            f"UPDATE books SET owner_email = {owner_email} WHERE book_id = {book_id}"
        )
        self.con.commit()
        logging.info("Book traded")

    def get_books(self):
        """Returns all of the books from the database with
         isbn, name, original ownder, and last transaction date fields"""

        self.cur.execute("SELECT ISBN, name, owner_email, last_transaction_date FROM books")
        return self.cur.fetchall()

    def drop_books_table(self):
        """Drops the books table, only used in setup"""

        self.cur.execute("DROP TABLE books")
        self.con.commit()
        logging.info("Dropping books table")

    def create_resume_table(self):
        """Creates the resume table, only used in setup"""

        self.cur.execute(
            "CREATE TABLE resume (user_email TEXT, AWS_link TEXT, PRIMARY KEY (user_email))"
        )
        self.con.commit()
        logging.info("Resume table created")

    def get_resumes(self, id=None):
        """Returns all of the resumes from the database"""
        
        if id is None:
            self.cur.execute("SELECT * FROM resume")
            return self.cur.fetchall()
        else:
            self.cur.execute(f"SELECT 1 FROM resume WHERE user_email = '{id}'")
            return self.cur.fetchall()

    def insert_resume(self, user_email, AWS_link):
        """Inserts a resume"""

        self.cur.execute(
            "INSERT INTO resume (user_email, AWS_link) VALUES (?, ?)", (user_email, AWS_link)
        )
        self.con.commit()
        logging.info(f"Resume inserted with AWS link {AWS_link}")

    def remove_resume(self, email):
        """Removes a resume from the resume table"""

        self.cur.execute(
            f"DELETE FROM resume WHERE user_email = '{email}'"
        )
        self.con.commit()
        logging.info("Resume removed from books table")

    def drop_resume_table(self):
        """Drops the resume table, only used in setup"""

        self.cur.execute("DROP TABLE resume")
        self.con.commit()
        logging.info("Dropping books table")

    def create_networking_table(self):
        """Creates the networking table, only used in setup"""
        # todo: more fields to be determined
        self.cur.execute(
            "CREATE TABLE networking (user_id TEXT, is_alum TEXT, list TEXT, PRIMARY KEY (user_id))"
        )
        self.con.commit()
        logging.info("Networking table created")

    def insert_user_to_networking(self, user_id, is_alum, list=""):
        """Inserts a user to the networking table"""
        # todo: not sure what list stands for, so it's defaulted to empty
        self.cur.execute(
            "INSERT INTO networking VALUES (?, ?, ?)", (user_id, is_alum, list)
        )
        self.con.commit()
        logging.info(f"User {user_id} inserted to networking table, alum={is_alum}")

    def drop_networking_table(self):
        """Drops the networking table, only used in setup"""

        self.cur.execute("DROP TABLE networking")
        self.con.commit()
        logging.info("Dropping networking table")
    
    def networking_is_alum(self, user_id):
        """Returns whether or not the user is an alum"""

        self.cur.execute(
            f"SELECT is_alum FROM networking WHERE user_id = '{user_id}'"
        )
        return self.cur.fetchone()[0]

    def get_last(self, user_id):
        """Returns the last user the user was matched with"""

        self.cur.execute(
            f"SELECT list FROM networking WHERE user_id = '{user_id}'"
        )
        return self.cur.fetchone()[0]