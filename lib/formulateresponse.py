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

    return "Your account has not yet been set up yet to interact with Include Bot, please contact an admin"


def denied_admin_access():
    """Returns the response for if a user tries to use an admin account but does not have proper access """

    return "You are not allowed to run that command because you do not have admin access. "


def help_response():
    """Returns the response for a user asking for help"""

    return "It seems like you asked for help on how to interact with me:\n" \
           f"- {explain_command(Commands.DATE_SINGLE)}\n" \
           f"- {explain_command(Commands.DATE_RANGE)}\n" \
           "- `admin {anything}` - This returns a message telling the user they are not an admin\n" \
           f"- {explain_command(Commands.INSTANCE_CREATE)}\n" \
           f"- {explain_command(Commands.INSTANCE_DESTROY)}\n" \
           f"- {explain_command(Commands.INSTANCE_EXTEND)}\n" \
           f"- {explain_command(Commands.INSTANCE_SET_PUBKEY)}\n" \
           f"- {explain_command(Commands.RESOLVE_WORKSPACE)}\n" \
           "- `{anything else}` - Any other message is unrecognized and will return a message clarifying how the bot failed to understand it.\n" \
           "If you're an admin type \"admin help\" for more information!"


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
