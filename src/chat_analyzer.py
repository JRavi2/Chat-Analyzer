import json
import re
from datetime import datetime
from json import JSONDecodeError
from time import time
from typing import Any, Dict, List

import click

import globals
from chat_functions import (
    calc_percentage, check_activity, find_conv_starters, interaction_curve_func
)

# Initialize the globals
globals.init()

"""
Define Regex Patterns
"""
# For Whatsapp chat exports
WUser = r'(- (?P<username>[^:]*):)'  # To get the user's name

# To get the date if it is in the format m/d/y(type1)
WDatetype1 = r'(?P<datetype1>(?P<monthtype1>[0-9]{1,2})[-\/]{1}(?P<daytype1>[0-9]{1,2})[-\/]{1}(?P<yeartype1>[0-9]{2,4}))'
# To get the date if it is in the format d/m/y(type2)
WDatetype2 = r'(?P<datetype2>(?P<daytype2>[0-9]{1,2})[-\/]{1}(?P<monthtype2>[0-9]{1,2})[-\/]{1}(?P<yeartype2>[0-9]{2,4}))'
# To get the date if it is in the format y/m/d(type3)
WDatetype3 = r'(?P<datetype3>(?P<yeartype3>[0-9]{2,4})[-\/]{1}(?P<monthtype3>[0-9]{1,2})[-\/]{1}(?P<daytype3>[0-9]{1,2}))'

# To get the time in 12hr clock
WTimeHour12 = r'(, (?P<time>(?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{2}) (?P<ampm>[AP]M)) )'
# To get the time in 24hr clock
WTimeHour24 = r'(, (?P<time>(?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{2})) )'

# Finally to get the parsed message
WMsgtype1Hour12 = WDatetype1 + WTimeHour12 + WUser + r'(?P<message>.*)'
WMsgtype1Hour24 = WDatetype1 + WTimeHour24 + WUser + r'(?P<message>.*)'

WMsgtype2Hour12 = WDatetype2 + WTimeHour12 + WUser + r'(?P<message>.*)'
WMsgtype2Hour24 = WDatetype2 + WTimeHour24 + WUser + r'(?P<message>.*)'

WMsgtype3Hour12 = WDatetype3 + WTimeHour12 + WUser + r'(?P<message>.*)'
WMsgtype3Hour24 = WDatetype3 + WTimeHour24 + WUser + r'(?P<message>.*)'

# For Signal chat exports
SDate = r'(?P<date>(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2}))'
STime = r'(?P<time>(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}))'
SDateTime = r'\[' + SDate + r' ' + STime + r'\]'
SUser = r'(?P<username>[^:]*):'
SMsg = SDateTime + r' ' + SUser + r'(?P<message>.*)'

# For Telegram chat exports
TDate = r'(?P<date>(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2}))'
TTime = r'(?P<time>(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<seconds>[0-9]{2}))'
TDateTime = TDate + r'T' + TTime


def import_data(path_to_chatfile: str) -> List[Dict[str, Any]]:
    """
    Recognize, parse data from a chat export and return in a standard format.

    Return prototype:
    msgs = [
        {
            'username': <string>,
            'date': <datetime.date object>
            'month': <string>
            'day': <string>
            'year': <string>
            'time': <datetime.time object>
            'hour': <string>
            'minute': <string>
        }
    ]
    """
    try:
        f = open(path_to_chatfile, 'r')
    except FileNotFoundError:
        print('File not found!!')
        exit()

    msgs = []

    # Telegram export
    try:
        data = json.load(f)['chats']['list']
        print('Telegram chat recognized')
        chat_name = input('Enter the chat name: ')

        for chat in data:
            if chat['name'] == chat_name:
                chat_data = chat['messages']
                break
        else:
            print('Chat data not found!')
            exit()

        for msg in chat_data:
            date_match = re.search(TDateTime, msg['date'])
            if date_match and 'from' in msg:
                msgs.append({
                    'username': msg['from'],
                    'date': datetime.strptime(date_match.groupdict()['date'], '%Y-%M-%d').date(),
                    'month': date_match.groupdict()['month'],
                    'day': date_match.groupdict()['day'],
                    'year': date_match.groupdict()['year'],
                    'time': datetime.strptime(date_match.groupdict()['time'], '%H:%M:%S').time(),
                    'hour': date_match.groupdict()['hour'],
                    'minute': date_match.groupdict()['minute'],
                })
        f.close()
        return msgs

    except KeyError:
        # Check for self-exported file
        try:
            f.seek(0)
            msgs = json.load(f)['messages']
            print('Self-exported file recognized')
            f.close()
            return msgs

        # Not a Telegram or self exported file but a JSON, so can't be of any other origin
        except KeyError:
            print('Invalid file!')
            exit()

    # Not a JSON file, so can't be a Telegram or self exported file, check for other types
    except JSONDecodeError:
        pass

    # Signal Export
    f.seek(0)
    isSignal = False
    for line_num, line in enumerate(f):
        if line_num > globals.SIGNAL_MEMBER_LIMIT:
            break
        match = re.search(SMsg, line)
        if match:
            isSignal = True
            break

    if isSignal:
        print('Signal chat recognized')
        f.seek(0)
        for line in f:
            match = re.search(SMsg, line)
            if match:
                msgs.append({
                    'username': match.groupdict()['username'],
                    'date': datetime.strptime(match.groupdict()['date'], '%Y-%M-%d').date(),
                    'month': match.groupdict()['month'],
                    'day': match.groupdict()['day'],
                    'year': match.groupdict()['year'],
                    'time': datetime.strptime(match.groupdict()['time'], '%H:%M').time(),
                    'hour': match.groupdict()['hour'],
                    'minute': match.groupdict()['minute'],
                })
        f.close()
        return msgs

    # Whatsapp Export
    f.seek(0)
    isWa = False
    for line_num, line in enumerate(f):
        if line_num > globals.WHATSAPP_MEMBER_LIMIT:
            break
        match1Hour12 = re.search(WMsgtype1Hour12, line)
        match1Hour24 = re.search(WMsgtype1Hour24, line)
        match2Hour12 = re.search(WMsgtype2Hour12, line)
        match2Hour24 = re.search(WMsgtype2Hour24, line)
        match3Hour12 = re.search(WMsgtype3Hour12, line)
        match3Hour24 = re.search(WMsgtype3Hour24, line)
        if match1Hour12 or match1Hour24 or match2Hour12 or match2Hour24 or match3Hour12 or match3Hour24 :
            isWa = True
            break

    if isWa:
        print('Whatsapp chat recognized')
        f.seek(0)
        for line in f:
            match1Hour12 = re.search(WMsgtype1Hour12, line)
            match1Hour24 = re.search(WMsgtype1Hour24, line)
            match2Hour12 = re.search(WMsgtype2Hour12, line)
            match2Hour24 = re.search(WMsgtype2Hour24, line)
            match3Hour12 = re.search(WMsgtype3Hour12, line)
            match3Hour24 = re.search(WMsgtype3Hour24, line)
            if match1Hour12 and 1<=int(match1Hour12.groupdict()['daytype1'])<=31 and 1<=int(match1Hour12.groupdict()['monthtype1'])<=12 :
                msgs.append({
                    'username': match1Hour12.groupdict()['username'],
                    'date': datetime.strptime(match1Hour12.groupdict()['datetype1'], '%m/%d/%y').date(),
                    'month': match1Hour12.groupdict()['monthtype1'],
                    'day': match1Hour12.groupdict()['daytype1'],
                    'year': match1Hour12.groupdict()['yeartype1'],
                    'time': datetime.strptime(match1Hour12.groupdict()['time'], '%I:%M %p').time(),
                    'hour': match1Hour12.groupdict()['hour'],
                    'minute': match1Hour12.groupdict()['minute'],
                })
            elif match1Hour24 and 1<=int(match1Hour24.groupdict()['daytype1'])<=31 and 1<=int(match1Hour24.groupdict()['monthtype1'])<=12 :
                msgs.append({
                    'username': match1Hour24.groupdict()['username'],
                    'date': datetime.strptime(match1Hour24.groupdict()['datetype1'], '%m/%d/%y').date(),
                    'month': match1Hour24.groupdict()['monthtype1'],
                    'day': match1Hour24.groupdict()['daytype1'],
                    'year': match1Hour24.groupdict()['yeartype1'],
                    'time': datetime.strptime(match1Hour24.groupdict()['time'], '%H:%M').time(),
                    'hour': match1Hour24.groupdict()['hour'],
                    'minute': match1Hour24.groupdict()['minute'],
                })
            elif match2Hour12 and 1<=int(match2Hour12.groupdict()['daytype2'])<=31 and 1<=int(match2Hour12.groupdict()['monthtype2'])<=12 :
                msgs.append({
                    'username': match2Hour12.groupdict()['username'],
                    'date': datetime.strptime(match2Hour12.groupdict()['datetype2'], '%d/%m/%y').date(),
                    'month': match2Hour12.groupdict()['monthtype2'],
                    'day': match2Hour12.groupdict()['daytype2'],
                    'year': match2Hour12.groupdict()['yeartype2'],
                    'time': datetime.strptime(match2Hour12.groupdict()['time'], '%I:%M %p').time(),
                    'hour': match2Hour12.groupdict()['hour'],
                    'minute': match2Hour12.groupdict()['minute'],
                })
            elif match2Hour24 and 1<=int(match2Hour24.groupdict()['daytype2'])<=31 and 1<=int(match2Hour24.groupdict()['monthtype2'])<=12 :
                msgs.append({
                    'username': match2Hour24.groupdict()['username'],
                    'date': datetime.strptime(match2Hour24.groupdict()['datetype2'], '%d/%m/%y').date(),
                    'month': match2Hour24.groupdict()['monthtype2'],
                    'day': match2Hour24.groupdict()['daytype2'],
                    'year': match2Hour24.groupdict()['yeartype2'],
                    'time': datetime.strptime(match2Hour24.groupdict()['time'], '%H:%M').time(),
                    'hour': match2Hour24.groupdict()['hour'],
                    'minute': match2Hour24.groupdict()['minute'],
                })
            elif match3Hour12 and 1<=int(match3Hour12.groupdict()['daytype3'])<=31 and 1<=int(match3Hour12.groupdict()['monthtype3'])<=12 :
                msgs.append({
                    'username': match3Hour12.groupdict()['username'],
                    'date': datetime.strptime(match3Hour12.groupdict()['datetype3'], '%d/%m/%y').date(),
                    'month': match3Hour12.groupdict()['monthtype3'],
                    'day': match3Hour12.groupdict()['daytype3'],
                    'year': match3Hour12.groupdict()['yeartype3'],
                    'time': datetime.strptime(match3Hour12.groupdict()['time'], '%I:%M %p').time(),
                    'hour': match3Hour12.groupdict()['hour'],
                    'minute': match3Hour12.groupdict()['minute'],
                })
            elif match3Hour24 and 1<=int(match3Hour24.groupdict()['daytype3'])<=31 and 1<=int(match3Hour24.groupdict()['monthtype3'])<=12 :
                msgs.append({
                    'username': match3Hour24.groupdict()['username'],
                    'date': datetime.strptime(match3Hour24.groupdict()['datetype3'], '%y/%m/%d').date(),
                    'month': match3Hour24.groupdict()['monthtype3'],
                    'day': match3Hour24.groupdict()['daytype3'],
                    'year': match3Hour24.groupdict()['yeartype3'],
                    'time': datetime.strptime(match3Hour24.groupdict()['time'], '%H:%M').time(),
                    'hour': match3Hour24.groupdict()['hour'],
                    'minute': match3Hour24.groupdict()['minute'],
                })
        f.close()
        return msgs

    f.close()

    print('Invalid file!')
    exit()


def export_data(msgs: List[Dict[str, Any]], filename: str) -> None:
    """Export the imported data to a json file in a standard format."""
    if not filename:
        filename = 'export.json'

    json_msgs = {'messages': msgs}

    with open(filename, 'w') as outfile:
        json.dump(json_msgs, outfile, default=str, indent=2)

    print("Chat data exported to {}".format(filename))


"""
The command line options
"""


@click.command()
@click.argument('path_to_chatfile')
@click.option('-u', '--username', nargs=1, type=str,
              help='Show results for a particular User only (Provide the username)')
@click.option('-c', '--constraint', nargs=2, type=str, help='Add date Constraints (format - mm/dd/yy)')
@click.option('-sG', '--show-graph', is_flag=True, help='Show graph(s) for the selected options if available')
@click.option('-p', '--percentage', is_flag=True, help='Show percentage contribution to the chat')
@click.option('-cS', '--conv-starters', is_flag=True,
              help='Get the frequecy at which each person has started the conversation')
@click.option('-a', '--activity', is_flag=True, help='Show hourwise activity of users')
@click.option('-iC', '--interaction-curve', is_flag=True,
              help='Tell whether the interaction of the user has increased or decreased')
@click.option('-e', '--export', is_flag=True, help='Export the data into a standard json format')
@click.option('-eP', '--export-path', nargs=1, type=str, help='Add the export path')
def controller(
        path_to_chatfile: str, username: str, percentage: bool, constraint: List[str], conv_starters: bool,
        activity: bool, interaction_curve: bool, show_graph: bool, export: bool, export_path: str) -> None:
    """The main CLI controller"""
    # Import the data
    msgs = import_data(path_to_chatfile)
    start = time()

    # Set the date constraints (if present)
    if constraint:
        start_date = datetime.strptime(constraint[0], '%m/%d/%y').date()
        end_date = datetime.strptime(constraint[1], '%m/%d/%y').date()
    else:
        start_date = None
        end_date = None

    if conv_starters:
        find_conv_starters(msgs, username)

    if percentage:
        calc_percentage(msgs, username, start_date, end_date, show_graph)

    if activity:
        check_activity(msgs, username, start_date, end_date, show_graph)

    if interaction_curve:
        interaction_curve_func(
            msgs, username=username, start_date=start_date, end_date=end_date, show_graph=show_graph)

    if export:
        export_data(msgs, export_path)

    end = time()
    print('Program Finished')
    print('Total time taken: {} seconds'.format(end - start))


if __name__ == '__main__':
    controller()
