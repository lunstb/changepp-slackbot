from typing import Dict
from lib.modules.databasemodule.databaseresponse import *
from lib.modules.modulehelpers import *
from lib.modules.moduletemplate import ModuleTemplate


class DatabaseModule(ModuleTemplate):

    def interpret_message(self, msg, email, db, admin, mavenlink_id) -> Dict:
        commands = msg["text"].split()

        if admin:
            commands = commands[1:]
            if len(commands) == 0:
                return

            if commands[0] == 'update_admin':
                if len(commands) != 3:
                    return catch_incorrect_arguments(Commands.ADMIN_UPDATE_ADMIN)

                email = commands[1]
                admin = True if commands[2] == "true" else False
                return {
                    "command": Commands.ADMIN_UPDATE_ADMIN,
                    "slack_email": email,
                    "is_admin": admin
                }
            elif commands[0] == 'is_admin':
                if len(commands) != 2:
                    return catch_incorrect_arguments(Commands.ADMIN_IS_ADMIN)

                email = commands[1]
                return {
                    "command": Commands.ADMIN_IS_ADMIN,
                    "slack_email": email
                }
            elif commands[0] == 'create_user':
                if len(commands) != 3:
                    return catch_incorrect_arguments(Commands.ADMIN_CREATE_USER)

                slack_email = commands[1]
                mavenlink_email = commands[2]
                return {
                    "command": Commands.ADMIN_CREATE_USER,
                    "slack_email": slack_email,
                    "mavenlink_email": mavenlink_email
                }
            elif commands[0] == 'delete_user':
                if len(commands) != 2:
                    return catch_incorrect_arguments(Commands.ADMIN_DELETE_USER)

                slack_email = commands[1]
                return {
                    "command": Commands.ADMIN_DELETE_USER,
                    "slack_email": slack_email
                }
            elif commands[0] == 'list_users':
                if len(commands) != 1:
                    return catch_incorrect_arguments(Commands.ADMIN_LIST_USERS)

                return {
                    "command": Commands.ADMIN_LIST_USERS
                }

    def process_message(self, interpretation, client, req, email, db, admin) -> Dict:
        response = None
        # if interpretation["command"] == Commands.ADMIN_CREATE_USER:
        #     parsed_slack_email = find_between(
        #         interpretation["slack_email"], '|', '>')
        #     if db.check_user_exists(slack_email=parsed_slack_email):
        #         response = user_already_exists(parsed_slack_email)
        #     else:
        #         parsed_mavenlink_email = find_between(
        #             interpretation["mavenlink_email"], '|', '>')
        #         if get_user_id(parsed_mavenlink_email) is None:
        #             response = no_such_maven(parsed_mavenlink_email)
        #         else:
        #             mavenlink_id = get_user_id(parsed_mavenlink_email)
        #             db.insert_user(slack_email=parsed_slack_email,
        #                            mavenlink_id=mavenlink_id, is_admin=False)
        #             response = user_created(parsed_slack_email)

        # elif interpretation["command"] == Commands.ADMIN_IS_ADMIN:
        #     parsed_slack_email = find_between(
        #         interpretation["slack_email"], '|', '>')
        #     if not db.check_user_exists(slack_email=parsed_slack_email):
        #         response = no_such_user(parsed_slack_email)
        #     else:
        #         response = admin_is_admin(
        #             interpretation["slack_email"],
        #             db.check_user_is_admin(slack_email=parsed_slack_email)
        #         )
        # elif interpretation["command"] == Commands.ADMIN_DELETE_USER:
        #     parsed_slack_email = find_between(
        #         interpretation["slack_email"], '|', '>')
        #     if not db.check_user_exists(slack_email=parsed_slack_email):
        #         response = no_such_user(parsed_slack_email)
        #     else:
        #         db.remove_user(slack_email=parsed_slack_email)
        #         response = admin_delete_user(parsed_slack_email)

        # elif interpretation["command"] == Commands.ADMIN_UPDATE_ADMIN:
        #     parsed_slack_email = find_between(
        #         interpretation["slack_email"], '|', '>')
        #     if not db.check_user_exists(slack_email=parsed_slack_email):
        #         response = no_such_user(parsed_slack_email)
        #     else:
        #         db.update_user_is_admin(
        #             slack_email=parsed_slack_email,
        #             is_admin=interpretation["is_admin"]
        #         )
        #         response = admin_update_admin(
        #             parsed_slack_email,
        #             interpretation["is_admin"]
        #         )
        # elif interpretation["command"] == Commands.ADMIN_LIST_USERS:
        #     response = admin_list_users(db)

        return response
