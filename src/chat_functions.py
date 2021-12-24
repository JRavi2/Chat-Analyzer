from datetime import datetime
from typing import Any, Dict, List, Tuple

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


def generate_graph_precentages(counts: List[Any]) -> Tuple[List[str], List[float]]:
    """Generate the percentage data from counts"""
    users = []
    percs = []
    minor_perc = 0
    minor_users = ''
    for user_count in counts:
        perc = user_count[2]
        if perc > 1.0:
            users.append(user_count[0])
            percs.append(perc)
        else:
            minor_perc += perc
            minor_users += user_count[0] if minor_users == '' else ', ' + user_count[0]

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
    res = [['Username', 'Message Count', 'Percentage']]

    # Return the results in a tabulate friendly format
    if username:
        res.append([username, user_count, user_count/total_count*100])
    else:
        for user, count in user_count.items():
            res.append([user, count, count/total_count*100])

    return (res, total_count)


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

    # Convert the counts to a tabulate friendly format
    res = [['User', 'Count']]

    if not username:
        for user, count in user_count.items():
            res.append([user, count])
    else:
        res.append([username, user_count[username]])

    return res


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
        res = [username, user_count[username]['max']]
        list1 = []
        if show_graph and globals.CAN_SHOW_GRAPH:
            hours = np.arange(24)
            counts = [0]*24
            for hour, count in user_count[username].items():
                if hour != 'max':
                    counts[int(hour)] = count
            list1 = [hours, counts]
        return res, list1
    else:
        return user_count


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
    return slope_sign_pred, str_dates, x, y, y_pred, dates
