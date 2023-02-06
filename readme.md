# Lauren Bot

Lauren is an internal tool developed by Kyle Burgess, Salomon Dushimirimana, and Berke Lunstad. She is accessible by all change++ members using the slack messaging app. She is a bot that can be used to perform various tasks such as: 
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

If "Laurenbot" doesn't show up in the apps section, click the "+" button that shows up when you hover over the "apps" section. Select it in the list of apps, or search for it if it doesn't show up there. This will add the app to your workspace, and you can proceed as directed above.

## Help
If you ever need help with the bot, you can type `help` in a direct message with the bot. This will return a list of all the modules and their respective help commands.

## Library Module
*Note*: All commands are case sensitive, so make sure to use the exact command as shown below.

Here are all of the command options for interacting with the library module:
- `library list_books` - This returns a list of all the books that are available for rent
<img width="607" alt="Screen Shot 2023-01-22 at 3 17 03 PM" src="https://user-images.githubusercontent.com/63796975/213941059-b88c5c67-028d-4a82-8cc8-1eb81047dcab.png">

- `library donate_book <ISBN>` - This allows you to donate a book to the library for people to borrow
- `library borrow_book <ISBN>` - This allows you to borrow a book from the library and sets up a conversation with the owner to confirm
- `library confirm <ISBN>` - This allows book owner to confirm the borrow transaction
- `library cancel <ISBN>` - This allows book owner or requester to cancel the borrow transaction
- `library transaction_history <ISBN>` - This returns transactions related to a specific book
- `library help` - This returns a clarification on how to interact with the bot's library module

## Resume Module

Here are all of the command options for interacting with the resume module:
- `resume list` - This returns a list of all the resumes that are available to view
<img width="613" alt="Screen Shot 2023-01-22 at 3 18 43 PM" src="https://user-images.githubusercontent.com/63796975/213941075-47acd9ec-643a-4569-a602-1d4b9235eb3f.png">

- `resume add <attach_resume>` - This adds your resume to the database. To add your resume, you can either drop it into the chat or attach it as a file with the command.
Note: You are encouraged not to include your GPA in your resume.
<img width="610" alt="Screen Shot 2023-01-22 at 3 23 42 PM" src="https://user-images.githubusercontent.com/63796975/213941196-74f7fa75-515d-46c6-b3f2-e7baa4c49614.png">

- `resume remove` - This removes your resume from the database
<img width="617" alt="Screen Shot 2023-01-22 at 3 21 59 PM" src="https://user-images.githubusercontent.com/63796975/213941134-c040e800-f555-4062-be28-bbd9fa3cee7b.png">

- `resume resources` - This returns a list of all the resources that are available to view (**Note:** Resources not added yet)

## Intern Module

Here are all of the command options for interacting with the intern module:
- `intern add {company}, {position}, {accepting_referrals?(true/false)}` - This adds an intern to the database. **Remember to separate the arguments with commas!**
<img width="915" alt="Screen Shot 2023-01-22 at 3 31 36 PM" src="https://user-images.githubusercontent.com/63796975/213941515-be8547a6-b71d-4537-8733-056408a4ca83.png">

- `intern remove` - This removes your intern from the database
<img width="920" alt="Screen Shot 2023-01-22 at 3 30 20 PM" src="https://user-images.githubusercontent.com/63796975/213941451-24394f78-3ecc-43b6-8e78-3d76e8eb111a.png">

- `intern list` - This returns a list of all the interns that are available to view
<img width="912" alt="Screen Shot 2023-01-22 at 3 29 34 PM" src="https://user-images.githubusercontent.com/63796975/213941417-9a3650c7-6210-4993-b17f-94a342e0f9a0.png">

- `intern help` - This returns a clarification on how to interact with the bot's intern module

## Networking Module
- `network add_me` - Adds you to a private networking channel. Random users will be paired up with some generated prompts on a biweekly basis!
- `network help` - Returns clarification on how to interact with the bot's network module
