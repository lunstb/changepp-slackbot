from typing import Dict
from lib.modules.databasemodule.databaseresponse import *
from lib.modules.modulehelpers import *
from lib.modules.moduletemplate import ModuleTemplate


class LibraryModule(ModuleTemplate):

    def interpret_message(self, msg: str, email, db, admin) -> Dict:
        commands = msg["text"].split()

        if commands[0] == "library":
            commands = commands[1:]
            if len(commands) == 0:
                return

            if commands[0] == "list_books":
                if len(commands) != 1:
                    return catch_incorrect_arguments(Commands.LIBRARY_LIST_BOOKS)

                return {
                    "command": Commands.LIBRARY_LIST_BOOKS
                }
            elif commands[0] == "donate_book":
                if len(commands) != 2:
                    return catch_incorrect_arguments(Commands.LIBRARY_DONATE_BOOK)

                return {
                    "command": Commands.LIBRARY_DONATE_BOOK,
                    "book_isbn": commands[1]
                }


    def process_message(self, interpretation, client, req, email, db: database, admin) -> Dict:
        if interpretation["command"] == Commands.LIBRARY_LIST_BOOKS:
            response = library_list_books(db)
        elif interpretation["command"] == Commands.LIBRARY_DONATE_BOOK:
            # Get name from ISBN using API
            isbn = interpretation["book_isbn"]
            name = get_book_name_from_isbn(isbn)
            if name is None:
                response = book_with_isbn_not_found(isbn)
            else:
                db.add_book(email, isbn, name)
                response = book_with_isbn_donated(isbn)

        return response