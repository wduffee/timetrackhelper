from datetime import datetime
from user_preferences_class import User_Preferences
import pandas as pd
from pathlib import Path
import csv

# Top level grouping of Activities
class Program:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"

# One item of work for a Program
class Activity:
    def __init__(self,label,description=""):
        self.label = label
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
        return f"{self.program}: \t{self.activity} | \t\t{self.start} -> {self.stop}"

    def time(self):
        diff = self.stop - self.start
        return f"{diff}"
    
    def delete(self):
        self.valid = 0

    def restore(self):
        self.valid = 1

# Group of Entries stored/read from CSV
class Log:
    def __init__(self,entries=[],csv_name=""):
        self.entries = entries
        self.csv_name = csv_name
        self.headers = ['Program','Activity','Description','Start','Stop','Valid']

    def set_csv_name(self,csv_name):
        print(f"Working with this csv_name: {self.csv_name}")

        self.csv_name = csv_name

        file_path = Path(self.csv_name)

        # Create the file and write headers if it doesn't exist
        if not file_path.exists():
            with open(file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(self.headers) # Write your desired headers
            print(f"CSV file '{file_path}' created with headers.")
        else:
            print(f"CSV file '{file_path}' already exists.")


    def get_program_entries(self,name):
        found_entries = []
        for entry in self.entries:
            if entry.program.name == name:
                found_entries.append(entry)
        
        return found_entries

    def load_entries_from_csv(self):
        print(f"Loading entries from this csv_name: {self.csv_name}")
        df = pd.read_csv(self.csv_name)

        for row_tuple in df.itertuples():

            this_entry = Entry(Program(row_tuple.Program),Activity(row_tuple.Activity,row_tuple.Description),row_tuple.Valid)
            this_entry.start = row_tuple.Start
            this_entry.stop = row_tuple.Stop

            self.entries.append(this_entry)

        return df
    
    def add_to_entries(self,entry):
        self.entries.append(entry)

    def store_entries_in_csv(self,overwrite=False):

        print(f"Storing data in {self.csv_name}")

        data_for_df = [{"Program":entry.program.name, "Activity":entry.activity.label, "Description":entry.activity.description, 
                        "Start": entry.start, "Stop": entry.stop,"Valid":entry.valid} for entry in self.entries]

        df = pd.DataFrame(data_for_df)

        # Write to CSV
        if overwrite:
            df.to_csv(self.csv_name, index=False)
        else:
           df.to_csv(self.csv_name,mode='a', header=False, index=False)


