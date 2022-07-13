from typing import Dict
from lib.modules.resumemodule.resumeresponse import *
from lib.modules.modulehelpers import *
from lib.modules.moduletemplate import ModuleTemplate
import boto3

s3 = boto3.client('s3')

class DatabaseModule(ModuleTemplate):

    def interpret_message(self, msg, email, db, admin) -> Dict:
        commands = msg["text"].split()

        if commands[0] == 'internship':
            commands = commands[1:0]
            if len(commands) == 0:
                return

            if commands[0] == 'list_resumes':
                if len(commands) > 2:
                    return catch_incorrect_arguments(Commands.INTERN_LIST_RESUMES)
                
                return {
                    "command": Commands.INTERN_LIST_RESUMES,
                    "id": commands[1] if len(commands) == 2 else None
                }
            
            if commands[0] == 'add_resume':
                if len(commands) != 2:
                    return catch_incorrect_arguments(Commands.INTERN_ADD_RESUME)
                return {
                    "command": Commands.INTERN_ADD_RESUME,
                    "resume": commands[1]
                }
            
            # if commands[0] == 'remove_resume':
            # USE THIS IF WE WANT TO ALLOW REMOVING RESUMES... MAYBE ONLY ON ADMIN LEVEL?
            #     if len(commands) != 2:
            #         return catch_incorrect_arguments(Commands.INTERN_REMOVE_RESUME)
            #     return {
            #         "command": Commands.INTERN_REMOVE_RESUME,
            #         "id": commands[1]
            #     }

    def process_message(self, interpretation, client, req, email, db: database, admin) -> Dict:
        response = None

        if interpretation["command"] == Commands.INTERN_LIST_RESUMES:
            response = list_resumes(db, interpretation["id"])
        if interpretation["command"] == Commands.INTERN_ADD_RESUME:
            try:
                s3.upload_fileobj(interpretation["resume"], "changeppresumebot", email)
                db.insert_resume(email, f"https://changeppresumebot.s3.amazonaws.com/{email}")
                response = resume_added(email)
            except ClientError as e:
                response = resume_added(e.response['Error']['Message'])
        return response
