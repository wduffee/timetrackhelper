from classes import *
from user_preferences_class import *

print("----------------------------------------------------------------------------------------------------------")

new_now = Log()
new_now.set_csv_name('test.csv')
content = new_now.load_entries_from_csv()

new_now.reset_entire_history_from_database()

e = Entry(Program("program"),Activity("mylabel"))
f = Entry(Program("programFFF22"),Activity("flippy floppy","this is my description for FF"))

new_now.add_to_entries(e)
new_now.add_to_entries(f)

new_now.store_entries_in_csv()
e.delete()
new_now.store_entries_in_csv()
e.restore()
new_now.store_entries_in_csv()
f.delete()
new_now.store_entries_in_csv()
e.delete()
new_now.set_csv_name('test_write3.csv')
new_now.store_entries_in_csv()
e.restore()
new_now.store_entries_in_csv()
new_now.store_entries_in_db()

second_log = Log()
print(new_now)
print(second_log)
print(f"New now log entries size: {len(new_now.entries)}")
print(f"Second log entries post-declaration size: {len(second_log.entries)}")

for q in second_log.entries:
    print(q)
second_log.set_csv_name("test_write3.csv")
second_log.load_entries_from_csv()
print(f"Second log entries size: {len(second_log.entries)}")
    
for l in second_log.entries:
    print(l)

print("----------------------------------------------------------------------------------------------------------")

new_now.load_entries_from_db()

print("----------------------------------------------------------------------------------------------------------")

up = User_Preferences()

up.reset_preferences()
up.store_activity("myfirst")
up.store_program("HSS")
up.store_program("BHBH")

d = up.get_active_programs()

print(up.get_active_programs())
print(up.get_inactive_programs())
print(up.get_programs())
print("+++")
#up.get_active_activities()

up.mark_program_inactive("HSS")
#up.mark_activity_inactive("myfirst")
print(up.get_active_programs())
print(up.get_inactive_programs())
print(up.get_programs())
print("+++")
up.store_program("HSS")
print(up.get_active_programs())
print(up.get_inactive_programs())
print(up.get_programs())

