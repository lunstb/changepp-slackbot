
from lib.modules.networkingmodule.networkingresponse import *
import requests
import json
import numpy as np
import os
from dotenv import load_dotenv
from pathlib import Path
from aiohttp import ClientError
from lib.modules.databasemodule.database import database
db = database.instance()

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

if __name__ == '__main__':
    try:
        header = {'Authorization': 'Bearer ' + os.getenv("SLACK_BOT_TOKEN")}
        # Gets list of users in Networking channel
        data = {'channel': 'C03QSC88Y4E'}
        rawusers = requests.get('https://slack.com/api/conversations.members', headers=header, params=data).content
        if not json.loads(rawusers.decode('utf-8'))['ok']:
            print("Error: " + json.loads(rawusers.decode('utf-8'))['error'])
        users = json.loads(rawusers.decode('utf-8'))['members']
        users.remove('U03QC4N6TDF')
        # Determines if users are alum
        alum = []
        student = []
        for user in filter(lambda x: x != 'U03THUJ5Y2X', users):
            if db.networking_is_alum(user):
                alum.append(user)
            else:
                student.append(user)
        if (len(alum) + len(student)) % 2 != 0:
            if len(alum) > 0:
                popped_user = alum.pop()
            else:
                popped_user = student.pop()
            popped_response = requests.post('https://slack.com/api/conversations.open', headers=header, data={"users": popped_user}).content
            popped_data = {'channel': json.loads(popped_response.decode('utf-8'))['channel']['id'], 'text': 'You are the odd one out... :cry:'}
            popped_response = requests.post('https://slack.com/api/chat.postMessage', data=popped_data, headers=header).content
            if not json.loads(popped_response.decode('utf-8'))['ok']:
                print("Error: " + json.loads(popped_response.decode('utf-8'))['error'] )         
        while alum and student:
            curr_alum = alum[np.random.randint(0, len(alum))]
            curr_student = student[np.random.randint(0, len(student))]
            while (db.get_last(curr_alum) == curr_student or db.get_last(curr_student) == curr_alum) and (len(alum) > 1 and len(student) > 1):
                curr_alum = alum[np.random.randint(0, len(alum))]
                curr_student = student[np.random.randint(0, len(student))]
            alum.remove(curr_alum)
            student.remove(curr_student)
            curr_data = {'users': f"{curr_alum},{curr_student}"}
            curr_response = requests.post('https://slack.com/api/conversations.open', data=curr_data, headers=header).content
            curr_data = {'channel': json.loads(curr_response.decode('utf-8'))['channel']['id'], 'text': networking_questions()[np.random.randint(0, len(networking_questions()))]}
            curr_response = requests.post('https://slack.com/api/chat.postMessage', data=curr_data, headers=header).content
            if not json.loads(curr_response.decode('utf-8'))['ok']:
                print( "Error: " + json.loads(curr_response.decode('utf-8'))['error'] )         
        combined_list = alum + student
        while combined_list:
            curr_user = combined_list[np.random.randint(0, len(combined_list))]
            other_user = combined_list[np.random.randint(0, len(combined_list))]
            while curr_user == other_user or ((db.get_last(curr_user) == other_user or db.get_last(other_user) == curr_user) and len(combined_list) > 3):
                other_user = combined_list[np.random.randint(0, len(combined_list))]
            print (curr_user, other_user)
            combined_list.remove(curr_user)
            combined_list.remove(other_user)
            curr_data = {'users': f'{curr_user},{other_user}'}
            print(curr_data)
            curr_response = requests.post('https://slack.com/api/conversations.open', data=curr_data, headers=header).content
            curr_data = {'channel': json.loads(curr_response.decode('utf-8'))['channel']['id'], 'text': networking_questions()[np.random.randint(0, len(networking_questions()))]}
            print(json.loads(curr_response.decode('utf-8')))
            curr_response = requests.post('https://slack.com/api/chat.postMessage', data=curr_data, headers=header).content
            print(json.loads(curr_response.decode('utf-8')))
            if not json.loads(curr_response.decode('utf-8'))['ok']:
                print( "Error: " + json.loads(curr_response.decode('utf-8'))['error'])
        # new_response = requests.post('https://slack.com/api/conversations.open', headers=header, data={"users": f"{users[0]}"}).content
        # message_data = {"channel": json.loads(new_response.decode('utf-8'))["channel"]["id"], "text": networking_questions()[np.random.randint(len(networking_questions()))]}
        # message_response = requests.post('https://slack.com/api/chat.postMessage', headers=header, data=message_data).content
        # print(message_response)
    except ClientError as e:
        print(e)