from typing import Dict
from lib.modules.databasemodule.databaseresponse import *
from lib.modules.modulehelpers import *
from lib.formulateresponse import *
from lib.modules.moduletemplate import ModuleTemplate
from slack_sdk.socket_mode import SocketModeClient

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
            elif commands[0] == "borrow_book":
                if len(commands) != 2:
                    return catch_incorrect_arguments(Commands.LIBRARY_BORROW_BOOK)

                return {
                        "command": Commands.LIBRARY_BORROW_BOOK,
                        "book_isbn": commands[1]
                    }
            elif commands[0] == "confirm":
                if len(commands) != 2:
                    return catch_incorrect_arguments(Commands.LIBRARY_CONFIRM_TRANSACTION)

                return {
                    "command": Commands.LIBRARY_CONFIRM_TRANSACTION,
                    "book_isbn": commands[1]
                }

            elif commands[0] == "cancel":
                if len(commands) != 2:
                    return catch_incorrect_arguments(Commands.LIBRARY_CANCEL_TRANSACTION)

                return {
                    "command": Commands.LIBRARY_CANCEL_TRANSACTION,
                    "book_isbn": commands[1]
                }
            elif commands[0] == "transaction_history":
                if len(commands) != 2:
                    return catch_incorrect_arguments(Commands.LIBRARY_TRANSACTION_HISTORY)

                return {
                    "command": Commands.LIBRARY_TRANSACTION_HISTORY,
                    "book_isbn": commands[1]
                }
            elif commands[0] == "help":
                if len(commands) != 1:
                    return catch_incorrect_arguments(Commands.LIBRARY_HELP)

                return {
                    "command": Commands.LIBRARY_HELP
                }


    def process_message(self, interpretation: dict, client: SocketModeClient, req, email, db: database, admin) -> Dict:
        # todo: don't allow donating a book twice by the same user, send a corresponding message
        if interpretation["command"] == Commands.LIBRARY_LIST_BOOKS:
            response = library_list_books(db)
        elif interpretation["command"] == Commands.LIBRARY_DONATE_BOOK:
            # Get name from ISBN using API
            isbn = extract_isbn_from_phone_number_format(interpretation["book_isbn"])
            name = get_book_name_from_isbn(isbn)
            if name is None:
                response = book_with_isbn_not_found(isbn)
            else:
                db.add_book(isbn, name, email)
                db.add_transaction_history_entry(isbn, f"{email} donated {name}")
                response = book_with_isbn_donated(isbn)

        elif interpretation["command"] == Commands.LIBRARY_BORROW_BOOK:
            isbn = extract_isbn_from_phone_number_format(interpretation["book_isbn"])
            book = db.get_book_by_isbn(isbn)
            if book is None:
                response = book_with_isbn_not_found(interpretation["book_isbn"])
            else:
                book_name = book[2]
                book_owner_email = book[4]

                db.request_book(isbn, email)
                response = book_with_isbn_requested(isbn, book_name)

                db.add_transaction_history_entry(isbn, f"{email} requested {book_name}")

                # send message to owner_email that the user has requested the book for approval
                user = client.web_client.users_lookupByEmail(email=book_owner_email)
                client.web_client.chat_postMessage(channel=user["user"]["id"], text=approve_request_of_book_with_isbn(isbn, email))

        elif interpretation["command"] == Commands.LIBRARY_CONFIRM_TRANSACTION:
            isbn = extract_isbn_from_phone_number_format(interpretation["book_isbn"])
            book = db.get_book_by_isbn(isbn)
            if book is None:
                response = book_with_isbn_not_found(isbn)
                return response 

            book_name = book[2]
            book_owner_email = book[4] 
            book_request_email = book[5]

            if book_owner_email != email:
                response = book_with_isbn_not_owned(interpretation["book_isbn"])
            elif book_request_email is None:
                response = book_with_isbn_not_requested(interpretation["book_isbn"])
            else:
                prev_owner_email = book_owner_email

                db.approve_book_request(isbn, book_request_email)
                response = book_borrow_request_with_isbn_approved(isbn, prev_owner_email)

                db.add_transaction_history_entry(isbn, f"{email} approved {book_name}")

                # send message to the new onwer that the book request has been approved
                user = client.web_client.users_lookupByEmail(email=book_request_email)
                client.web_client.chat_postMessage(channel=user["user"]["id"],
                text=response)

        elif interpretation["command"] == Commands.LIBRARY_CANCEL_TRANSACTION:
            isbn = extract_isbn_from_phone_number_format(interpretation["book_isbn"])
            book = db.get_book_by_isbn(isbn)
            if book is None:
                response = book_with_isbn_not_found(interpretation["book_isbn"])
                return response
            
            book_name = book[2]
            book_owner_email = book[4]
            book_request_email = book[5]

            if book_owner_email != email and book_request_email != email:
                response = book_with_isbn_not_owned_or_requested(interpretation["book_isbn"])
            elif book_request_email is None:
                response = book_with_isbn_not_requested(interpretation["book_isbn"])
            else:
                
                db.cancel_book_request(isbn)
                response = book_borrow_request_with_isbn_cancelled(isbn)

                db.add_transaction_history_entry(isbn, f"{email} cancelled {book_name}")

                # send message to the new onwer that the book request has been cancelled
                user = client.web_client.users_lookupByEmail(email=book_request_email)
                client.web_client.chat_postMessage(channel=user["user"]["id"],
                 text=response)

        elif interpretation["command"] == Commands.LIBRARY_TRANSACTION_HISTORY:
            isbn = extract_isbn_from_phone_number_format(interpretation["book_isbn"])
            book = db.get_book_by_isbn(isbn)
            if book is None:
                response = book_with_isbn_not_found(interpretation["book_isbn"])
            else:
                response = library_list_book_transactions(isbn)

        elif interpretation["command"] == Commands.LIBRARY_HELP:
            response = library_help()
            
        return response