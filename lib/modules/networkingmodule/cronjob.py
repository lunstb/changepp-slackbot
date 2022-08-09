from networkingresponse import *
import requests
import json
import numpy as np

if __name__ == '__main__':
    print("Oh no...")
    header = {'Authorization': 'Bearer xoxb-3815502494722-3828158231457-FgjsbBbZbzX6DmSTZ4QyGyvg'}
    data = {'channel': 'C03QSC88Y4E'}
    rawusers = requests.get('https://slack.com/api/conversations.members', headers=header, params=data).content
    if not json.loads(rawusers.decode('utf-8'))['ok']:
        print("Error: " + json.loads(rawusers.decode('utf-8'))['error'])
    users = json.loads(rawusers.decode('utf-8'))['members']
    print(users)
    new_response = requests.post('https://slack.com/api/conversations.open', headers=header, data={"users": f"{users[0]}"}).content
    message_data = {"channel": json.loads(new_response.decode('utf-8'))["channel"]["id"], "text": networking_questions()[np.random.randint(len(networking_questions()))]}
    message_response = requests.post('https://slack.com/api/chat.postMessage', headers=header, data=message_data).content
    print(message_response)