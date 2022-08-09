from typing import Dict
from pathlib import Path
from aiohttp import ClientError
from dotenv import load_dotenv
from lib.modules.modulehelpers import *
from lib.modules.moduletemplate import ModuleTemplate
from lib.modules.networkingmodule.networkingresponse import *
from lib.modules.databasemodule.database import database
import os
import requests
import json
import numpy as np


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class NetworkingModule(ModuleTemplate):

    def interpret_message(self, msg, email, db, admin) -> Dict:
        commands = msg["text"].split()

        if commands[0] == 'networking':
            commands = commands[1:]
            if len(commands) == 0:
                return {
                    "command": Commands.NETWORK_ADD_ME
                }
            else:
                return catch_incorrect_arguments(Commands.NETWORK_ADD_ME)
        
        if commands[0] == 'talk':
            commands = commands[1:]
            if len(commands) == 0:
                return {
                    "command": Commands.NETWORK_TALK
                }
            else:
                return catch_incorrect_arguments(Commands.NETWORK_TALK)
    def process_message(self, interpretation, client, req, email, db: database, admin) -> Dict:
        if interpretation["command"] == Commands.NETWORK_ADD_ME:
            user = req.payload['event']['user']
            try:
                data = {'channel': 'C03QSC88Y4E', 'users': user}
                header = {'Authorization': 'Bearer ' + os.getenv("SLACK_BOT_TOKEN")}
                issues = requests.post('https://slack.com/api/conversations.invite', data=data, headers=header).content
                if json.loads(issues.decode('utf-8'))['ok']:
                    db.insert_user_to_networking(user, True if db.get_user_year(email) <= 2021 else False)
                return networking_success() if json.loads(issues.decode('utf-8'))['ok'] else networking_failure(json.loads(issues.decode('utf-8'))['error'])
            except ClientError as e:
                return networking_failure(e)
        if interpretation["command"] == Commands.NETWORK_TALK:
            try:
                header = {'Authorization': 'Bearer ' + os.getenv("SLACK_BOT_TOKEN")}
                # Gets list of users in Networking channel
                data = {'channel': 'C03QSC88Y4E'}
                rawusers = requests.get('https://slack.com/api/conversations.members', headers=header, params=data).content
                if not json.loads(rawusers.decode('utf-8'))['ok']:
                    return "Error: " + json.loads(rawusers.decode('utf-8'))['error']
                users = json.loads(rawusers.decode('utf-8'))['members']
                users.remove('U03QC4N6TDF')
                print(users)
                # Determines if users are alum
                alum = []
                student = []
                for user in users:
                    if db.networking_is_alum(user):
                        alum.append(user)
                    else:
                        student.append(user)
                if (len(alum) + len(student)) % 2 != 0:
                    popped_user = alum.pop()
                    popped_response = requests.post('https://slack.com/api/conversations.open', headers=header, data={"users": popped_user}).content
                    popped_data = {'channel': json.loads(curr_response.decode('utf-8'))['channel']['id'], 'text': 'You are the odd one out... :cry:'}
                    popped_response = requests.post('https://slack.com/api/chat.postMessage', data=curr_data, headers=header).content
                    if not json.loads(popped_response.decode('utf-8'))['ok']:
                        return "Error: " + json.loads(popped_response.decode('utf-8'))['error']          
                while alum and student:
                    curr_alum = alum[np.random.randint(0, len(alum))]
                    curr_student = student[np.random.randint(0, len(student))]
                    while (db.get_last(curr_alum) == curr_student or db.get_last(curr_student) == curr_alum) and (len(alum) > 1 and len(student) > 1):
                        curr_alum = alum[np.random.randint(0, len(alum))]
                        curr_student = student[np.random.randint(0, len(student))]
                    alum.remove(curr_alum)
                    student.remove(curr_student)
                    curr_data = {'channel': 'C03QSC88Y4E', 'users': [curr_alum, curr_student]}
                    curr_response = requests.post('https://slack.com/api/conversations.open', data=curr_data, headers=header).content
                    curr_data = {'channel': json.loads(curr_response.decode('utf-8'))['channel']['id'], 'text': networking_questions()[np.random.randint(0, len(networking_questions()))]}
                    curr_response = requests.post('https://slack.com/api/chat.postMessage', data=curr_data, headers=header).content
                    if not json.loads(curr_response.decode('utf-8'))['ok']:
                        return "Error: " + json.loads(curr_response.decode('utf-8'))['error']          
                while alum or student:
                    combined_list = alum + student
                    curr_user = combined_list[np.random.randint(0, len(combined_list))]
                    other_user = combined_list[np.random.randint(0, len(combined_list))]
                    while curr_user == other_user or ((db.get_last(curr_user) == other_user or db.get_last(other_user) == curr_user) and len(combined_list) > 3):
                        other_user = combined_list[np.random.randint(0, len(combined_list))]
                    combined_list.remove(curr_user)
                    combined_list.remove(other_user)
                    curr_data = {'channel': 'C03QSC88Y4E', 'users': [curr_user, other_user]}
                    curr_response = requests.post('https://slack.com/api/conversations.open', data=curr_data, headers=header).content
                    curr_data = {'channel': json.loads(curr_response.decode('utf-8'))['channel']['id'], 'text': networking_questions()[np.random.randint(0, len(networking_questions()))]}
                    curr_response = requests.post('https://slack.com/api/chat.postMessage', data=curr_data, headers=header).content
                    if not json.loads(curr_response.decode('utf-8'))['ok']:
                        return "Error: " + json.loads(curr_response.decode('utf-8'))['error']
                # new_response = requests.post('https://slack.com/api/conversations.open', headers=header, data={"users": f"{users[0]}"}).content
                # message_data = {"channel": json.loads(new_response.decode('utf-8'))["channel"]["id"], "text": networking_questions()[np.random.randint(len(networking_questions()))]}
                # message_response = requests.post('https://slack.com/api/chat.postMessage', headers=header, data=message_data).content
                # print(message_response)
            except ClientError as e:
                return e
#   Need to activate sandbox, work on algorithm, set up database... argh.