"""This contains the enums for the different possible commands"""
from enum import Enum

class Commands(Enum):
    # These are all commands accessible to an admin user
    ADMIN_CREATE_USER = 1
    ADMIN_IS_ADMIN = 2
    ADMIN_DELETE_USER = 3
    ADMIN_UPDATE_ADMIN = 4
    ADMIN_VIEW_SCHEDULE = 5
    ADMIN_NOT_RECOGNIZED = 6
    ADMIN_HELP = 7
    ADMIN_LIST_USERS = 8

    # These are commands accessible to a non-admin user
    CREATE_USER = 9
    ADMIN_NOT_AUTHORIZED = 10
    DATE_SINGLE = 11
    DATE_RANGE = 12
    NOT_RECOGNIZED = 13
    HELP = 14
    INSTANCE_CREATE = 15
    INSTANCE_DESTROY = 16
    INSTANCE_EXTEND = 17
    INSTANCE_SET_PUBKEY = 18

    # And if the user is not set up:
    NOT_SET_UP = 19

    # If the user enters the wrong number of arguments for a command
    INCORRECT_ARGUMENTS = 20

    # sendsafely workspace commands
    RESOLVE_WORKSPACE = 21

    # Accessible commands using the library command
    LIBRARY_LIST_BOOKS = 22
    LIBRARY_DONATE_BOOK = 23
    LIBRARY_BORROW_BOOK = 24
    LIBRARY_CONFIRM_TRANSACTION = 25
    LIBRARY_CANCEL_TRANSACTION = 26
    LIBRARY_TRANSACTION_HISTORY = 27
    LIBRARY_HELP = 28

    # Accessible commands using the network command
    NETWORK_ADD_ME = 29
    NETWORK_HELP = 30

    # Accessible commands using the resume command
    LIST_RESUMES = 31
    ADD_RESUME = 32
    REMOVE_RESUME = 33
    RESUME_RESOURCES  = 34
    RESUME_HELP = 35

    # Accessible commands using the intern command
    INTERN_ADD_ME = 36
    INTERN_REMOVE = 37
    INTERN_LIST = 38
    INTERN_HELP = 39

command_dispatch = {
    Commands.ADMIN_CREATE_USER : "`admin create_user {slack email} {mavenlink email}` - This creates a user with the specified slack and mavenlink emails",
    Commands.ADMIN_IS_ADMIN : "`admin is_admin {email}` - This returns whether the specified email is an admin account or not",
    Commands.ADMIN_DELETE_USER : "`admin delete_user {slack email}` - This deletes the user with the specified slack and mavenlink emails.",
    Commands.ADMIN_UPDATE_ADMIN : "`admin update_admin {email} {true/false}` This makes the specified email an admin or not depending on whether a `true` or `false` is passed in",
    Commands.ADMIN_VIEW_SCHEDULE : "`admin view_schedule {email} {date range or single date}` - This returns the schedule of the user with the specified email.",
    Commands.ADMIN_HELP : "`admin help` - This returns a clarification on how to interact with the bot as an admin",
    Commands.ADMIN_LIST_USERS : "`admin list_users` - This returns a list of users with their admin status",

    Commands.HELP : "`help` - This command explains how to interact with the bot as a non-admin + a note for admins",
    
    # User commands
    Commands.CREATE_USER : "`register <first_name> <last_name> <graduation_year>` - This creates a user with the specified slack and all required credential fields",

    # Library commands
    Commands.LIBRARY_LIST_BOOKS : "`library list_books` - This returns a list of all the books that are available for rent",
    Commands.LIBRARY_DONATE_BOOK : "`library donate_book <ISBN>` - This allows you to donate a book to the library for people to borrow",
    Commands.LIBRARY_BORROW_BOOK : "`library borrow_book <ISBN>` - This allows you to borrow a book from the library and sets up a conversation with the owner to confirm",
    Commands.LIBRARY_CONFIRM_TRANSACTION : "`library confirm <ISBN>` - This allows book owner to confirm the borrow transaction",
    Commands.LIBRARY_CANCEL_TRANSACTION : "`library cancel <ISBN>` - This allows book owner or requester to cancel the borrow transaction",
    Commands.LIBRARY_TRANSACTION_HISTORY: "`library transaction_history <ISBN>` - This returns transactions related to a specific book",
    Commands.LIBRARY_HELP: "`library help` - This returns a clarification on how to interact with the bot's library module",


    # Network commands
    Commands.NETWORK_ADD_ME : "`network add_me` - This adds you to the network",
    Commands.NETWORK_HELP : "`network help` - This returns a clarification on how to interact with the bot's network module",

    # Resumes commands
    Commands.LIST_RESUMES : "`resume list` - This returns a list of all the resumes that are available to view",
    Commands.ADD_RESUME : "`resume add <attach_resume>` - This adds a resume to the database",
    Commands.REMOVE_RESUME : "`resume remove` - This removes your resume from the database",
    Commands.RESUME_RESOURCES : "`resume resources` - This returns a list of all the resources that are available to view",

    # Intern commands - see if when you add user, check if email in resume database and add url if so
    Commands.INTERN_ADD_ME : "`intern add {company}, {position}, {accepting_referrals?(true/false)}` - This adds an intern to the database. Remember to separate the arguments with commas!",
    Commands.INTERN_REMOVE : "`intern remove` - This removes your intern from the database",
    Commands.INTERN_LIST : "`intern list` - This returns a list of all the interns that are available to view",
    Commands.INTERN_HELP : "`intern help` - This returns a clarification on how to interact with the bot's intern module",
}

# TODO: put this back into the commands class
# for some reason I couldn't access the dictionary if it was in the enum namespace.
def explain_command(command):
    """ Explain the command """
    return command_dispatch[command]
