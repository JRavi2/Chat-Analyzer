import click
import re
from datetime import datetime
from time import time
#  import matplotlib
#  import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
#  matplotlib.use('TkAgg')


'''
Define Regex Patterns
'''
User = '(- (?P<username>[^:]*):)' # To get the user's name
Date = '(?P<date>(?P<month>[0-9]{1,2})[-|\/]{1}(?P<day>[0-9]{1,2})[-|\/]{1}(?P<year>[0-9]{2}))' # To get the date
Time = '(, (?P<time>(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2})) )' # To get the time
DateTime = Date + Time # To get the date and time combined (Don't know why I added this, probably never gonna use it :P)

Msg = Date + Time + User + '(?P<message>.*)' # Finally to get the parsed message


def find_msg_count(chatfile, start_date=None, end_date=None):
    '''
    Find the number of messages
    '''
    file = open(chatfile, "r")
    count = 0
    for line in file:
        match = re.search(Msg, line)
        if match:
            matched_date = datetime.strptime(match.groupdict()['date'], '%m/%d/%y').date()
            if not start_date or (start_date and start_date < matched_date < end_date):
                count += 1
    file.close()
    return count


def find_freq(chatfile, username=None, start_date=None, end_date=None):
    '''
    Find the frequecy at which a given users messages
    '''
    file = open(chatfile, 'r')
    user_count = {}
    for line in file:
        match = re.search(Msg, line)
        if match:
            matched_user = match.groupdict()['username']
            matched_date = datetime.strptime(match.groupdict()['date'], '%m/%d/%y').date()
            if not start_date or (start_date and start_date < matched_date < end_date):
                user_count[match.groupdict()['username']] = user_count[match.groupdict()['username']] + 1 if match.groupdict()['username'] in user_count else 1
    file.close()
    if username:
        return user_count[username] if username in user_count else 0
    else:
        return user_count


def calc_percentage(path_to_chatfile, username=None, start_date=None, end_date=None):
    '''
    Calc the metrics of how much the entered user has spoken in the chat within the given constraint(if provided)
    '''
    user_count = find_freq(path_to_chatfile, username, start_date, end_date)
    total_count = find_msg_count(path_to_chatfile, start_date, end_date)

    print('Total Count: {}\n'.format(total_count))

    if username:
        print('User Count: {}'.format(user_count))
        print('Percentage: {}'.format(user_count/total_count*100))
    else:
        for user, count in user_count.items():
            print("For the user {}".format(user))
            print("User Count: {}".format(count))
            print("Percentage: {}\n".format(count/total_count*100))


def find_conv_starters(path_to_chatfile, username=None):
    '''
    Find out who has started a conversations how many times
    '''
    file = open(path_to_chatfile, 'r')
    total_diff = 0
    count = 1
    last_msg = None

    # Get the first message that was sent in the chat
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
                '''
                If the difference in time between current message and the last message is more than the average difference
                then that would mean that the current message is a conversation starter
                '''
                if difference > average:
                    user_count[m.groupdict()['username']] = user_count[m.groupdict()['username']] + 1 if m.groupdict()['username'] in user_count else 1
                    total_diff = 0
                    count = 0
                last_msg = curr_msg
                count += 1
    file.close()

    if username:
        print("The user {} started consversation {} time(s)".format(username, user_count[username]))
    else:
        for user, count in user_count.items():
            print("The user {} started consversation {} time(s)".format(user, count))


def check_activity(path_to_chatfile, username=None, start_date=None, end_date=None):
    '''
    Get the time of the day when each user(or a particular user) is most active
    '''
    file = open(path_to_chatfile, 'r')
    '''
    Prototype for the user_count variable
    user_count = {
        <username> : {
            <hour> : <frequency>
        }
    }
    '''
    user_count = {}
    for line in file:
        match = re.search(Msg, line)
        if match:
            matched_user = match.groupdict()['username']
            matched_hour = match.groupdict()['hour']
            matched_date = datetime.strptime(match.groupdict()['date'], '%m/%d/%y').date()
            if not start_date or (start_date and start_date < matched_date < end_date):
                if matched_user not in user_count:
                    user_count[matched_user] = {}
                user_count[matched_user][matched_hour] = user_count[matched_user][matched_hour] + 1 if matched_hour in user_count[matched_user] else 1

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
    file.close()


def interaction_curve_func(chatfile, username=None, start_date=None, end_date=None):
    '''
    Make a linear regression model to predict whether there has been
    an increase or decrease in the number of messages
    '''
    file = open(chatfile, "r")
    cur_date = ""
    cur_freq = 0
    dates = []
    str_dates = []
    freqs = []

    for line in file:
        match = re.search(Msg, line)
        if match:
            matched_date = datetime.strptime(match.groupdict()['date'], '%m/%d/%y').date()
            matched_user = match.groupdict()['username']

            if (not username or matched_user == username) and (not start_date or (matched_date >= start_date and matched_date <= end_date)):
                if cur_date == "":
                    cur_date = matched_date
                elif matched_date != cur_date:
                    dates.append(datetime.toordinal(cur_date))
                    str_dates.append(str(cur_date))
                    freqs.append(cur_freq)
                    cur_date = matched_date
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
    print("Showing graph....")

    # Graph for future
    #  plt.plot(x, y, 'o', color='black') # The point plot
    #  plt.plot(x, y_pred, color='red') # The line plot
    #  plt.xticks(dates, str_dates)
    #  plt.locator_params(axis='x', nbins=4)
    #  plt.show()
    file.close()


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
def controller(path_to_chatfile, username, percentage, constraint, conv_starters, activity, interaction_curve):
    start = time()
    if constraint:
        start_date = datetime.strptime(constraint[0], '%m/%d/%y').date()
        end_date = datetime.strptime(constraint[1], '%m/%d/%y').date()
    else:
        start_date = None
        end_date = None
    if interaction_curve:
        interaction_curve_func(path_to_chatfile, username=username, start_date=start_date, end_date=end_date)
    if conv_starters:
        find_conv_starters(path_to_chatfile, username)
    if percentage:
        calc_percentage(path_to_chatfile, username, start_date, end_date)
    if activity:
        check_activity(path_to_chatfile, username, start_date, end_date)
    end = time()
    print("Program Finished")
    print("Total time taken: {} seconds".format(end - start))


if __name__ == '__main__':
    controller()
