"""This script formulates the responses that are then sent in messages"""

from lib.commands import Commands, explain_command

from lib.modules.databasemodule.database import *

# db = database.instance()


def incorrect_arguments(attempted):
    """Returns the response for when the incorrect number of arguments are specified when attempting a command"""

    return f"It seems like you entered the wrong number of commands. Here's a reminder on how to use that command:\n {explain_command(attempted)}"

def invalid_book_isbn():
    """Returns the response for when an invalid isbn is entered"""

    return "The ISBN you entered is invalid, please try again"


def account_not_set_up():
    """Returns the response for any user whose account is not setup (is not in the database) """

    return "Your account has not been set up yet! Let's get you started.\n Send the following command and substitute in your credentials:\n`register <first_name> <last_name> <graduation_year>`\n*Example:* \n>register Salomon Dushimirimana 2024 \n"



def denied_admin_access():
    """Returns the response for if a user tries to use an admin account but does not have proper access """

    return "You are not allowed to run that command because you do not have admin access. "


def help_response():
    """Returns the response for a user asking for help"""

    return "It seems like you asked for help on how to interact with me.\n" \
            "Below are different commands on how to interact with the supported admin, library, network, resume, and internship functionalities: \n" \
            f"- Type `library help` for library module help commands.\n" \
            f"- Type `resume help` for resume module help commands.\n" \
            f"- Type `intern help` for resume module help commands.\n" \
            f"- Type `network help` for network module help commands.\n" \
           "- `{anything else}` Any other message is unrecognized and will return a message clarifying how the bot failed to understand it.\n" \
           "If you're an admin type `admin help` for more information!"

def library_help():
    """Returns the response for when a user asks for help with the library module"""

    return f"Here are all of the command options for interacting with the library module:\n" \
        f"- {explain_command(Commands.LIBRARY_LIST_BOOKS)}\n" \
        f"- {explain_command(Commands.LIBRARY_DONATE_BOOK)}\n" \
        f"- {explain_command(Commands.LIBRARY_BORROW_BOOK)}\n" \
        f"- {explain_command(Commands.LIBRARY_CONFIRM_TRANSACTION)}\n" \
        f"- {explain_command(Commands.LIBRARY_CANCEL_TRANSACTION)}\n" \
        f"- {explain_command(Commands.LIBRARY_TRANSACTION_HISTORY)}\n" \
        f"- {explain_command(Commands.LIBRARY_HELP)}\n" \

def network_help():
    """Returns the response for when a user asks for help with the network module"""

    return  f"*Note:* Still in development + Testing.\n" \
    f"Here are all of the command options for interacting with the network module:\n" \
        f"- {explain_command(Commands.NETWORK_ADD_ME)}\n" \
        f"- {explain_command(Commands.NETWORK_HELP)}\n" \

def resume_help():
    """Returns the response for when a user asks for help with the resume module"""

    return f"Here are all of the command options for interacting with the resume module:\n" \
        f"- {explain_command(Commands.LIST_RESUMES)}\n" \
        f"- {explain_command(Commands.ADD_RESUME)}\n" \
        f"_*Note:* You are encouraged not to include your *GPA* in your resume._\n"\
        f"- {explain_command(Commands.REMOVE_RESUME)}\n" \
        f"- {explain_command(Commands.RESUME_RESOURCES)}\n" \

def intern_help():
    """Returns the response for when a user asks for help with the intern module"""

    return f"Here are all of the command options for interacting with the intern module:\n" \
        f"- {explain_command(Commands.INTERN_ADD_ME)}\n" \
        f"- {explain_command(Commands.INTERN_REMOVE)}\n" \
        f"- {explain_command(Commands.INTERN_LIST)}\n" \
        f"- {explain_command(Commands.INTERN_HELP)}\n" \

def welcome_message():
    """Returns the response for when a user first connects to the bot"""

    return "Welcome to change++!\n" \
        "My name is Laurenbot, and I am here to assist you through various functionalities mentioned below.\n" \
        "- `Networking`: Once you opt in, you'll be paired with another change++ member on a once-in-two-weeks" \
            " basis with random networking prompts to discuss. Text `Networking help` for more.\n" \
        "- `Resume`: View and access shared resumes from fellow members, and you can also share your own resume. " \
            "Text `Resume help` for more.\n"\
        "- `Library`: Donate and exchange books with fellow members. Text `library help` for more.\n"\
        "Type `help` to see a list of commands that I understand.\n" \

def did_not_understand():
    """Returns the response for when a non-admin message is not understood."""

    return "Command not understood. Please type \"help\" for information on what I can do!"

def admin_not_recognized():
    """Returns the response for when an admin messaege is not understood"""

    return f"The command that you entered as an admin was not recognized, try asking for help by typing `admin help`"


def admin_help():
    """Returns the response for when an admin user asks for help"""

    return f"Interacting with the Include Bot as an admin requires a lot of precision in commands. Here are all of the command options:\n" \
           f"- {explain_command(Commands.ADMIN_UPDATE_ADMIN)}\n" \
           f"- {explain_command(Commands.ADMIN_CREATE_USER)}\n" \
           f"- {explain_command(Commands.ADMIN_DELETE_USER)}\n" \
           f"- {explain_command(Commands.ADMIN_IS_ADMIN)}\n" \
           f"- {explain_command(Commands.ADMIN_VIEW_SCHEDULE)}\n" \
           f"- {explain_command(Commands.ADMIN_HELP)}\n" \
           f"- {explain_command(Commands.ADMIN_LIST_USERS)}"
