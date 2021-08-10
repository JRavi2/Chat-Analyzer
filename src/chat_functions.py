from datetime import datetime
from typing import Any, Dict, List, Tuple

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
        if start_date and start_date < date < end_date:
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


def generate_graph_precentages(counts: Dict[str, int], total_count: int) -> Tuple[List[str], List[float]]:
    """Generate the percentage data from counts"""
    users = []
    percs = []
    minor_perc = 0
    minor_users = ''
    for user, count in counts.items():
        perc = count/total_count * 100
        if perc > 1.0:
            users.append(user)
            percs.append(perc)
        else:
            minor_perc += perc
            minor_users += user if minor_users == '' else ', ' + user

    if minor_users != "":
        users.append(minor_users)
        percs.append(minor_perc)

    return (users, percs)


def calc_percentage(msgs: List[Dict[str, Any]],
                    username: datetime = None, start_date: datetime = None, end_date: datetime = None,
                    show_graph: datetime = False) -> None:
    """Calculate the percentage contirbution of each user (or a given user)"""
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
            users, percs = generate_graph_precentages(user_count, total_count)
            plt.pie(x=percs, autopct='%1.1f%%', shadow=True, startangle=90)
            plt.axis('equal')
            plt.legend(users)
            plt.tight_layout()
            plt.title('Percentage contribution of each user in the chat')
            plt.show()


def find_conv_starters(msgs: List[Dict[str, Any]], username: str = None) -> None:
    """Find out how many times each user (or a given user) has started a conversation"""
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
        print('The user {} started conversation {} time(s)'.format(username, user_count[username]))
    else:
        for user, count in user_count.items():
            print('The user {} started conversation {} time(s)'.format(user, count))


def check_activity(
        msgs: List[Dict[str, Any]], username: str = None,
        start_date: datetime = None, end_date: datetime = None, show_graph: bool = False) -> None:
    """
    Get the time of the day when each user (or a given user) is most active

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
            hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
                     '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
            plt.xticks(ticks=np.arange(24), labels=globals.HOURS_LIST)
            plt.tight_layout()
            plt.xlabel('Time of day (in Hours)')
            plt.ylabel('Message Count')
            plt.title('Activity of each user')
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
            plt.xticks(ticks=np.arange(24), labels=globals.HOURS_LIST)
            plt.tight_layout()
            plt.legend()
            plt.xlabel('Time of day (in Hours)')
            plt.ylabel('Message Count')
            plt.title('Activity of each user')
            plt.show()


def interaction_curve_func(
        msgs: List[Dict[str, Any]], username: str = None,
        start_date: datetime = None, end_date: datetime = None, show_graph: bool = False) -> None:
    """Use Linear Regression to figure out whether there has been an increase or decrease in the interactions"""
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
        plt.xticks(ticks=dates, labels=str_dates, rotation=45)
        plt.locator_params(axis='x', nbins=10)
        plt.tight_layout()
        plt.xlabel('Date')
        plt.ylabel('Message count')
        plt.title('Regression curve for interactions (no. of messages) in the chat')
        plt.show()
