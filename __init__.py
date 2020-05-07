

import sqlite3

from flask import Markup

import datetime
import calendar
import random


# ----- creation of useful_data.sqlite file ------------------------------------
# to speed up the search for information by the sites, We create another sqlite
# file with only the information we use

def dates(sqlite_file):
    """
    pre sqlite_file(str) : sqlite file
    return (list) : list of dates between the first and the last date in
                    sqlite_file
    """
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    #append dates in sqlite file in dates list
    dates = []
    print("<dates> scanning file ...")
    for row in cursor.execute("SELECT submitted_on from submissions"):
        date = datetime.date(int(row[0][:4]),int(row[0][5:7]),int(row[0][8:10]))
        if date not in dates:
            dates.append(date)
    print("<dates> scanning done !")
    #sort dates list
    dates.sort()
    #if it miss dates between the first and the last date, append them
    for i in range(len(dates)-1):
        current_date = dates[i]
        next_day = current_date + datetime.timedelta(days=1)
        if dates[i+1] != next_day:
            dates.insert(i+1,next_day)
    #turn the dates into str
    str_dates = []
    for date in dates:
        str_dates.append(str(date))
    #return
    return str_dates

def results(sqlite_file, dates):
    """
    pre sqlite_file(str) : sqlite file
    pre dates(list) : list of dates
    return (dict) : a dict with dates in str form as keys and
    [submissions_number, success, failures, errors, LSINF1101-PYTHON, LEPL1402,
    LSINF1252, others] as values
    """
    #create a dict with dates in str form as keys and
    #[submissions_number, success, failures, errors, LSINF1101-PYTHON, LEPL1402,
    #LSINF1252, others] values
    dates_dict = {}
    for date in dates:
        dates_dict[date] = [0,0,0,0,0,0,0,0]
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    #count submissions_number, success, failures, errors and courses submissions  for each date
    print("<results> scanning file ...")
    for row in cursor.execute("SELECT submitted_on, result, course from submissions"):
        date = row[0][:10]
        dates_dict[date][0] += 1
        #sucess
        if row[1] == "success":
            dates_dict[date][1] += 1
        #failures
        elif row[1] == "failed":
            dates_dict[date][2] += 1
        #error
        elif row[1] != "success" and row[1] != "failed":
            dates_dict[date][3] += 1
        #LSINF1101-PYTHON
        if row[2] == "LSINF1101-PYTHON":
            dates_dict[date][4] += 1
        #LEPL1402
        elif row[2] == "LEPL1402":
            dates_dict[date][5] += 1
        #LSINF1252
        elif row[2] == "LSINF1252":
            dates_dict[date][6] += 1
        #other courses
        elif row[2] != "LSINF1252" and row[2] != "LEPL1402" and row[2] != "LSINF1101-PYTHON":
            dates_dict[date][7] += 1
    print("<results> scanning done !")
    #return
    return dates_dict

def create_submissions_table(file_name, results_dict):
    """
    pre file_name(str) : name of sqlite3 file created
    pre results_dict(dict) : a dict as {date: submission_number, success, failures, errors}
    post : create a submissions table with data as
           date, submission_number, success, failures, errors
    """
    #reach to file
    conn = sqlite3.connect(file_name)
    cursor = conn.cursor()
    #create table
    cursor.execute('''CREATE TABLE submissions
    (
      date  TEXT PRIMARY KEY    NOT NULL,
      submission_number  INT    NOT NULL,
      success INT               NOT NULL,
      failures  INT             NOT NULL,
      errors    INT             NOT NULL,
      LSINF1101_PYTHON INT      NOT NULL,
      LEPL1402  INT             NOT NULL,
      LSINF1252 INT             NOT NULL,
      other_courses INT        NOT NULL
    );''')
    for date in results_dict:
        submission_number = results_dict[date][0]
        success = results_dict[date][1]
        failures = results_dict[date][2]
        errors = results_dict[date][3]
        LSINF1101 = results_dict[date][4]
        LEPL1402 = results_dict[date][5]
        LSINF1252 = results_dict[date][6]
        other = results_dict[date][7]
        cursor.execute('''INSERT OR REPLACE INTO submissions (date, submission_number, success, failures, errors, LSINF1101_PYTHON, LEPL1402, LSINF1252, other_courses)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',(date, submission_number, success, failures, errors, LSINF1101, LEPL1402, LSINF1252, other))
    conn.commit()
    conn.close()


def results_courses(sqlite_file, dates):
    """
    pre sqlite_file(str) : sqlite file
    pre dates(list) : list of dates
    return (dict) : a dict with dates in str form as keys and
    [LSINF1101-PYTHON success, LSINF1101-PYTHON failures, LSINF1101-PYTHON errors,
    LEPL1402 success, LEPL1402 failures, LEPL1402 errors,
    LSINF1252 success, LSINF1252 failures, LSINF1252 errors] as values
    """
    #create a dict with dates in str form as keys and
    #[submissions_number, success, failures, errors, LSINF1101-PYTHON, LEPL1402,
    #LSINF1252, others] values
    dates_dict = {}
    for date in dates:
        dates_dict[date] = [0,0,0,0,0,0,0,0,0]
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    #count submissions_number, success, failures, errors and courses submissions  for each date
    print("<results_courses> scanning file ...")
    for row in cursor.execute("SELECT submitted_on, result, course from submissions"):
        date = row[0][:10]
        #LSINF1101-PYTHON
        if row[2] == "LSINF1101-PYTHON":
            #sucess
            if row[1] == "success":
                dates_dict[date][0] += 1
            #failures
            elif row[1] == "failed":
                dates_dict[date][1] += 1
            #error
            elif row[1] != "success" and row[1] != "failed":
                dates_dict[date][2] += 1
        #LEPL1402
        elif row[2] == "LEPL1402":
            #sucess
            if row[1] == "success":
                dates_dict[date][3] += 1
            #failures
            elif row[1] == "failed":
                dates_dict[date][4] += 1
            #error
            elif row[1] != "success" and row[1] != "failed":
                dates_dict[date][5] += 1
        #LSINF1252
        elif row[2] == "LSINF1252":
            #sucess
            if row[1] == "success":
                dates_dict[date][6] += 1
            #failures
            elif row[1] == "failed":
                dates_dict[date][7] += 1
            #error
            elif row[1] != "success" and row[1] != "failed":
                dates_dict[date][8] += 1
    print("<results_courses> scanning done !")
    #return
    return dates_dict

def create_courses_table(file_name, results_dict):
    """
    pre file_name(str) : name of sqlite3 file created
    pre results_dict(dict) : a dict as {date: submission_number, success, failures, errors}
    post : creat a submissions table with data as
           date, submission_number, success, failures, errors
    """
    #reach to file
    conn = sqlite3.connect(file_name)
    cursor = conn.cursor()
    #create table
    cursor.execute('''CREATE TABLE courses
    (
      date  TEXT PRIMARY KEY        NOT NULL,
      LSINF1101_PYTHON_success  INT NOT NULL,
      LSINF1101_PYTHON_failures INT NOT NULL,
      LSINF1101_PYTHON_errors  INT  NOT NULL,
      LEPL1402_success    INT       NOT NULL,
      LEPL1402_failures INT         NOT NULL,
      LEPL1402_errors  INT          NOT NULL,
      LSINF1252_success INT         NOT NULL,
      LSINF1252_failures INT        NOT NULL,
      LSINF1252_errors INT          NOT NULL
    );''')
    #insert values
    for date in results_dict:
        LSINF1101_PYTHON_success = results_dict[date][0]
        LSINF1101_PYTHON_failures = results_dict[date][1]
        LSINF1101_PYTHON_errors = results_dict[date][2]
        LEPL1402_success = results_dict[date][3]
        LEPL1402_failures = results_dict[date][4]
        LEPL1402_errors = results_dict[date][5]
        LSINF1252_success = results_dict[date][6]
        LSINF1252_failures = results_dict[date][7]
        LSINF1252_errors = results_dict[date][8]
        cursor.execute('''INSERT OR REPLACE INTO courses (date, LSINF1101_PYTHON_success, LSINF1101_PYTHON_failures, LSINF1101_PYTHON_errors, LEPL1402_success, LEPL1402_failures, LEPL1402_errors, LSINF1252_success, LSINF1252_failures, LSINF1252_errors)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',(date, LSINF1101_PYTHON_success, LSINF1101_PYTHON_failures, LSINF1101_PYTHON_errors, LEPL1402_success, LEPL1402_failures, LEPL1402_errors, LSINF1252_success, LSINF1252_failures, LSINF1252_errors))
    #commit and close
    conn.commit()
    conn.close()


def tasks(sqlite_file, dates):
    """
    pre sqlite_file(str) : sqlite file
    pre dates(list) : list of dates
    return (list) : list of tasks in each course as
                    [LSINF1101_PYTHON_tasks, LEPL1402_tasks, LSINF1252_tasks]
    """
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    #list of tasks in each course
    LSINF1101_PYTHON_tasks = []
    LEPL1402_tasks = []
    LSINF1252_tasks = []
    #find tasks for each course
    print("<tasks> scanning file ...")
    for row in cursor.execute("SELECT course, task from submissions"):
        if row[0] == "LSINF1101-PYTHON":
            if row[1] not in LSINF1101_PYTHON_tasks:
                LSINF1101_PYTHON_tasks.append(row[1])
        elif row[0] == "LEPL1402":
            if row[1] not in LEPL1402_tasks:
                LEPL1402_tasks.append(row[1])
        elif row[0] == "LSINF1252":
            if row[1] not in LSINF1252_tasks:
                LSINF1252_tasks.append(row[1])
    print("<tasks> scanning done !")
    #return
    return [LSINF1101_PYTHON_tasks, LEPL1402_tasks, LSINF1252_tasks]

def LSINF1101_PYTHON_tasks(sqlite_file, dates):
    """
    pre sqlite_file(str) : sqlite file
    pre dates(list) : list of dates
    return (dict) : a dict with dates in str form as keys and
    [task1 submissions, ..., taskn submissions] as values
    """
    l_tasks = tasks(sqlite_file, dates) #list of tasks as [LSINF1101_PYTHON_tasks, LEPL1402_tasks, LSINF1252_tasks]
    #create dict as {date : {task : submissions number}}
    dates_dict = {}
    for date in dates:
        tasks_dict = {}
        for task in l_tasks[0]: #tasks in LSINF1101-PYTHON
            tasks_dict[task] = 0
        dates_dict[date] = tasks_dict
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    #count submissions number for each date
    print("<LSINF1101_PYTHON_tasks> scanning file ...")
    for row in cursor.execute("SELECT submitted_on, course, task from submissions"):
        date = row[0][:10]
        if row[1] == "LSINF1101-PYTHON":
            dates_dict[date][row[2]] += 1
    print("<LSINF1101_PYTHON_tasks> scanning done !")
    #return
    return dates_dict

def create_LSINF1101_PYTHON_table(file_name, results_dict):
    """
    pre file_name(str) : name of sqlite3 file created
    pre results_dict(dict) : a dict as {date: {task : n_submissions}}
    post : create LSINF1101_PYTHON table with data as
           date, task1 submissions, ..., taskn submissions
    """
    #reach to file
    conn = sqlite3.connect(file_name)
    cursor = conn.cursor()
    #create table
    table = '''CREATE TABLE LSINF1101_PYTHON ( date  TEXT PRIMARY KEY        NOT NULL'''
    for task in results_dict['2019-02-04']:
        #turn invalid name of task to a valid name
        if task == "2degree":
            task = "twodegree"
        elif task == "2degree2":
            task = "twodegree2"
        table += ", " + task.replace("-","_") + " INT NOT NULL"
    table += ");"
    cursor.execute(table)
    #insert = command to insert values
    insert = "INSERT OR REPLACE INTO LSINF1101_PYTHON (date"
    for task in results_dict['2019-02-04']:
        if task == "2degree":
            task = "twodegree"
        elif task == "2degree2":
            task = "twodegree2"
        insert += " , " + task.replace("-","_")
    insert += ") VALUES (?"
    for task in range(len(results_dict['2019-02-04'])):
        insert += ", ?"
    insert += ")"
    #insert values
    for date in results_dict:
        values = (date,)
        for task in results_dict[date].values():
            values += (task,)
        cursor.execute(insert,values)
    #commit and close
    conn.commit()
    conn.close()


def LEPL1402_tasks(sqlite_file, dates):
    """
    pre sqlite_file(str) : sqlite file
    pre dates(list) : list of dates
    return (dict) : a dict with dates in str form as keys and
    [task1 submissions, ..., taskn submissions] as values
    """
    l_tasks = tasks(sqlite_file, dates) #list of tasks as [LSINF1101_PYTHON_tasks, LEPL1402_tasks, LSINF1252_tasks]
    #create dict as {date : {task : submissions number}}
    dates_dict = {}
    for date in dates:
        tasks_dict = {}
        for task in l_tasks[1]: #tasks in LEPL1402
            tasks_dict[task] = 0
        dates_dict[date] = tasks_dict
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    #count submissions number for each date
    print("<LEPL1402_tasks> scanning file ...")
    for row in cursor.execute("SELECT submitted_on, course, task from submissions"):
        date = row[0][:10]
        if row[1] == "LEPL1402":
            dates_dict[date][row[2]] += 1
    print("<LEPL1402_tasks> scanning done !")
    #return
    return dates_dict

def create_LEPL1402_table(file_name, results_dict):
    """
    pre file_name(str) : name of sqlite3 file created
    pre results_dict(dict) : a dict as {date: {task : n_submissions}}
    post : create LSINF1101_PYTHON table with data as
           date, task1 submissions, ..., taskn submissions
    """
    #reach to file
    conn = sqlite3.connect(file_name)
    cursor = conn.cursor()
    #create table
    table = '''CREATE TABLE LEPL1402 ( date  TEXT PRIMARY KEY        NOT NULL'''
    for task in results_dict['2019-02-04']:
        table += ", " + task.replace("-","_") + " INT NOT NULL"
    table += ");"
    cursor.execute(table)
    #insert = command to insert values
    insert = "INSERT OR REPLACE INTO LEPL1402 (date"
    for task in results_dict['2019-02-04']:
        insert += " , " + task.replace("-","_")
    insert += ") VALUES (?"
    for task in range(len(results_dict['2019-02-04'])):
        insert += ", ?"
    insert += ")"
    #insert values
    for date in results_dict:
        values = (date,)
        for task in results_dict[date].values():
            values += (task,)
        cursor.execute(insert,values)
    #commit and close
    conn.commit()
    conn.close()


def LSINF1252_tasks(sqlite_file, dates):
    """
    pre sqlite_file(str) : sqlite file
    pre dates(list) : list of dates
    return (dict) : a dict with dates in str form as keys and
    [task1 submissions, ..., taskn submissions] as values
    """
    l_tasks = tasks(sqlite_file, dates) #list of tasks as [LSINF1101_PYTHON_tasks, LEPL1402_tasks, LSINF1252_tasks]
    #create dict as {date : {task : submissions number}}
    dates_dict = {}
    for date in dates:
        tasks_dict = {}
        for task in l_tasks[2]: #tasks in LSINF1252
            tasks_dict[task] = 0
        dates_dict[date] = tasks_dict
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    #count submissions_number for each date
    print("<LSINF1252_tasks> scanning file ...")
    for row in cursor.execute("SELECT submitted_on, course, task from submissions"):
        date = row[0][:10]
        if row[1] == "LSINF1252":
            print(row[2])
            dates_dict[date][row[2]] += 1
    print("<LSINF1252_tasks> scanning done !")
    #return
    return dates_dict

def create_LSINF1252_table(file_name, results_dict):
    """
    pre file_name(str) : name of sqlite3 file created
    pre results_dict(dict) : a dict as {date: {task : n_submissions}}
    post : create LSINF1252 table with data as
           date, task1, ..., taskn
    """
    #reach to file
    conn = sqlite3.connect(file_name)
    cursor = conn.cursor()
    #create table
    table = '''CREATE TABLE LSINF1252 ( date  TEXT PRIMARY KEY        NOT NULL'''
    for task in results_dict['2019-02-04']:
        table += ", " + task.replace("-","_") + " INT NOT NULL"
    table += ");"
    cursor.execute(table)
    #insert = command to insert values
    insert = "INSERT OR REPLACE INTO LSINF1252 (date"
    for task in results_dict['2019-02-04']:
        insert += " , " + task.replace("-","_")
    insert += ") VALUES (?"
    for task in range(len(results_dict['2019-02-04'])):
        insert += ", ?"
    insert += ")"
    #insert values
    for date in results_dict:
        values = (date,)
        for task in results_dict[date].values():
            values += (task,)
        cursor.execute(insert,values)
    #commit and close
    conn.commit()
    conn.close()

# ----- Execution -----

# l = dates("data_inginious.sqlite")
# d = results("data_inginious.sqlite",l)
# create_submissions_table("useful_data.sqlite", d)

# d = results_courses("data_inginious.sqlite",l)
# create_courses_table("useful_data.sqlite", d)

# d = LSINF1101_PYTHON_tasks("data_inginious.sqlite", l)
# create_LSINF1101_PYTHON_table("useful_data.sqlite", d)

# d = LEPL1402_tasks("data_inginious.sqlite", l)
# create_LEPL1402_table("useful_data.sqlite", d)

# d = LSINF1252_tasks("data_inginious.sqlite", l)
# create_LSINF1252_table("useful_data.sqlite", d)

# ----- Use useful_data.sqlite file --------------------------------------------

def date_reverse(date):
    """
    pre date(str) : date in dd-mm-yyyy format
    return (str) : date reversed as yyyy-mm-dd
    """
    return date[7:]+"-"+date[3:5]+"-"+date[:2]

def select_dates(sqlite_file, start_date, end_date):
    """
    pre dates(list) : liste of dates as [yyyy-mm-dd, yyyy-mm-dd]
    pre start_date(str) : date as yyyy-mm-dd
    pre end_date(str) : date as yyyy-mm-dd
    return (list) : list of dates in "dates" between "start_date" and
                    "end_date"
    """
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    result = []
    #turn  start_date and end_date into date object
    sd_object = datetime.date(int(start_date[:4]),int(start_date[5:7]),int(start_date[8:10]))
    ed_object = datetime.date(int(end_date[:4]),int(end_date[5:7]),int(end_date[8:10]))
    #check if start_date < end_date
    if ed_object < sd_object:
        return None
    #check id start_date and end_date in sqlite_file
    if sd_object < datetime.date(2019,2,4) or sd_object > datetime.date(2020,2,16):
        return None
    if ed_object < datetime.date(2019,2,4) or ed_object > datetime.date(2020,2,16):
        return None
    #put each date between start_date and end_date in result
    for row in cursor.execute("SELECT date from submissions"):
        current_date = datetime.date(int(row[0][:4]),int(row[0][5:7]),int(row[0][8:10]))
        if current_date >= sd_object:
            result.append(str(current_date))
        if current_date >= ed_object: #stop loop when the end_date has passed
            break
    return result

def calc_intervals(dates, interval):
    """
    pre dates(list) : liste of dates as [yyyy-mm-dd, yyyy-mm-dd]
    pre interval(int) : interval between two dates as "day", "week," "month" or
                        "year"
    return (list) : list of interal as [(yyyy-mm-dd, yyyy-mm-dd, yyyy-mm-dd, yyyy-mm-dd)]
    """
    intervals = []
    #interval = day
    if interval == "day":
        for date in dates:
            intervals.append((date,date))
        #return day intervals
        return intervals
    #interval = week
    elif interval == "week":
        first = dates[0]
        for date in dates:
            date_object = datetime.date(int(date[:4]),int(date[5:7]),int(date[8:10]))
            #date = monday
            if date_object.weekday() == 0:
                first = date
            #date = sunday
            elif date_object.weekday() == 6:
                last = date
                intervals.append((first, last))
        if intervals[-1][0] != first:
            intervals.append((first, date))
        #return week intervals
        return intervals
    #interval = month
    elif interval == "month":
        first = dates[0]
        for date in dates:
            date_object = datetime.date(int(date[:4]),int(date[5:7]),int(date[8:10]))
            monthrange = calendar.monthrange(int(date[:4]),int(date[5:7]))[1]
            #date = first day of month
            if date_object.day == 1:
                first = date
            #date = last day of month
            elif date_object.day == monthrange:
                last = date
                intervals.append((first,last))
        if date_object.day != monthrange:
            intervals.append((first,date))
        #return month intervals
        return intervals
    #interval = year
    elif interval == "year":
        first = dates[0]
        for date in dates:
            #date is the 1st Jan
            if int(date[5:7]) == 1 and int(date[8:10]) == 1:
                first = date
            #date is the 31th Dec
            elif int(date[5:7]) == 12 and int(date[8:10]) == 31:
                last = date
                intervals.append((first,last))
        if first[:4] != last[:4]:
            intervals.append((first, date))
        #return month intervals
        return intervals

def is_in_interval(date, interval):
    """
    pre date(str) : date as yyyy-mm-dd, yyyy-mm-dd
    pre interval(tuple) : interval as (yyyy-mm-dd, yyyy-mm-dd, yyyy-mm-dd, yyyy-mm-dd)
    return (bool) : date is in interval
    """
    date = datetime.date(int(date[:4]),int(date[5:7]),int(date[8:10]))
    fd = datetime.date(int(interval[0][:4]),int(interval[0][5:7]),int(interval[0][8:10]))
    ed = datetime.date(int(interval[1][:4]),int(interval[1][5:7]),int(interval[1][8:10]))
    if date >= fd and date <= ed:
        return True
    return False

def percentage(data_list):
    """
    pre data_list(list/tuple)
    return (list) : the percentage for each data in listS
    """
    result = []
    #count the number of elements
    total_elements = sum(data_list)
    #put the percentages of element in list
    for data in data_list:
        result.append(data/total_elements*100)
    return result

# ----- Charts -----

def chart_global(sqlite_file, start_date, end_date, interval):
    """
    pre sqlite_file(str) : sqlite file
    pre start_date(str) : start date as yyyy-mm-dd
    pre end_date(str) : end date as yyyy-mm-dd
    pre interval(int) : interval between two dates as "day", "week," "month" or
                        "year"
    return (list) : chart_setup of data
    """
    intervals_dict = {}
    data_list = []
    labels_list = []
    #select dates
    dates = select_dates(sqlite_file, start_date, end_date)
    #check if date is in sqlite file
    if dates == None:
        return None
    #calc calc_intervals
    intervals = calc_intervals(dates,interval)
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * from submissions"):
        date = row[0]
        for interval in intervals:
            if is_in_interval(date, interval):
                if intervals_dict.get(interval,-1) == -1:
                    intervals_dict[interval] = row[1]
                else:
                    intervals_dict[interval] += row[1]
    for key in intervals_dict:
        #turn date in yyyy-mm-dd form into dd/mm/yy form
        label = key[0][8:10]+"/"+key[0][5:7]+"/"+key[0][:4]+" - "+key[1][8:10]+"/"+key[1][5:7]+"/"+key[1][:4]
        labels_list.append(label)
        data_list.append(intervals_dict[key])
    print("<chart_global>",labels_list,data_list)
    return chart_setup(type = 'bar', labels = labels_list, datas = data_list, extra_options = '{legend: { display: false}}')

def chart_details(sqlite_file, interval, mode):
    """
    pre sqlite_file(str) : sqlite file
    pre interval(tuple) : a interval as (yyyy-mm-dd, yyyy-mm-dd, yyyy-mm-dd, yyyy-mm-dd)
    pre mode(str) : - "value"
                    - "percentage"
    return (list) : chart_setup of data
    """
    results_dict = {'total': 0, 'success': 0, 'failures': 0, 'errors': 0}
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * from submissions"):
        date = row[0]
        date_object = datetime.date(int(date[:4]),int(date[5:7]),int(date[8:10]))
        latest_date_object = datetime.date(int(interval[1][:4]),int(interval[1][5:7]),int(interval[1][8:10]))
        if is_in_interval(date, interval):
            results_dict['total'] += row[1]
            results_dict['success'] += row[2]
            results_dict['failures'] += row[3]
            results_dict['errors'] += row[4]
        elif date_object > latest_date_object:
            break
    #turn sucess, failures and errors into percentage form
    if mode == "percentage":
        values = list(results_dict.values())[1:]
        percs = percentage(values)
        results_dict["success"] = percs[0]
        results_dict["failures"] = percs[1]
        results_dict["errors"] = percs[2]
    print("<chart_details>",[results_dict['total'],results_dict['success'],results_dict['failures'],results_dict['errors']])
    return round(float(results_dict['total']),2), round(float(results_dict['success']),2),round(float(results_dict['failures']),2),round(float(results_dict['errors']),2)

def chart_courses(sqlite_file, interval, mode):
    """
    pre sqlite_file(str) : sqlite file
    pre interval(tuple) : a interval as (yyyy-mm-dd, yyyy-mm-dd, yyyy-mm-dd, yyyy-mm-dd)
    pre mode(str) : - "value"
                    - "percentage"
    return (list) : chart_setup of data
    """
    courses_dict = {'LSINF1101_PYTHON': 0, 'LEPL1402': 0, 'LSINF1252': 0}
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * from submissions"):
        date = row[0]
        date_object = datetime.date(int(date[:4]),int(date[5:7]),int(date[8:10]))
        latest_date_object = datetime.date(int(interval[1][:4]),int(interval[1][5:7]),int(interval[1][8:10]))
        if is_in_interval(date, interval):
            courses_dict['LSINF1101_PYTHON'] += row[5]
            courses_dict['LEPL1402'] += row[6]
            courses_dict['LSINF1252'] += row[7]
        elif date_object > latest_date_object:
            break
    #turn data into percentage
    if mode == "percentage":
        values = list(courses_dict.values())
        percs = percentage(values)
        for key in courses_dict:
            courses_dict[key] = percs[0]
            del percs[0]
    print("<chart_courses>",[courses_dict['LSINF1101_PYTHON'],courses_dict['LEPL1402'],courses_dict['LSINF1252']])
    return chart_setup(type = 'pie', labels = ['LSINF1101_PYTHON','LEPL1402','LSINF1252'], datas = [courses_dict['LSINF1101_PYTHON'],courses_dict['LEPL1402'],courses_dict['LSINF1252']], extra_options = "{legend: {display: false}}"     )

def chart_global_courses(sqlite_file, start_date, end_date, interval, course):
    """
    pre sqlite_file(str) : sqlite file
    pre start_date(str) : start date as yyyy-mm-dd
    pre end_date(str) : end date as yyyy-mm-dd
    pre interval(int) : interval between two dates as "day", "week," "month" or
                        "year"
    pre course(str) : course as 'LSINF1101_PYTHON', 'LEPL1402' or 'LSINF1252'
    return (list) : chart_setup of data
    """
    intervals_dict = {}
    data_list = []
    labels_list = []
    #course
    if course == 'LSINF1101_PYTHON':
        c = 5
    elif course == 'LEPL1402':
        c = 6
    elif course == 'LSINF1252':
        c = 7
    else:
        raise Exception("No course {}".format(course))
    #select dates
    dates = select_dates(sqlite_file, start_date, end_date)
    #check if date is in sqlite file
    if dates == None:
        raise Exception("Date no existing")
    #calc calc_intervals
    intervals = calc_intervals(dates,interval)
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * from submissions"):
        date = row[0]
        for interval in intervals:
            if is_in_interval(date, interval):
                if intervals_dict.get(interval,-1) == -1:
                    intervals_dict[interval] = row[c]
                else:
                    intervals_dict[interval] += row[c]
    for key in intervals_dict:
        #turn date in yyyy-mm-dd form into dd/mm/yy form
        label = key[0][8:10]+"/"+key[0][5:7]+"/"+key[0][:4]+" - "+key[1][8:10]+"/"+key[1][5:7]+"/"+key[1][:4]
        labels_list.append(label)
        data_list.append(intervals_dict[key])
    print("<chart_global>",labels_list,data_list)
    return chart_setup(type = 'bar', labels = labels_list, datas = data_list, extra_options = '{legend: { display: false}}')

def chart_details_courses(sqlite_file, interval, mode, course):
    """
    pre sqlite_file(str) : sqlite file
    pre interval(tuple) : a interval as (yyyy-mm-dd, yyyy-mm-dd, yyyy-mm-dd, yyyy-mm-dd)
    pre mode(str) : - "value"
                    - "percentage"
    pre course(str) : course as 'LSINF1101_PYTHON', 'LEPL1402' or 'LSINF1252'
    return (list) : chart_setup of data
    """
    #course
    if course == 'LSINF1101_PYTHON':
        c = 1
    elif course == 'LEPL1402':
        c = 4
    elif course == 'LSINF1252':
        c = 7
    else:
        raise Exception("No course {}".format(course))
    results_dict = {'total': 0, 'success': 0, 'failures': 0, 'errors': 0}
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    #count total, success, failures and errors for course chosen
    for row in cursor.execute("SELECT * from courses"):
        date = row[0]
        date_object = datetime.date(int(date[:4]),int(date[5:7]),int(date[8:10]))
        latest_date_object = datetime.date(int(interval[1][:4]),int(interval[1][5:7]),int(interval[1][8:10]))
        if is_in_interval(date, interval):
            total = 0
            results_dict['success'] += row[c]
            total += row[c]
            results_dict['failures'] += row[c+1]
            total += row[c+1]
            results_dict['errors'] += row[c+2]
            total += row[c+2]
            results_dict['total'] += total
        elif date_object > latest_date_object:
            break
    #turn sucess, failures and errors into percentage form
    if mode == "percentage":
        values = list(results_dict.values())[1:]
        percs = percentage(values)
        results_dict["success"] = percs[0]
        results_dict["failures"] = percs[1]
        results_dict["errors"] = percs[2]
    print("<chart_details>",[results_dict['total'],results_dict['success'],results_dict['failures'],results_dict['errors']])
    return round(float(results_dict['total']),2), round(float(results_dict['success']),2),round(float(results_dict['failures']),2),round(float(results_dict['errors']),2)

def chart_task(sqlite_file, interval, mode, course):
    """
    pre sqlite_file(str) : sqlite file
    pre interval(tuple) : a interval as (yyyy-mm-dd, yyyy-mm-dd, yyyy-mm-dd, yyyy-mm-dd)
    pre mode(str) : - "value"
                    - "percentage"
    pre course(str) : course as 'LSINF1101_PYTHON', 'LEPL1402' or 'LSINF1252'
    return (list) : chart_setup of data
    """
    #reach to file
    conn = sqlite3.connect("useful_data.sqlite")
    cursor = conn.cursor()
    results_list = []
    #put [0, task] in results_list
    for x in list(cursor.execute("select * from pragma_table_info('"+course+"')"))[1:] :
        results_list.append([0,x[1]])
    #count submissions submissions of each task
    for row in cursor.execute("SELECT * from "+course):
        date = row[0]
        date_object = datetime.date(int(date[:4]),int(date[5:7]),int(date[8:10]))
        latest_date_object = datetime.date(int(interval[1][:4]),int(interval[1][5:7]),int(interval[1][8:10]))
        if is_in_interval(date, interval):
            i = 0
            for column in row[1:]:
                results_list[i][0] += column
                i += 1
        elif date_object > latest_date_object:
            break
    #find the 3 max and put them into results_dict
    results_dict = {}
    for x in range(3):
        i_max = results_list.index(max(results_list))
        results_dict[results_list[i_max][1]] = results_list[i_max][0]
        del results_list[i_max]
    #other execrices
    results_dict["Others"] = 0
    for result in results_list:
        results_dict["Others"] += 1
    #list of lables
    labels_list = []
    for key in results_dict.keys():
        labels_list.append(key)
    #list of values
    values_list = []
    for value in results_dict.values():
        values_list.append(value)
    #turn values in purcentage
    if mode == "percentage":
        percs = percentage(values_list)
        values_list[0] = percs[0]
        values_list[1] = percs[1]
        values_list[2] = percs[2]
        values_list[3] = percs[3]
    print("<chart_task>",labels_list, values_list)
    return chart_setup(type = 'pie', labels = labels_list, datas = values_list, extra_options = "{legend: {display: false}}")


def random_rgb():
    """
    Choose random rbg colors
    """
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    return 'rgba({}, {}, {}, {})'.format(r,g,b,0.8)

def date_reverse(date):
    """
    pre date(str) : date in dd-mm-yyyy format
    return (str) : date reversed as yyyy-mm-dd
    """
    return date[7:]+"-"+date[3:5]+"-"+date[:2]

def chart_setup(type, labels, datas, background_color=None, border_color=None, extra_options=None):
    """
    pre : configuration for the chart
    return (str) : configuration for the chart in js format
    """

    label = []
    data = []
    backgroundColor = []
    borderColor = []

    for i in labels:
        label.append(i)
    for i in datas:
        data.append(i)

    if background_color is None and border_color is None:
        for i in labels:
            color = random_rgb()
            backgroundColor.append(color)
            borderColor.append(color)

    else:
        for i in background_color:
            backgroundColor.append(i)
        for i in border_color:
            borderColor.append(i)


    if extra_options is not None:
        return Markup("{{ 'type': '{0}',  'data': {{ 'labels': {1}, 'datasets': [{{ 'data': {2}, 'backgroundColor': {3}, 'borderColor': {4} }}] }}, 'options' : {5} }}".format(type, labels, datas, backgroundColor, borderColor ,extra_options))
    else:
        return Markup("{{ 'type': '{0}',  'data': {{ 'labels': {1}, 'datasets': [{{ 'data': {2}, 'backgroundColor': {3}, 'borderColor': {4} }}] }} }}".format(type, labels, datas, backgroundColor, borderColor))
