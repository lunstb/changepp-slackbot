"""This is the main script for IncludeBot

Here's some very relevant documentation:
MavenLink API - http://developer.mavenlink.com/

And also here's where you can see and manage slack apps - https://api.slack.com/apps"""

import logging

# Setup logging file
# This unfortunately needs to be done ahead of other imports bc/other (likely) use logging as well and
# likely also set a basicConfig. Given that basicConfig is ignored if called > 1 times this needs to be the first one
# https://stackoverflow.com/questions/20240464/python-logging-file-is-not-working-when-using-logging-basicconfig/63868063
from slack_sdk.socket_mode.response import SocketModeResponse

from lib.modules.moduletemplate import ModuleTemplate

logging.basicConfig(
    # filename='includebot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

from lib.modules.modulehelpers import check_admin
from lib.modules.databasemodule.databasemodule import DatabaseModule
from lib.modules.resumemodule.resumemodule import ResumeModule
from lib.modules.networkingmodule.networkingmodule import NetworkingModule
from lib.modules.librarymodule.librarymodule import LibraryModule
from lib.modules.internmodule.internmodule import InternModule
from threading import Event
from lib.constants import *
from lib.formulateresponse import *
from lib.setup import run_setup
from lib.slack_connect import client
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest

modules = [DatabaseModule(), ResumeModule(), NetworkingModule(), LibraryModule(), InternModule()]


def catch_basic_responses(msg: str, email, db: database):
    """This function """

    if msg.startswith('register '):
        return None

    if not db.check_user_exists(email):
        return account_not_set_up()

    if msg.startswith('admin '):
        if not check_admin(email, db):
            return denied_admin_access()
        if 'help' in msg:
            return admin_help()

    if 'help' == msg.strip():
        return help_response()


def pre_process(msg: str, email, db):
    is_admin = False
    if msg.startswith('admin '):
        is_admin = True

    return {
        "is_admin": is_admin,
    }


def process(client: SocketModeClient, req: SocketModeRequest):
    """This function handles different events from the Slack API and is the starting point for everything that IncludeBot does"""
    logging.info(f"Received request: {req}")
    
    if req.type == "events_api":
        # Acknowledge the request anyway
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        # To avoid an infinite loop of the bot responding itself
        if "bot_id" in req.payload["event"]:
            return

        # This retrieves the email of whoever sent the message
        email = client.web_client.users_info(user=req.payload["event"]["user"])[
            "user"]["profile"]["email"]

        logging.info(f"{email}->bot: {req.payload['event']['text']}")

        basic_response = catch_basic_responses(req.payload["event"]["text"], email, db)

        if basic_response is not None:
            response = basic_response
        else:
            process_results = pre_process(req.payload["event"]["text"], email, db)

            for module in modules:
                found_command = module.handle_input(client, req, db, process_results["is_admin"])
                if found_command:
                    return

            if 'admin' in req.payload["event"]["text"]:
                response = admin_not_recognized()
            else:
                response = did_not_understand()


        logging.info(f"bot->{email} response: {response}")
        client.web_client.chat_postMessage(channel=req.payload["event"]["channel"], text=response)


# Create db if it doesn't exist
run_setup()

# Connect to db
db = database.instance()

# Add a new listener to receive messages from Slack
# You can add more listeners like this
client.socket_mode_request_listeners.append(process)
# Establish a WebSocket connection to the Socket Mode servers
client.connect()

# Just not to stop this process
Event().wait()
