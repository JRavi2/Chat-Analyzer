import re
from datetime import datetime
import sys

#-----------------------
n = len(sys.argv)
print("Total arguments passed:", n)
 
input_file_name = sys.argv[1]
output_file_name = sys.argv[2]
input_date_format = sys.argv[3]

# Function to convert the date format
def convert24(str1):

    '''
    This function takes time in am/pm as input and returns the 24 hr format 

    '''
      
    # Checking if last two elements of time
    # is AM and first two elements are 12
    if str1[-2:] == "am" and str1[:2] == "12":
        return "00" + str1[2:-2]
          
    # remove the AM    
    elif str1[-2:] == "am":
        return str1[:-2]
      
    # Checking if last two elements of time
    # is PM and first two elements are 12   
    elif str1[-2:] == "pm" and str1[:2] == "12":
        return str1[:-2]
          
    else:
          
        # add 12 to hours and remove PM
        return str(int(str1[:2]) + 12) + str1[2:5]

#---------------------------------------------------

def format_input_file(input_file_name):

    '''
    This needs more work.
    This function cleans the exported chat to remove lines which 
    do not conform to the acceptable format. For eg. Chats which 
    are of multiple lines and with spaces within.
    
    '''

    WUser = r'(- (?P<username>[^:]*):)'  # To get the user's name
    WDate = r'(?P<date>(?P<month>[0-9]{1,2})[-\/]{1}(?P<day>[0-9]{1,2})[-\/]{1}(?P<year>[0-9]{2}))'
    WTime = r'(, (?P<time>(?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{2}) (?P<ampm>AM|PM|am|pm)) )'
# to get the parsed message
    WMsg = WDate + WTime + WUser + r'(?P<message>.*)'
    formatted_input_list = []
    
    with open(input_file_name, "r") as file_input:
        for line in file_input:
            match = re.search(WMsg, line)
            if match:
                formatted_input_list.append(line)
    return formatted_input_list

#-----------------------------------------------

def format_date(formatted_input_list,input_date_format): #ddmmyy

    '''
    This function formats the date in exported chat into acceptable format

    '''

    dict_date = {"ddmmyy": "%d/%m/%y","mmddyy": "%m/%d/%y"}
    WDate = r'(?P<date>(?P<day>[0-9]{1,2})[-\/]{1}(?P<month>[0-9]{1,2})[-\/]{1}(?P<year>[0-9]{2}))'
    new_full_string = []
    for line in range(len(formatted_input_list) -1):
            match = re.search(WDate,formatted_input_list[line])
            old_format = match.group()
            datetimeobject = datetime.strptime(old_format,dict_date[input_date_format])
            new_format = datetimeobject.strftime("%m/%d/%y")
            full_string = formatted_input_list[line]
            new_full_string.append(full_string.replace(old_format,new_format))
    return new_full_string


def format_time_string(string):

    '''
    This function formats the time from 12hr format to 24hr format
    '''



    if string[0] > '1': 
        return string[:0] + "0" + string[0:]
    elif string[0] == '1' and string[1] != '1' and string[1] != ':' :
        return string
    elif string[0] == '1' and string[1] == '1' :
        return string
    elif string[0] == '1' and string[1] == ':' :
        return string[:0] + "0" + string[0:]

#-----------------------------------------------------

def format_time(new_full_string):
    '''
    This function formats the string to have 24hr format time
    '''




    new_full_string_time = []
    for line in range(len(new_full_string)):
        time_string = new_full_string[line][10:18].strip()
        formatted_time_string = format_time_string(time_string)
        new_time_string = convert24(formatted_time_string).strip()
        full_string = new_full_string[line]
        new_full_string_time.append(full_string.replace(time_string,new_time_string))
    return new_full_string_time

#-------------------------------------------------------





def save_file(output_file_name):
    '''
    This saves the formatted file. 
    
    '''

    with open(output_file_name, "w") as output:
        for line in new_full_string:
            output.write(line)


def save_file_original():
    '''
    This saves the formatted file with everything as the original code
    
    '''

    with open('formatted_time.txt', "w") as output:
        for line in new_full_string_time:
            output.write(line)
        

formatted_input_list = format_input_file(input_file_name)
new_full_string = format_date(formatted_input_list, input_date_format)
new_full_string_time = format_time(new_full_string)
save_file(output_file_name)
save_file_original()