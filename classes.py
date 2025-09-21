from datetime import datetime
from user_preferences_class import User_Preferences
from pathlib import Path
import csv
import sqlite3


# Top level grouping of Activities
class Program:
    def __init__(self, name):
        self.name = ''
        if len(name) > 0:
            self.name = name

    def __str__(self):
        return f"{self.name}"

# One item of work for a Program
class Activity:
    def __init__(self,label,description=""):
        self.label = ''
        self.description = ''
            
        if len(label) > 0:
            self.label = label    
        
        if len(description) > 0:
            self.description = description
            
    def __str__(self):
        return f"{self.label} \t{self.description}"

# Everything needed to record work during a specific period of time
class Entry:
    def __init__(self,program,activity,start=datetime.now(),stop=datetime.now(),valid=1):
        self.program = program
        self.activity = activity
        self.start = start
        self.stop = stop
        self.valid = valid

    def __str__(self):
        return f"{self.program}: \t{self.activity} | \t\t{self.start} -> {self.stop} | \t{self.valid}"

    def time(self):
        diff = self.stop - self.start
        return f"{diff}"
    
    def delete(self):
        self.valid = 0

    def restore(self):
        self.valid = 1

    def start(self):
        self.start = datetime.now()

    def stop(self):
        self.stop = datetime.now()

# Group of Entries stored/read from CSV
class Log:
    def __init__(self,entries=[],csv_name=""):
        self.entries = []
        self.csv_name = ''

        if len(entries) > 0:
            self.entries = entries

        if len(csv_name) > 0:
            self.csv_name = csv_name
        
        self.headers = ['Program','Activity','Description','Start','Stop','Valid']

        self.log_con = sqlite3.connect("history.db")
        self.log_cur = self.log_con.cursor()
        return

    def set_csv_name(self,csv_name):
        self.csv_name = csv_name
        file_path = Path(self.csv_name)

        # Create the file and write headers if it doesn't exist
        if not file_path.exists():
            with open(file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(self.headers) # Write your desired headers

    def get_program_entries(self,name):
        found_entries = []
        for entry in self.entries:
            if entry.program.name == name:
                found_entries.append(entry)
        
        return found_entries

    def load_entries_from_db(self):
        self.load_entries("db")

    def load_entries_from_csv(self):
        self.load_entries("csv")

    def load_entries(self,type):
        if type == "csv":

            with open(self.csv_name, newline='') as f:
                reader = csv.reader(f)
                next(reader)  # Skips the header row

                for row in reader:
                    this_entry = Entry(Program(row[0]),Activity(row[1],row[2]),row[3],row[4],row[5])
                    self.entries.append(this_entry)
        else:
            res = self.log_cur.execute(f"SELECT * FROM history")
            data = res.fetchall()

            for d in data:
                this_entry = Entry(Program(d[0]),Activity(d[1],d[2]),d[3],d[4],d[5])
                self.entries.append(this_entry)

    def add_to_entries(self,entry):
        self.entries.append(entry)

    def store_entries(self,type="db"):

        if (type == "csv"):    
            with open(self.csv_name,mode="a",newline="",encoding='utf-8') as file:
                writer = csv.writer(file)

                for entry in self.entries:
                    writer.writerow([entry.program.name,entry.activity.label,
                                     entry.activity.description,entry.start,entry.stop,entry.valid])
        else:
            for entry in self.entries:
                self.log_cur.execute("""INSERT INTO history (program,activity,description,start,stop,valid) VALUES (?, ?, ?, ?, ?, ?);""",
                                    (entry.program.name,entry.activity.label,entry.activity.description,entry.start,entry.stop,entry.valid))
            self.log_con.commit()

        return

    def store_entries_in_db(self):
        self.store_entries("db")   

    def store_entries_in_csv(self):
        self.store_entries("csv")

    def reset_entire_history_from_database(self):
        self.log_cur.execute("DROP TABLE IF EXISTS history")
        self.log_cur.execute("CREATE TABLE history (program,activity,description,start,stop,valid)")
        self.log_con.commit()
        


