import click
import re
import json
from datetime import datetime
from time import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

try:
    matplotlib.use('TkAgg')
    CAN_SHOW_GRAPH = True
except:
    print("Warning: Tkinter is not installed, graphs will not be shown")
    CAN_SHOW_GRAPH = False


'''
Define Regex Patterns
'''
# For Telegram chat exports
TDate = '(?P<date>(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2}))'
TTime = '(?P<time>(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<seconds>[0-9]{2}))'
TDateTime = TDate + 'T' + TTime

# For Whatsapp chat exports
WUser = '(- (?P<username>[^:]*):)' # To get the user's name
WDate = '(?P<date>(?P<month>[0-9]{1,2})[-|\/]{1}(?P<day>[0-9]{1,2})[-|\/]{1}(?P<year>[0-9]{2}))' # To get the date
WTime = '(, (?P<time>(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2})) )' # To get the time
WMsg = WDate + WTime + WUser + '(?P<message>.*)' # Finally to get the parsed message


def import_data(path_to_chatfile):
    f = open(path_to_chatfile, "r")
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
    return msgs


def find_msg_count(msgs, start_date=None, end_date=None):
    '''
    Find the number of messages
    '''
    count = 0
    for msg in msgs:
        date = msg['date']
        if not start_date or (start_date and start_date < date < end_date):
            count += 1
    return count


def find_freq(msgs, username=None, start_date=None, end_date=None):
    '''
    Find the frequecy at which a given users messages
    '''
    user_count = {}
    for msg in msgs:
        user = msg['username']
        date = msg['date']
        if not start_date or (start_date and start_date < date < end_date):
            user_count[user] = user_count[user] + 1 if user in user_count else 1
    if username:
        return user_count[username] if username in user_count else 0
    else:
        return user_count


def calc_percentage(msgs, username=None, start_date=None, end_date=None):
    '''
    Calc the metrics of how much the entered user has spoken in the chat within the given constraint(if provided)
    '''
    user_count = find_freq(msgs, username, start_date, end_date)
    total_count = find_msg_count(msgs, start_date, end_date)

    print('Total Count: {}\n'.format(total_count))

    if username:
        print('Message Count: {}'.format(user_count))
        print('Percentage: {}'.format(user_count/total_count*100))
    else:
        for user, count in user_count.items():
            print("For the user {}".format(user))
            print("Message Count: {}".format(count))
            print("Percentage: {}\n".format(count/total_count*100))


def find_conv_starters(msgs, username=None):
    '''
    Find out who has started a conversations how many times
    '''
    total_diff = 0
    count = 1
    last_msg = None

    # Get the first message that was sent in the chat
    last_msg = datetime.combine(msgs[0]['date'], msgs[0]['time'])
    user_count = {}
    for msg in msgs:
        curr_msg = datetime.combine(msg['date'], msg['time'])
        difference = (curr_msg - last_msg).total_seconds()
        if difference != 0:
            total_diff += difference
            average = total_diff / count
            '''
            If the difference in time between current message and the last message is more than the average difference
            then that would mean that the current message is a conversation starter
            '''
            if difference > average:
                user_count[msg['username']] = user_count[msg['username']] + 1 if msg['username'] in user_count else 1
                total_diff = 0
                count = 0
            last_msg = curr_msg
            count += 1

    if username:
        print("The user {} started consversation {} time(s)".format(username, user_count[username]))
    else:
        for user, count in user_count.items():
            print("The user {} started consversation {} time(s)".format(user, count))


def check_activity(msgs, username=None, start_date=None, end_date=None):
    '''
    Get the time of the day when each user(or a particular user) is most active
    '''
    '''
    Prototype for the user_count variable
    user_count = {
        <username> : {
            <hour> : <frequency>
        }
    }
    '''
    user_count = {}
    for msg in msgs:
        user = msg['username']
        hour = msg['hour']
        date = msg['date']
        if not start_date or (start_date and start_date < date < end_date):
            if user not in user_count:
                user_count[user] = {}
            user_count[user][hour] = user_count[user][hour] + 1 if hour in user_count[user] else 1

    for user in user_count:
        max_freq = 0
        max_freq_hour = '00'
        for hour in user_count[user]:
            if user_count[user][hour] > max_freq:
                max_freq = user_count[user][hour]
                max_freq_hour = hour
        user_count[user]['max'] = max_freq_hour


    if username:
        print("The user {} mostly stays active around {} Hours".format(username, user_count[username]['max']))
    else:
        for user in user_count:
            print("The user {} mostly stays active around {} Hours".format(user, user_count[user]['max']))


def interaction_curve_func(msgs, username=None, start_date=None, end_date=None, show_graph=False):
    '''
    Make a linear regression model to predict whether there has been
    an increase or decrease in the number of messages
    '''
    cur_date = ""
    cur_freq = 0
    dates = []
    str_dates = []
    freqs = []

    for msg in msgs:
        date = msg['date']
        user = msg['username']

        if (not username or user == username) and (not start_date or (date >= start_date and date <= end_date)):
            if cur_date == "":
                cur_date = date
            elif date != cur_date:
                dates.append(datetime.toordinal(cur_date))
                str_dates.append(str(cur_date))
                freqs.append(cur_freq)
                cur_date = date
                cur_freq = 0
            cur_freq += 1

    dates.append(datetime.toordinal(cur_date))
    str_dates.append(str(cur_date))
    freqs.append(cur_freq)

    # Reshaping to get a (n X 1)D array
    x = np.array(dates).reshape(-1, 1)
    y = np.array(freqs).reshape(-1, 1)
    linear_regressor = LinearRegression()
    linear_regressor.fit(x, y)
    y_pred = linear_regressor.predict(x)
    slope_sign_pred = (y_pred[1][0] - y_pred[0][0]) / abs(y_pred[1][0] - y_pred[0][0])

    if slope_sign_pred < 0:
        print("Your interactions in this chat has decreased!")
    else:
        print("Your interactions in this chat has increased!")

    # For Graph
    if show_graph and CAN_SHOW_GRAPH:
        print("Showing graph....")
        plt.plot(x, y, 'o', color='black') # The point plot
        plt.plot(x, y_pred, color='red') # The line plot
        plt.xticks(dates, str_dates)
        plt.locator_params(axis='x', nbins=4)
        plt.show()


'''
The command line options
'''
@click.command()
@click.argument('path_to_chatfile')
@click.option('-p', '--percentage', is_flag=True, help='Show percentage contribution to the chat')
@click.option('-cS', '--conv-starters', is_flag=True, help='Get the frequecy at which each person has started the conversation')
@click.option('-u', '--username', nargs=1, type=str, help='Show results for a particular User only (Provide the username)')
@click.option('-c', '--constraint', nargs=2, type=str, help='Add date Constraints (format - mm/dd/yy)')
@click.option('-a', '--activity', is_flag=True, help='Show hourwise activity of users')
@click.option('-iC', '--interaction-curve', is_flag=True, help='Tell whether the interaction of the user has increased or decreased')
@click.option('-sG', '--show-graph', is_flag=True, help='Show graph(s) for the selected options if available')
def controller(path_to_chatfile, username, percentage, constraint, conv_starters, activity, interaction_curve, show_graph):
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
        calc_percentage(msgs, username, start_date, end_date)
    if activity:
        check_activity(msgs, username, start_date, end_date)
    if interaction_curve:
        interaction_curve_func(msgs, username=username, start_date=start_date, end_date=end_date, show_graph=show_graph)
    end = time()
    print("Program Finished")
    print("Total time taken: {} seconds".format(end - start))


if __name__ == '__main__':
    controller()
