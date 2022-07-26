from typing import Dict

import boto3
import requests
import io
from botocore.exceptions import ClientError
from lib.modules.modulehelpers import *
from lib.modules.moduletemplate import ModuleTemplate
from lib.modules.resumemodule.resumeresponse import *
import os
from pathlib import Path
from dotenv import load_dotenv
import PyPDF2

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


s3 = boto3.client('s3')

class ResumeModule(ModuleTemplate):

    def interpret_message(self, msg, email, db, admin) -> Dict:
        commands = msg["text"].split()

        if commands[0] == 'resume':
            commands = commands[1:]
            if len(commands) == 0:
                return

            if commands[0] == 'list_resumes':
                if len(commands) > 2:
                    return catch_incorrect_arguments(Commands.LIST_RESUMES)
                
                return {
                    "command": Commands.LIST_RESUMES,
                    "id": commands[1] if len(commands) == 2 else None
                }
            
            if commands[0] == 'add_resume':
                if len(commands) != 1:
                    return catch_incorrect_arguments(Commands.ADD_RESUME)
                return {
                    "command": Commands.ADD_RESUME
                }
            
            if commands[0] == 'remove_resume':
                if len(commands) != 1:
                    return catch_incorrect_arguments(Commands.REMOVE_RESUME)
                return {
                    "command": Commands.REMOVE_RESUME
                }

    def process_message(self, interpretation, client, req, email, db: database, admin) -> Dict:
        response = None

        if interpretation["command"] == Commands.LIST_RESUMES:
            response = list_resumes(db, interpretation["id"])
        if interpretation["command"] == Commands.ADD_RESUME:
            try:
                headers = {'Authorization': 'Bearer ' + os.getenv("SLACK_BOT_TOKEN")}
                content = requests.get(req.payload['event']['files'][0]['url_private'], headers=headers, allow_redirects=True).content
                # Check if PDF is valid:
                PyPDF2.PdfFileReader(io.BytesIO(content))
                s3.upload_fileobj(io.BytesIO(content), "changeppresumebot", f"{email}.pdf")
                if not db.get_resumes(email):
                    db.insert_resume(email, f"https://changeppresumebot.s3.amazonaws.com/{email}.pdf")
                response = resume_added()
            except (ClientError, PyPDF2.errors.PdfReadError) as e:
                response = resume_not_added(e.response['Error']['Message'] if hasattr(e, 'response') else "Invalid PDF")
        if interpretation["command"] == Commands.REMOVE_RESUME:
            if not db.get_resumes(email):
                response = resume_not_removed()
            try:
                s3.delete_object(Bucket="changeppresumebot", Key=email)
                db.remove_resume(email)
                response = resume_removed()
            except ClientError as e:
                response = resume_not_removed(e.response['Error']['Message'])
        return response
