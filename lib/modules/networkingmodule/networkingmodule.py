from typing import Dict
from pathlib import Path
from aiohttp import ClientError
from dotenv import load_dotenv
from lib.modules.modulehelpers import *
from lib.modules.moduletemplate import ModuleTemplate
from lib.modules.networkingmodule.networkingresponse import *
from lib.modules.databasemodule.database import database
import os
from constants import *
import requests
import json
from datetime import date
import numpy as np
from lib.formulateresponse import *


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class NetworkingModule(ModuleTemplate):

    def interpret_message(self, msg, email, db, admin) -> Dict:
        commands = msg["text"].split()

        if commands[0] == 'network':
            commands = commands[1:]
            if commands[0] == 'add_me':
                if len(commands) == 1:
                    return {
                        "command": Commands.NETWORK_ADD_ME
                    }
                else:
                    return catch_incorrect_arguments(Commands.NETWORK_ADD_ME)
            if commands[0] == 'help':
                return {
                    "command": Commands.NETWORK_HELP
                }
            else:
                return catch_incorrect_arguments(Commands.NETWORK_ADD_ME)
    def process_message(self, interpretation, client, req, email, db: database, admin) -> Dict:
        if interpretation["command"] == Commands.NETWORK_ADD_ME:
            user = req.payload['event']['user']
            try:
                data = {'channel': CHANNEL_ID, 'users': user}
                header = {'Authorization': 'Bearer ' + os.getenv("SLACK_BOT_TOKEN")}
                issues = requests.post(SLACK_URL + 'conversations.invite', data=data, headers=header).content
                if json.loads(issues.decode('utf-8'))['ok']:
                    db.insert_user_to_networking(user, True if db.get_user_year(email) <= date.today().year else False)
                return networking_success() if json.loads(issues.decode('utf-8'))['ok'] else networking_failure(json.loads(issues.decode('utf-8'))['error'])
            except ClientError as e:
                return e
        if interpretation["command"] == Commands.NETWORK_HELP:
            return network_help()
