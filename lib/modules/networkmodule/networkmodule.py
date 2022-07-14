from typing import Dict
from lib.modules.databasemodule.databaseresponse import *
from lib.modules.modulehelpers import *
from lib.modules.moduletemplate import ModuleTemplate

class NetworkModule(ModuleTemplate):

    def interpret_message(self, msg: str, email, db, admin) -> Dict:
        commands = msg["text"].split()
        
        if commands[0] == "network":
            commands = commands[1:]
            if len(commands) == 0:
                return

            if commands[0] == "add_me":
                if len(commands) != 1:
                    return catch_incorrect_arguments(Commands.NETWORK_ADD_ME)

                return {
                    "command": Commands.NETWORK_ADD_ME
                }


    def process_message(self, interpretation, client, req, email, db: database, admin) -> Dict:
            if interpretation["command"] == Commands.NETWORK_ADD_ME:
                # todo: more clarification needed: fields to add to networking table
                db.insert_user_to_networking(email)
                response = network_add_me(email)

            return response
