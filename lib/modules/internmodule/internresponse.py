from lib.modules.databasemodule.database import database
import csv
from pathlib import Path
from dotenv import load_dotenv
import os
import requests
import json

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

def added_intern():
    """Returns the response for when an intern is successfully added"""

    return "Intern added."

def not_added_intern(error):
    """Returns the response for when an intern is not successfully added"""

    return "Intern not added: " + error

def removed_intern():
    """Returns the response for when an intern is successfully removed"""

    return "Intern removed."

def not_removed_intern(error):
    """Returns the response for when an intern is not successfully removed"""

    return "Intern not removed: " + error

def list_interns(db: database, channel_id):
    """Returns a csv with intern data"""

    all_intern_info = db.return_all_interns()
    with open("out.csv", "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Name', 'Email', 'Company', 'Position', 'Able to Give Referrals?', 'Resume'])
        for i in all_intern_info:
            self_resumes = db.get_resumes(i[1])
            resume_link = ""
            if self_resumes:
                resume_link = self_resumes[0][1]
            else:
                resume_link = "N/A"
            csv_writer.writerow([i[0], i[1], i[2], i[3], i[4], resume_link])
    my_file = {'file' : ('out.csv', open('out.csv', 'rb'), 'csv')}
    payload = {
        'filename': 'intern_data.csv',
        'channels': channel_id
        }
    r = requests.post("https://slack.com/api/files.upload", params=payload, files=my_file, headers={'Authorization': 'Bearer ' + os.getenv("SLACK_BOT_TOKEN")}).content
    if json.loads(r.decode('utf-8'))["ok"]:
        return

    return "Something has gone wrong :cry:"
    