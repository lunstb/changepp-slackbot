from typing import Dict
from pathlib import Path
from aiohttp import ClientError
from dotenv import load_dotenv
from lib.modules.modulehelpers import *
from lib.modules.moduletemplate import ModuleTemplate
from lib.modules.internmodule.internresponse import *
from lib.modules.databasemodule.database import database
from lib.formulateresponse import *


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class InternModule(ModuleTemplate):

    def interpret_message(self, msg, email, db, admin) -> Dict:
        commands = msg["text"].split()

        if commands[0] == 'intern':
            commands = commands[1:]
            if commands[0] == 'add':
                if len(commands) == 4:
                    return {
                        "command": Commands.INTERN_ADD_ME,
                        "company": commands[1],
                        "position": commands[2],
                        "accepting_refs": commands[3]
                    }
                else:
                    return catch_incorrect_arguments(Commands.INTERN_ADD_ME)
            if commands[0] == 'remove':
                if len(commands) == 1:
                    return {
                        "command": Commands.INTERN_REMOVE
                    }
                else:
                    return catch_incorrect_arguments(Commands.INTERN_REMOVE)
            if commands[0] == 'list':
                if len(commands) == 1:
                    return {
                        "command": Commands.INTERN_LIST,
                    }
                else:
                    return catch_incorrect_arguments(Commands.INTERN_LIST)
            if commands[0] == 'help':
                return {
                    "command": Commands.INTERN_HELP
                }
    
    def process_message(self, interpretation, client, req, email, db: database, admin) -> Dict:
        if interpretation["command"] == Commands.INTERN_ADD_ME:
            db.insert_intern(email, interpretation["company"], interpretation["position"], interpretation["accepting_refs"])
            return added_intern()
        if interpretation["command"] == Commands.INTERN_REMOVE:
            db.remove_intern(email)
            return removed_intern()
        if interpretation["command"] == Commands.INTERN_LIST:
            return list_interns(db, req.payload['event']['channel'])
        if interpretation["command"] == Commands.INTERN_HELP:
            return intern_help()