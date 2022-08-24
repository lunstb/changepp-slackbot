from lib.modules.databasemodule.database import database

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

def list_interns(db: database, id=None):
    """Returns the response for when a user asks for a list of interns"""

    # Currently, we save the company ID, resume URL, and email in the database. The example says that 
    # the author's name is shown... how will we do this? Also, where will we store the company ID?
    # Should we allow users to delete interns?
    response = "Here is a list of interns:\n"

    interns_db = db.get_interns(id)
    if not interns_db and not id:
        return "There are no interns in the database"

    if not db.get_interns(id):
        return "There are no interns in the database with that email"

    response = "Here is a list of interns:\n"
    for intern in interns_db:
        (user_name, user_email, company, position, refs) = intern

        self_resumes = db.get_resumes(user_email)
        resume_link = ""
        print(self_resumes)

        if self_resumes:
            resume_link = self_resumes[0][1]
        else:
            resume_link = "No resume found."

        answer = ''
        resume_answer = ''
        if refs == "false":
            answer = 'not '
        if resume_link != "No resume found.":
            resume_answer = 'Their resume can be found at ' + resume_link + '.'
        response += f"{user_name} works at {company} as a {position} and is {answer}able to give references. " + resume_answer + f" Email them at {user_email}.\n"

    return response