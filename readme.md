# Lauren Bot

Lauren is an internal tool accessible by all change++ members using the slack messaging app. She is a bot that can be used to perform various tasks such as: 
* Exchanging books using the `Library Module`
* Sharing and vewing resumes using the `Resume Module`
* Internship networking that shows companies and referrals using the `Intern Module`
* Setting app biweekly discussion chats by randomly pairing members using the `Networking Module`
* and more to come!

This was all accomplished thanks to Berke Lunstad, Kyle Burgess, and myself.

# Contents
* [Help](#help)
* [Library Module](#library-module)
* [Resume Module](#resume-module)
* [Intern Module](#intern-module)
* [Networking Module](#networking-module)

# How to use Lauren
The bot should be visible in the bottom part of our slack’s side navigation, in the “Apps” section. You have to open a direct message with the bot to interact with her. You can do this by clicking on the “>” button next to the "Apps" section in the bottom left corner of the side navigation and selecting “Lauren” from the list of apps.

## Help
If you ever need help with the bot, you can type `help` in a direct message with the bot. This will return a list of all the modules and their respective help commands.

## Library Module
*Note*: All commands are case sensitive, so make sure to use the exact command as shown below.

Here are all of the command options for interacting with the library module:
- `library list_books` - This returns a list of all the books that are available for rent
- `library donate_book <ISBN>` - This allows you to donate a book to the library for people to borrow
- `library borrow_book <ISBN>` - This allows you to borrow a book from the library and sets up a conversation with the owner to confirm
- `library confirm <ISBN>` - This allows book owner to confirm the borrow transaction
- `library cancel <ISBN>` - This allows book owner or requester to cancel the borrow transaction
- `library transaction_history <ISBN>` - This returns transactions related to a specific book
- `library help` - This returns a clarification on how to interact with the bot's library module

## Resume Module

Here are all of the command options for interacting with the resume module:
- `resume list` - This returns a list of all the resumes that are available to view
- `resume add <attach_resume>` - This adds a resume to the database. To add your resume, you can either drop it into the chat or attach it as a file with the command.
Note: You are encouraged not to include your GPA in your resume.
- `resume remove` - This removes your resume from the database
- `resume resources` - This returns a list of all the resources that are available to view

## Intern Module

Here are all of the command options for interacting with the intern module:
- `intern add {company}, {position}, {accepting_referrals?(true/false)}` - This adds an intern to the database. **Remember to separate the arguments with commas!**
- `intern remove` - This removes your intern from the database
- `intern list` - This returns a list of all the interns that are available to view
- `intern help` - This returns a clarification on how to interact with the bot's intern module

## Networking Module
**Note**: This module is currently in beta testing.