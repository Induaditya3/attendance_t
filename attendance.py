import sqlite3
import os
from datetime import datetime, date
# first create way to store persistent data 
## use json to store dicts
## OR
## use csv file to record the data
## OR
## use sqlite db
## since querying a table from db is  fastest 
## so db  is settled

# no of tables files to maintain
## using separate table for each subject is more logical

# things to store in each table 
## date - obviously. in the form of year-month-day format with padding
## day - which day. as three letter abbreviation such as Sun,Mon,Tue,Wed,Thr,Fri,Sat.
## attend - to store present,absent,holiday as P,A,H

# cd to home and create a dir 'attendance_data' and cd into it
home_directory = os.path.expanduser('~')
os.chdir(home_directory)
try:
    os.mkdir("attendance_data")
    os.chdir("attendance_data")
except FileExistsError:
    os.chdir("attendance_data")
except Exception as e:
    print(f"An error occurred: {e}")

# create a db attendance with subject abbreviations as table inside the attendance_data dir
conn = sqlite3.connect("attend.db")
cursor = conn.cursor()

# create dict conataining all subjects wtih values as the name of tables
subjects = {
    "Analog & Digital Electronics" : "ade",
    "Data Structure & Algorithm" : "dsa",
    "Computer Organization" : "co",
    "Linear Algebra" : "la",
    "Economics for Engineers" : "e",
    "Analog & Digital Electronics Lab" : "adel",
    "Data Structure & Algorithm Lab" : "dsal",
    "Computer Organization Lab" : "col",
    "IT Workshop" : "it" 
}

# fields or header in table
fieldnames = ["date", "day", "attend"]
# create tables with required columns
for table in subjects.values():
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table} (
        id INTEGER PRIMARY KEY,
        date TEXT,
        day TEXT,
        attend TEXT
    )
    """)
    conn.commit()

# routine as dict for each day as key and list of subjects as values
routine = {
    "Mon" : [
        "Computer Organization",
        "Analog & Digital Electronics",
        "Economics for Engineers",
        "IT Workshop",
        "Analog & Digital Electronics Lab"
        ],
    "Tue" : [
        "Analog & Digital Electronics",
        "Computer Organization",
        "Economics for Engineers"
    ],
    "Wed" : [
        "Economics for Engineers",
        "Data Structure & Algorithm",
        "Data Structure & Algorithm Lab",
        "Linear Algebra",
        "Computer Organization Lab"
    ],
    "Thu" : [
        "Data Structure & Algorithm",
        "Computer Organization",
        "Computer Organization Lab"
    ],
    "Fri" : [
        "Linear Algebra",
        "Data Structure & Algorithm",
        "Analog & Digital Electronics",
        "IT Workshop",
        "Data Structure & Algorithm Lab"
    ],
    "Sat" : [],
    "Sun" : []
}
def markAttend(given_date,attend):
    try:
        dateobj = datetime.strptime(given_date,"%Y-%m-%d")
        weekday = dateobj.strftime("%a")
        for subject, table in subjects.items():
            if subject in routine[weekday]:
                cursor.execute(f"""
                INSERT INTO {table}
                (date, day, attend) 
                VALUES (?,?,?);
                           """, (given_date,weekday,attend))
                conn.commit()
    except ValueError:
        print("problem")

# show current percentage of present in each subject
def stat():
    for subject, table in subjects.items():
        res = cursor.execute(f"""SELECT COUNT(*) from {table} 
                       WHERE attend = 'P';
                       """)
        present = float(res.fetchone()[0])
        res = cursor.execute(f"""SELECT COUNT(*) from {table} 
                       WHERE attend = 'A';
                       """)
        absent = float(res.fetchone()[0])
        print(f"{subject} : {100*present/(present+absent)}")
# print(date.today())
# current_datetime = datetime.now()
# weekday = current_datetime.strftime("%a")
# print(len(weekday))

stat()

# close the connection
conn.close()
