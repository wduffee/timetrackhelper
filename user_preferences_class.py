import sqlite3

# Utility class to manage internal database
class User_Preferences:
    def __init__(self):
        self.up_con = sqlite3.connect("info.db")
        self.up_cur = self.up_con.cursor()
        return
    
    # Resets the internal database
    def reset_preferences(self):
        self.up_cur.execute("DROP TABLE IF EXISTS programs")
        self.up_cur.execute("DROP TABLE IF EXISTS activities")
        self.up_cur.execute("CREATE TABLE programs (name UNIQUE,active)")
        self.up_cur.execute("CREATE TABLE activities (label UNIQUE,active)")
        self.up_con.commit()

        
    # Enter program and activity title strings into the internal database
    # If already present, update to the specified active value
    def store_content(self,content_type,content,active=1):
        if content_type == "programs":
            self.up_cur.execute("""INSERT INTO programs (name, active) VALUES (?, ?) ON CONFLICT(name) DO UPDATE SET active = ?;""",(content,active,active))
        elif content_type == "activities":
            self.up_cur.execute("""INSERT INTO activities (label, active) VALUES (?, ?) ON CONFLICT(label) DO UPDATE SET active = ?;""",(content,active,active))
        self.up_con.commit()

    def store_program(self, program_name="",active=1):
        self.store_content("programs",program_name,active)

    def store_activity(self,activity_name="",active=1):
        self.store_content("activities",activity_name,active)

    def mark_program_inactive(self,content):
        self.store_content("programs",content,0)
    
    def mark_activity_inactive(self,content):
        self.store_content("activities",content,0)

    # Gets program and activity title strings from the internal database
    def get_content(self, content_type, active=1):
        if active >= 0:
            res = self.up_cur.execute(f"SELECT * FROM {content_type} WHERE active = {active}")
        else: 
            res = self.up_cur.execute(f"SELECT * FROM {content_type}")
        data = res.fetchall()
        return data
    
    def get_programs(self):
        return self.get_content("programs",-1)
    
    def get_active_programs(self):
        return self.get_content("programs",1)

    def get_inactive_programs(self):
        return self.get_content("programs",0)
    
    def get_activities(self):
        return self.get_content("activities",-1)
    
    def get_active_activities(self):
        return self.get_content("activities",1)
    
    def get_inactive_activities(self):
        return self.get_content("activities",0)