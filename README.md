# Chat Analyzer

## Description

This program analyzes the gives chat file for:
- How active a given user is in the chat
- Who has started a conversation in the chat how many times
- Has a user's (or the whole chat's) interaction increased in the given period (or the whole chat)

It also allows the user to add some date constraints and genrate graphs for some actions.

The program currently works for Telegram and Whatsapp chat exports

## How to Run

First install the required dependencies using the command:
`pip install -r requirements.txt`

Then you can run the program, by going to to 'src' directory and then running the following command:
`python chat_analyzer.py <options> <path_to_chatfile>`

To know about the options run the command:
`python chat_analyzer --help`

## Testing

To test changes, enter the 'tests' directory and run the following command:
`pytest tests.py`
