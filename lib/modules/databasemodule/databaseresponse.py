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
