
from lib.modules.networkingmodule.networkingresponse import *
import requests
import json
import numpy as np
import os
from dotenv import load_dotenv
from pathlib import Path
from aiohttp import ClientError
from lib.modules.databasemodule.database import database
from constants import *
import logging

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

db = database.instance()

header = {'Authorization': 'Bearer ' + os.getenv("SLACK_BOT_TOKEN")}

def handle_extra_user(popped_user):
    popped_response = requests.post('https://slack.com/api/conversations.open', headers=header, data={"users": popped_user}).content
    popped_data = {'channel': json.loads(popped_response.decode('utf-8'))['channel']['id'], 'text': 'You are the odd one out... :cry:'}
    popped_response = requests.post('https://slack.com/api/chat.postMessage', data=popped_data, headers=header).content
    if not json.loads(popped_response.decode('utf-8'))['ok']:
        logging.log("Error: " + json.loads(popped_response.decode('utf-8'))['error'] )

def handle_connection(first_user, second_user):
    db.networking_update_last(first_user, second_user)
    curr_data = {'users': f"{first_user},{second_user}"}
    curr_response = requests.post('https://slack.com/api/conversations.open', data=curr_data, headers=header).content
    curr_data = {'channel': json.loads(curr_response.decode('utf-8'))['channel']['id'], 'text': networking_questions()[np.random.randint(0, len(networking_questions()))]}
    curr_response = requests.post('https://slack.com/api/chat.postMessage', data=curr_data, headers=header).content
    if not json.loads(curr_response.decode('utf-8'))['ok']:
        logging.log( "Error: " + json.loads(curr_response.decode('utf-8'))['error'] )

def main():
    try:
        # Gets list of users in Networking channel
        data = {'channel': CHANNEL_ID}
        rawusers = requests.get('https://slack.com/api/conversations.members', headers=header, params=data).content
        if not json.loads(rawusers.decode('utf-8'))['ok']:
            logging.log("Error: " + json.loads(rawusers.decode('utf-8'))['error'])
        users = json.loads(rawusers.decode('utf-8'))['members']
        users.remove(BOT_USER)
        # Determines if users are alum
        alum = []
        student = []
        for user in users:
            if db.networking_is_alum(user):
                alum.append(user)
            else:
                student.append(user)
        np.random.shuffle(alum)
        np.random.shuffle(student)
        if (len(alum) + len(student)) % 2 != 0:
            if len(alum) > 0:
                popped_user = alum.pop()
            else:
                popped_user = student.pop()
            handle_extra_user(popped_user)   
        while alum and student:
            curr_alum = alum[0]
            curr_student = student[0]
            while (db.get_last(curr_alum) == curr_student or db.get_last(curr_student) == curr_alum) and (len(alum) > 1 and len(student) > 1):
                np.random.shuffle(alum)
                np.random.shuffle(student)
                curr_alum = alum[0]
                curr_student = student[0]
            alum.pop()
            student.pop()
            handle_connection(curr_alum, curr_student)        
        combined_list = alum + student
        while combined_list:
            curr_user = combined_list[0]
            combined_list.pop()
            other_user = combined_list[0]
            while ((db.get_last(curr_user) == other_user or db.get_last(other_user) == curr_user) and len(combined_list) > 2):
                np.random.shuffle(combined_list)
                other_user = combined_list[0]
            combined_list.pop()
            handle_connection(curr_user, other_user)
    except ClientError as e:
        logging.log(e)

if __name__ == '__main__':
    main()