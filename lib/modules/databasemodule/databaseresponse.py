from lib.modules.databasemodule.database import database


def user_created(slack_email):
    """Returns the response for when a new user is created with the specified slack email"""

    return f"User created with the slack email {slack_email} as non admin"


def admin_is_admin(slack_email, is_admin):
    """Returns the response for checking if the user with the specified slack email is an admin"""

    return f"The user with the email {slack_email} {'is' if is_admin else 'is not'} an admin"


def admin_delete_user(slack_email):
    """Returns the response for deleting the user with the specified slack_email"""

    return f"The user with the email {slack_email} has been deleted"


def admin_update_admin(user_email, is_admin):
    return f"The user with the email {user_email} has been updated such that they are now {'' if is_admin else 'not'} an admin"


def user_already_exists(slack_email):
    """Returns the response for when someone tries to create a user with a slack_email that already has a correspoding user"""

    return f"A user with the email {slack_email} already exists so that user will not be created"

def no_such_user(user_email):
    """Returns the response for when an admin tries to interact with a user who does not yet exist in the database"""

    return f"You tried to enter a command and specified a user {user_email} but no such user exists"

def admin_list_users(db):
    """Generates and returns the response for when an admin asks for a list of users"""

    # users_db = db.get_users()
    # users_mavenlink = get_users()

    # mavenlink_to_name = {}
    # for user in users_mavenlink:
    #     mavenlink_to_name[users_mavenlink[user]["user_id"]
    #     ] = users_mavenlink[user]["full_name"]

    # response = "Here is a list of users with their admin status:\n"
    # for user in users_db:
    #     (mavenlink_id, email, is_admin) = user
    #     name = mavenlink_to_name[mavenlink_id]
    #     response += f"{name} with the slack email {email} {'is an admin' if (is_admin == 1) else 'is not an admin'}\n"

    return "Here is a list of users with their admin status:\n"

def book_with_isbn_not_owned_or_requested(isbn):
    """Returns the response for when a user tries to cancel borrow request on a book with an ISBN that is not owned or requested"""

    return f"I am sorry, but you did not request or own a book with ISBN {isbn}. Try again!"

def book_with_isbn_requested(isbn, name):
    """Returns the response for when a user requests a book with an ISBN that exists in our database"""

    return f"You have requested {name} with the ISBN {isbn}. Please wait for the owner to accept your request. \n" \
              f"You will be notified when the owner accepts your request\n" \
                f"To cancel your request: `library cancel {isbn}`"

def approve_request_of_book_with_isbn(isbn, requester_email):
    """Returns the response for when a book owner needs to approve a request for a book with an ISBN"""

    return f"Book with ISBN {isbn} has been requested by {requester_email}.\nPlease approve the request by typing `library confirm {isbn}`\n" \
                f"To cancel the request: `library cancel {isbn}`"

def book_with_isbn_not_requested(isbn):
    """Returns the response for when a user tries to approve a request for a book with an ISBN that has not been requested"""

    return f"Book with ISBN {isbn} has not been requested. Please try again :)"

def book_borrow_request_with_isbn_approved(isbn, owner_email):
    """Returns the response for when a book owner approves a request for a book with provided ISBN"""

    return f"Book with ISBN {isbn} has been approved by {owner_email}"

def book_with_isbn_not_owned(isbn):
    """Returns the response for when a user tries to confirm a book with an ISBN that does not exist in their library"""

    return f"I am sorry, but you do not own a book with ISBN {isbn}. Try the options below:\n- Try again with your book's" + \
    " ISBN\n- Type `library list_books` to see a list of books you own\n- Type `help library` for more information"

def book_borrow_request_with_isbn_cancelled(book_isbn):
    """Returns the response for when a user cancels a borrow request for a book with given ISBN"""

    return f"Book with ISBN {book_isbn} has been cancelled"

def book_with_isbn_not_found(isbn):
    """Returns the response for when a user tries to interact with a book with an ISBN that does not exist in our API"""

    return f"Sorry, I couldn't find book with ISBN: {isbn}. Please try again with a valid ISBN :("

def book_with_isbn_donated(isbn):
    """Returns the response for when a book is successfully donated"""

    return f"Book with ISBN {isbn} has been donated"

def library_list_books(db: database):
    """Generates and returns the response for when a user asks for a list of books"""

    books_db = db.get_books()

    if not books_db:
        return "There are no books in the library"

    response = "Here is a list of available books:\n"
    for book in books_db:
        (isbn, name, owner_email, last_transaction_date) = book
        response += f"\n>- {name} with the ISBN `{isbn}` currently owned by {owner_email} since `{last_transaction_date}`"

    return response

def library_list_book_transactions(db: database, book_isbn):
    """Generates and returns the response for when a user asks for a list of book transactions"""

    transactions_db = db.get_transaction_history(book_isbn)

    if not transactions_db:
        return "There are no book transactions in the library"

    response = "Here is a list of book transactions:\n"
    for transaction in transactions_db:
        (book_isbn, description, transaction_date) = transaction
        response += f"{book_isbn}: {description} on {transaction_date}\n"

def network_add_me(email):
    """Returns the response for when a user adds themselves to the network"""

    return f"You have been added to the network with the email {email}"
