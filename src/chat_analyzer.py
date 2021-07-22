import click
import json
import re

from time import time
from chat_functions import *

try:
    matplotlib.use('TkAgg')
    CAN_SHOW_GRAPH = True
except:
    print('Warning: Tkinter is not installed, graphs will not be shown')
    CAN_SHOW_GRAPH = False


'''
Define Regex Patterns
'''
# For Signal chat exports
SDate = '(?P<date>(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2}))'
STime = '(?P<time>(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}))'
SDateTime = '\[' + SDate + ' ' + STime + '\]'
SUser = '(?P<username>[^:]*):'
SMsg = SDateTime + ' ' + SUser + '(?P<message>.*)'

# For Telegram chat exports
TDate = '(?P<date>(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2}))'
TTime = '(?P<time>(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<seconds>[0-9]{2}))'
TDateTime = TDate + 'T' + TTime

# For Whatsapp chat exports
WUser = '(- (?P<username>[^:]*):)' # To get the user's name
WDate = '(?P<date>(?P<month>[0-9]{1,2})[-\/]{1}(?P<day>[0-9]{1,2})[-\/]{1}(?P<year>[0-9]{2}))' # To get the date
WTime = '(, (?P<time>(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2})) )' # To get the time
WMsg = WDate + WTime + WUser + '(?P<message>.*)' # Finally to get the parsed message


def import_data(path_to_chatfile):
    '''
    Recognise and parse data from a chat export and return in a standardised format
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
    '''
    try:
        f = open(path_to_chatfile, 'r')
    except:
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

        return msgs
    except Exception as e:
        pass

    # Signal Export
    f.seek(0)
    isSignal = False
    for line in f:
        match = re.search(SMsg, line)
        if match:
            isSignal = True
            break

    if isSignal:
        f.seek(0)
        print('Signal chat recognized')
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
        return msgs

    # Whatsapp Export
    f.seek(0)
    for line in f:
        match = re.search(WMsg, line)
        if match:
            msgs.append({
                            'username': match.groupdict()['username'],
                            'date': datetime.strptime(match.groupdict()['date'], '%m/%d/%y').date(),
                            'month': match.groupdict()['month'],
                            'day': match.groupdict()['day'],
                            'year': match.groupdict()['year'],
                            'time': datetime.strptime(match.groupdict()['time'], '%H:%M').time(),
                            'hour': match.groupdict()['hour'],
                            'minute': match.groupdict()['minute'],
                        })
    f.close()

    if len(msgs) == 0:
        print('Invalid file!')
        exit()

    return msgs


def export_data(msgs, filename):
    '''
    Export the imported data to a json file in a standar format
    '''
    if not filename:
        filename = 'export.json'

    json_msgs = {'messages' : msgs}

    with open(filename, 'w') as outfile:
        json.dump(json_msgs, outfile, default=str)


'''
The command line options
'''
@click.command()
@click.argument('path_to_chatfile')
@click.option('-u', '--username', nargs=1, type=str, help='Show results for a particular User only (Provide the username)')
@click.option('-c', '--constraint', nargs=2, type=str, help='Add date Constraints (format - mm/dd/yy)')
@click.option('-sG', '--show-graph', is_flag=True, help='Show graph(s) for the selected options if available')
@click.option('-p', '--percentage', is_flag=True, help='Show percentage contribution to the chat')
@click.option('-cS', '--conv-starters', is_flag=True, help='Get the frequecy at which each person has started the conversation')
@click.option('-a', '--activity', is_flag=True, help='Show hourwise activity of users')
@click.option('-iC', '--interaction-curve', is_flag=True, help='Tell whether the interaction of the user has increased or decreased')
@click.option('-e', '--export', is_flag=True, help='Export the data into a standard json format')
@click.option('-eP', '--export-path', nargs=1, type=str, help='Add the export path')
def controller(path_to_chatfile, username, percentage, constraint, conv_starters, activity, interaction_curve, show_graph, export, export_path):
    msgs = import_data(path_to_chatfile)
    start = time()
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
        interaction_curve_func(msgs, username=username, start_date=start_date, end_date=end_date, show_graph=show_graph)
    if export:
        export_data(msgs, export_path)
    end = time()
    print('Program Finished')
    print('Total time taken: {} seconds'.format(end - start))


if __name__ == '__main__':
    controller()
