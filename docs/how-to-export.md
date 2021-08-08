# How to export chats

## Whatsapp

Follow the official docs [here](https://faq.whatsapp.com/android/chats/how-to-save-your-chat-history/?lang=en) or TLDR:

1. Open the chat to be exported
2. Tap `More Options` > `More` > `Export Chat`
3. Choose `Without Media`


## Telegram

You can find the official release blog for the chat export feature [here](https://telegram.org/blog/export-and-more).

TLDR, on the telegram desktop app:
1. Goto `Settings` > `Advanced` > `Export`
2. Uncheck `Account Information` and `Contacts List` (Both not required)
3. Under `Chat export settings` select the appropriate options according to your preference
4. Uncheck all options under `Media export settings` and `Other` (Not required)
5. Set the location, and select format as `Machine-readable JSON`

## Signal

Signal does not provide any "default" way to export chats to plain text. So you can use [this](https://github.com/carderne/signal-export) tool by [@carderne](https://github.com/carderne), and follow the steps given in it's README to export all the chats. You should have signal-desktop installed for the tool to work.

TLDR:
1. Clone the tool from the link given above.
2. Install the dependencies (namely, sqlcipher and openssl)
3. Go to the directory of the cloned repository
4. Run `./sigexport.py outputdir` to export the chats

**Note:** The Tool exports the chats in both HTML and Markdown. Make sure to use the Markdown files.