# Commands

This text file gives a list of commands for the slackbot

# Admin Commands

# Non-Admin Commands

## Library Functionality

1. `library list_books`

The `list_books` commands returns a list of books currently available in the library including who currently owns them.

**EXAMPLE**

Salomon: list_books

SlackBot:
| Book Name          | ID  | Owners |
|--------------------------------------|-----|-------------------------------|
| Dynamic Programming: Made easy       | ABC | Berke Lunstad, Salomon Dushimirimana         |
| How is Berke so Cool                 | DAW | Adam Hollander                |
| Whatever Happened to Easy Interviews | BKL | Izzy Hood                     |

2. `library borrow_book BOOK_ID (USER_EMAIL)`

The `borrow_book` command is passed a `BOOK_ID` and (optional) `USER_EMAIL`. The slackbot then sets up a conversation between person and owner of book with ID of transaction. Owner of book confirms transaction via `library confirm TRANSACTION_ID`

**EXAMPLE**

Salomon: library borrow_book ABC




3. `library donate_book ISBN`

Adds specified book to library. 

## Internship Functionality

Get companies at which Changepp members have worked! ~NETWORKING~

1. `internship list_companies`

**EXAMPLE**

Salomon: `internship list_companies`

SlackBot:
| Company Name          | ID  | workers |
|--------------------------------------|-----|-------------------------------|
| Microsoft       | ABC | Berke Lunstad, Salomon Dushimirimana         |
| Google                 | DAW | Adam Hollander                |
| Meta | BKL | Izzy Hood                     |

2. `internship network [COMPANY_ID] optional-[user_email]`

3. `internship list_resumes`

4. `internship add_resume`

5. `inernship add_company year`

## Resume Module

View resumes (list)

View resume (individual)

Upload resume

## Networking Module

**New Idea:** Referrals

You can join a networking channel and then once a week you are randomly paired with another member of the channel to discuss things. An initial chat is setup between you and that other member with three prompts of conversation topics (eg. mock interview, resume critique, coding shtuff) plus one other randomly selected one from a list. The channel can be left at any time, at which point you will stop being randomly paired.

1. `network`
