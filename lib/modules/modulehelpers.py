import datefinder
import requests
from lib.commands import Commands


def get_dates(msg):
    """This function finds the dates in a message"""

    matches = datefinder.find_dates(msg)

    # convert response to an array
    dates = []
    for match in matches:
        dates.append(match)
    return dates

def get_book_name_from_isbn(isbn: str):
    """
    This function returns the book info from the isbn
    Example request:
    https://www.googleapis.com/books/v1/volumes?q=isbn:0984782869

    Docs: https://developers.google.com/books/docs/overview
    """
    
    # make a get request to google books api
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")
    json_response = response.json()

    if not json_response:
        return None

    return json_response["items"][0]["volumeInfo"]["title"]


def catch_incorrect_arguments(command):
    return {
        "command": Commands.INCORRECT_ARGUMENTS,
        "attempted": command
    }


def find_between(s, first, last):
    """This function returns the substring of text between the specified first and last"""

    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def get_slack_url(url):
    """ Because of how slack modifies URLs when a user sends them, this function just returns
    the url how it was pasted, it removes angle brackets and if it's super long it also does 
    the pipe substitution.
    """

    parts = url.split("|")
    if len(parts) != 2:
        return url[1:-1]

    return parts[0][1:-1]

def check_admin(slack_email, db):
    """This function checks whether the supplied slack email is an admin or not"""

    return db.check_user_is_admin(slack_email=slack_email) == 1

def clean_slack_message(text):
    """ The  purpose of this utility function is to remove 0xa0 characters from
    messages, these appear to keep urls in 1 line (to prevent linebreak), replace them
    with a space charactero
    """
    return text.replace('\xa0', ' ')
