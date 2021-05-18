# Chat Analyzer

## Description

This program analyzes the gives chat file for:
- What is the percentage contribution (in terms of number of messages) of a user in the chat
- How active a given user is in the chat
- Who has started a conversation in the chat how many times
- Has a user's (or the whole chat's) interaction increased in the given period (or the whole chat)

It also allows the user to add some date constraints and genrate graphs for some actions.

If you want to run your own analysis, the program can also export the chat data after converting it into a standard format.

The program currently works for Signal, Telegram and Whatsapp chat exports

## How to Run

First install the required dependencies using the command:

    pip install -r requirements.txt

Then you can run the program, by going to to `src` directory and then running the following command:

    python chat_analyzer.py <options> <path_to_chatfile>

To know about the options run the command:

    python chat_analyzer --help

## Testing

To test changes, enter the `tests` directory and run the following command:

    pytest tests.py
