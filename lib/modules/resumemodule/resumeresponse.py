from lib.modules.databasemodule.database import database

def resume_added():
    """Returns the response for when a resume is successfully added"""

    return "Resume added."

def resume_not_added(error):
    """Returns the response for when a resume is not successfully added"""

    return "Resume not added: " + error

def resume_removed():
    """Returns the response for when a resume is successfully removed"""

    return "Resume removed."

def resume_not_removed(error):
    """Returns the response for when a resume is not successfully removed"""

    return "Resume not removed: " + error

def list_resumes(db: database, id=None):

    # Currently, we save the company ID, resume URL, and email in the database. The example says that 
    # the author's name is shown... how will we do this? Also, where will we store the company ID?
    # Should we allow users to delete resumes?

    """Returns the response for when a user asks for a list of resumes"""

    response = "Here is a list of resumes:\n"
    
    resumes_db = db.get_resumes(id)
    if not resumes_db and not id:
        return "There are no resumes in the database"

    if not db.get_resumes(id):
        return "There are no resumes in the database with that email"

    response = "Here is a list of resumes:\n"
    for resume in resumes_db:
        (email, url) = resume
        response += f"{email}'s Resume: {url}\n"
    
    return response