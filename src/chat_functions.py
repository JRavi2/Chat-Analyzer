from datetime import datetime
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

import globals


def find_msg_count(msgs: List[Dict[str, Any]], start_date: datetime = None, end_date: datetime = None) -> int:
    """Find the number of messages"""
    count = 0

    if not start_date:
        return len(msgs)

    for msg in msgs:
        date = msg['date']
        if not start_date or (start_date and start_date < date < end_date):
            count += 1
    return count


def find_freq(msgs: List[Dict[str, Any]],
              username: str = None, start_date: datetime = None, end_date: datetime = None) -> Dict[str, int]:
    """Find the frequecy at which a given users messages"""
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


def calc_percentage(msgs: List[Dict[str, Any]],
                    username: datetime = None, start_date: datetime = None, end_date: datetime = None,
                    show_graph: datetime = False) -> None:
    """Calc the metrics of how much the entered user has spoken in the chat within the given constraint(if provided)"""
    user_count = find_freq(msgs, username, start_date, end_date)
    total_count = find_msg_count(msgs, start_date, end_date)

    print('Total Count: {}\n'.format(total_count))

    if username:
        print('Message Count: {}'.format(user_count))
        print('Percentage: {}'.format(user_count/total_count*100))
    else:
        for user, count in user_count.items():
            print('For the user {}'.format(user))
            print('Message Count: {}'.format(count))
            print('Percentage: {}\n'.format(count/total_count*100))

        # For Graph
        if show_graph and globals.CAN_SHOW_GRAPH:
            print('\nShowing graph....')
            users = list(user_count.keys())
            counts = list(user_count.values())
            x = np.arange(len(users))
            #  width = 0.35
            plt.bar(x, counts, tick_label=users)
            plt.xticks(rotation=60)
            plt.tight_layout()
            plt.show()


def find_conv_starters(msgs: List[Dict[str, Any]], username: str = None) -> None:
    """Find out who has started a conversations how many times"""
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
            """
            If the difference in time between current message and the last message is more than the average difference
            then that would mean that the current message is a conversation starter
            """
            if difference > average:
                user_count[msg['username']] = user_count[msg['username']] + 1 if msg['username'] in user_count else 1
                total_diff = 0
                count = 0
            last_msg = curr_msg
            count += 1

    if username:
        print('The user {} started consversation {} time(s)'.format(username, user_count[username]))
    else:
        for user, count in user_count.items():
            print('The user {} started consversation {} time(s)'.format(user, count))


def check_activity(
        msgs: List[Dict[str, Any]], username: str = None,
        start_date: datetime = None, end_date: datetime = None, show_graph: bool = False) -> None:
    """
    Get the time of the day when each user(or a particular user) is most active

    Prototype for the user_count variable
    user_count = {
        <username> : {
            <hour> : <frequency>
        }
    }
    """
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
        print('The user {} mostly stays active around {} Hours'.format(username, user_count[username]['max']))

        # For Graph
        if show_graph and globals.CAN_SHOW_GRAPH:
            print('\nShowing graph....')
            hours = np.arange(24)
            counts = [0]*24
            for hour, count in user_count[username].items():
                if hour != 'max':
                    counts[int(hour)] = count
            plt.plot(hours, counts)
            plt.xticks(rotation=60)
            plt.tight_layout()
            plt.show()
    else:
        for user in user_count:
            print('The user {} mostly stays active around {} Hours'.format(user, user_count[user]['max']))

        # For Graph
        if show_graph and globals.CAN_SHOW_GRAPH:
            print('\nShowing graph....')

            for user in user_count:
                hours = np.arange(24)
                counts = [0]*24
                for hour, count in user_count[user].items():
                    if hour != 'max':
                        counts[int(hour)] = count
                plt.plot(hours, counts, label=user)
            plt.xticks(rotation=60)
            plt.tight_layout()
            plt.legend()
            plt.show()


def interaction_curve_func(
        msgs: List[Dict[str, Any]], username: str = None,
        start_date: datetime = None, end_date: datetime = None, show_graph: bool = False) -> None:
    """Use Linear Regression to predict whether there has been an increase or decrease in the number of messages"""
    cur_date = ''
    cur_freq = 0
    dates = []
    str_dates = []
    freqs = []

    for msg in msgs:
        date = msg['date']
        user = msg['username']

        if (not username or user == username) and (not start_date or (date >= start_date and date <= end_date)):
            if cur_date == '':
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

    print('{} interactions in this chat have {}!'.format(
        'Your' if username else 'The',
        'decreased' if slope_sign_pred < 0 else 'increased'
    ))

    # For Graph
    if show_graph and globals.CAN_SHOW_GRAPH:
        print('Showing graph....')
        plt.plot(x, y, 'o', color='black')  # The point plot
        plt.plot(x, y_pred, color='red')  # The line plot
        plt.xticks(dates, str_dates)
        plt.locator_params(axis='x', nbins=4)
        plt.show()
