import click
import re
from datetime import datetime


# Define Regex Patterns
User = '(- (?P<username>[^:]*):)' # To get the user's name
Date = '(?P<date>(?P<month>[0-9]{1,2})[-|\/]{1}(?P<day>[0-9]{1,2})[-|\/]{1}(?P<year>[0-9]{2}))' # To get the date
Time = '(, (?P<time>[0-9]{2}:[0-9]{2}) )' # To get the time
DateTime = Date + Time # To get the date and time combined (Don't know why I added this, probably never gonna use it :w:P)
Msg = Date + Time + User + '(?P<message>.*)' # Finally to get the parsed message


# Find the number of messages
def find_msg_count(chatfile, start_date=None, end_date=None):
    file = open(chatfile, "r")
    count = 0
    for line in file:
        match = re.search(Msg, line)
        if match:
            matched_date = datetime.strptime(match.groupdict()['date'], '%m/%d/%y').date()
            # print(matched_user, matched_date)
            if not start_date or (start_date and start_date < matched_date < end_date):
                count += 1
    file.close()
    return count


# Find the frequecy at which a given users messages
def find_freq(username, chatfile, start_date=None, end_date=None):
    file = open(chatfile, 'r')
    count = 0
    for line in file:
        match = re.search(Msg, line)
        if match:
            matched_user = match.groupdict()['username']
            matched_date = datetime.strptime(match.groupdict()['date'], '%m/%d/%y').date()
            if username == matched_user and (not start_date or (start_date and start_date < matched_date < end_date)):
                count += 1
    file.close()
    return count


# Calc the metrics of how much the entered user has spoken in the chat within the given constraint(if provided)
def calc_percentage(username, path_to_chatfile, start_date=None, end_date=None):
    user_count = find_freq(username, path_to_chatfile, start_date, end_date)
    total_count = find_msg_count(path_to_chatfile, start_date, end_date)

    print('User Count: {}'.format(user_count))
    print('Total Count: {}'.format(total_count))
    print('Percentage: {}'.format(user_count/total_count*100))


# Find out who has started a conversations how many times
def find_conv_starters(chatfile):
    file = open(chatfile, 'r')
    total_diff = 0
    count = 1
    last_msg = None
    m = None
    while not m:
        m = re.match(Msg, file.readline())
    last_msg = datetime.strptime(m.groupdict()['date'] + ' ' + m.groupdict()['time'], '%m/%d/%y %H:%M')
    user_count = {}
    for line in file:
        m = re.match(Msg, line)
        if m:
            curr_msg = datetime.strptime(m.groupdict()['date'] + ' ' + m.groupdict()['time'], '%m/%d/%y %H:%M')
            difference = (curr_msg - last_msg).total_seconds()
            if difference != 0:
                total_diff += difference
                average = total_diff / count
                if difference > average:
                    user_count[m.groupdict()['username']] = user_count[m.groupdict()['username']] + 1 if m.groupdict()['username'] in user_count else 1
                    total_diff = 0
                    count = 0
                last_msg = curr_msg
                count += 1
    file.close()
    return user_count


# Add all the command line parameters
@click.command()
@click.argument('username')
@click.argument('path_to_chatfile')
@click.option('-p', '--percentage', is_flag=True, help='Show percentage contribution to the chat')
@click.option('-c', '--constraint', nargs=2, type=str, help='Add date Constraints (format - mm/dd/yy)')
@click.option('-cS', '--conv-starters', is_flag=True, help='Get the frequecy at which each person has started the conversation')
def controller(username, path_to_chatfile, percentage, constraint, conv_starters):
    if constraint:
        start_date = datetime.strptime(constraint[0], '%m/%d/%y').date()
        end_date = datetime.strptime(constraint[1], '%m/%d/%y').date()
    else:
        start_date = None
        end_date = None
    if conv_starters:
        print(find_conv_starters(path_to_chatfile))
    if percentage:
        calc_percentage(username, path_to_chatfile, start_date, end_date)


if __name__ == '__main__':
    controller()
