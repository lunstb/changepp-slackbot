from abc import ABC, abstractmethod
import logging
from typing import Dict

from lib.commands import Commands
from lib.formulateresponse import *
from slack_sdk.socket_mode import SocketModeClient

class ModuleTemplate(ABC):
    def handle_input(self, client: SocketModeClient, req, db, admin) -> bool:
        """"""

        # This retrieves the email of whoever sent the message
        email = client.web_client.users_info(user=req.payload["event"]["user"])[
            "user"]["profile"]["email"]

        logging.info(f"{email}->bot: {req.payload['event']['text']}")

        # Interpret and respond to the message
        interpretation = self.interpret_message(
            req.payload["event"],
            email,
            db,
            admin,
        )

        if interpretation is None:
            # Command was not found in the interpretation, just exit
            return False

        if interpretation["command"] == Commands.INCORRECT_ARGUMENTS:
            response = incorrect_arguments(interpretation["attempted"])
        else:
            response = self.process_message(interpretation, client, req, email, db, admin)

        logging.info(f"{email}->bot message interpreted as: {interpretation['command']}")

        if response is None:
            # This means that a recognized command with an interpretation does not have a given response, code isn't complete
            raise Exception(f"Recognized command \"{interpretation['command']}\" does not have programmed response in its module")

        logging.info(f"bot->{email} response: {response}")
        client.web_client.chat_postMessage(channel=req.payload["event"]["channel"], text=response)
        return True

    @abstractmethod
    def interpret_message(self, msg, email, db, admin, mavenlink_id) -> Dict:
        pass

    @abstractmethod
    def process_message(self, interpretation, client, req, email, db, admin) -> Dict:
        pass
