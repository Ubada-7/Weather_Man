import sys
from pathlib import Path
import calendar
import numpy as np
from colorama import Fore
def assign_location():
    user_input = input('''
                        Enter a L for Lahore 
                        Enter a M for Murree
                        Enter a D for Dubai : ''')
    FILE_ = ""
    if user_input == "L" or user_input == "l":
        FILE_= "lahore_weather"
    elif user_input == "D"or user_input == "d":
        FILE_ = "Dubai_weather"
    elif user_input == "M" or user_input == "m":
        FILE_ = "Murree_weather"
    else:
        print("Invalid path")
    return FILE_
def choi():
    user_i = input("Press 1 for highest, 2 for average, and 3 for Blue and Red: ")
    cho = ""
    if user_i == "1":
        cho = "-e"
    elif user_i == "2":
        cho = "-a"
    elif user_i == "3":
        cho = "-c"
    return cho
FILE_PATH = assign_location()
CHOICE = choi()  # Execute the function and store the return value in CHOICE variable
DATE = input("Enter the Year you want to know weather:")

def highest_temperature(file_data):
    '''It finds out the data for maximum,minimum and humid temperatures'''
    max_data = []
    min_data = []
    max_humid = []

    for data in file_data:
        if data[1] != "":
            max_data.append(int(data[1]))
            min_data.append(int(data[3]))
            max_humid.append(int(data[7]))
    max_temp = np.max(max_data)
    min_temp = np.min(min_data)
    max_humid = np.max(max_humid)
    for data in file_data:
        if data[1] != "" and int(data[1]) == max_temp:
            max_date = data[0]
        if data[3] != "" and int(data[3]) == min_temp:
            min_date = data[0]
        if data[3] != "" and int(data[7]) == max_humid:
            humid_date = data[0]
    return max_temp, max_date, min_temp, min_date, max_humid, humid_date

def average_temperature(lst):
    '''Returns data for the month average temperature'''
    max_average = []
    min_average = []
    humid_average = []

    for data in lst:
        if data[1] != "":
            max_average.append(int(data[1]))
            min_average.append(int(data[3]))
            humid_average.append(int(data[7]))
    max_temp_avg = int(np.sum(max_average)/len(max_average))
    min_temp_avg = int(np.sum(min_average)/len(min_average))
    max_humid_avg = int(np.sum(humid_average)/len(humid_average))
    return max_temp_avg, min_temp_avg, max_humid_avg

def max_min(file_data):
    '''Max-Min returns the data for displaying the chart by separating each day data'''
    max_daily = []
    min_daily = []
    date_daily = []
    for data in file_data:
        if data[1] != "":
            max_daily.append(int(data[1]))
            min_daily.append(int(data[3]))
            date_daily.append(data[0])
    return max_daily, min_daily, date_daily

def clean_data(files):
    '''Clean data function to exclude the raw data fromm file which is unnecessary'''
    local_list = []
    for file in files:
        data_file = open(file, 'r')
        data = data_file.read().splitlines()

        if "Max" in data[0]:
            data.pop(0)
        elif "Max" in data[1]:
            data.pop(0)
            data.pop(0)
        if "<!--" in data[-1]:
            data.pop()
        else:
            pass
        for element in data:
            local_list.append(element.split(','))
    return local_list

def main(choic):
    '''Main Function'''
    try:
        year = DATE
        if choic == "-e":
            file = Path(FILE_PATH).rglob('*{date}*.txt'.format(date=DATE))
            heighest_result = highest_temperature(clean_data(file))
            max_month = calendar.month_name[int(heighest_result[1].split('-')[1])]
            min_month = calendar.month_name[int(heighest_result[3].split('-')[1])]
            min_day = int(heighest_result[3].split('-')[2])
            humid_month = calendar.month_name[int(heighest_result[5].split('-')[1])]
            humid_day = int(heighest_result[5].split('-')[2])
            print("Highest: " + str(heighest_result[0])+"C on ", end="")
            print(str(max_month)+' '+str(int(heighest_result[1].split('-')[2])))
            print("Lowest:  " + str(heighest_result[2])+"C on "+str(min_month)+" "+str(min_day))
            print("Humid:   " + str(heighest_result[4])+"% on "+str(humid_month)+" "+str(humid_day))
        elif choic == "-a":
            month = input("Enter First three alphabets of Month: ")
            month = month[:1].upper() + month[1:3].lower()
            file = Path(FILE_PATH).rglob('*{date}_{month}.txt'.format(date=year, month=month))
            average_temp = average_temperature(clean_data(file))
            print("Highest Average: " + str(average_temp[0])+"C")
            print("Lowest Average:  " + str(average_temp[1])+"C")
            print("Humid Average:   " + str(average_temp[2])+"%")
        elif choic == "-c":
            month = input("Enter First three alphabets of Month: ")
            month = month[:1].upper() + month[1:3].lower()
            file = Path(FILE_PATH).rglob('*{date}_{month}.txt'.format(date=year, month=month))
            values = max_min(clean_data(file))
            for i in range(len(values[1])):
                _v = values[2][i].split('-')[2]
                print(_v, end="")
                for _x in range(int(values[0][i])):
                    print(Fore.RED, "+", end="")
                print()
                print(Fore.WHITE,_v, end="")
                for _x in range(int(values[1][i])):
                    print(Fore.BLUE, "+", end="")
                print(Fore.WHITE, str(values[0][i])+"-"+str(values[1][i]))
        else:
            print("invalid entry please try again")
    except ValueError:
        print("Please Enter existing path and valid choice")
        
main(CHOICE)