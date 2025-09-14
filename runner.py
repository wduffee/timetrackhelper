from classes import *
from user_preferences_class import *

print("----------------------------------------------------------------------------------------------------------")


new_now = Log()
new_now.set_csv_name('test.csv')
content = new_now.load_entries_from_csv()
print(content)

for item in new_now.get_program_entries("HSS"):
    print(item.program.name)

new_now.set_csv_name('test_write.csv')

new_now.store_entries_in_csv()
new_now.store_entries_in_csv()

new_now.set_csv_name('test_write2.csv')
new_now.store_entries_in_csv()
new_now.store_entries_in_csv(True)

e = Entry(Program("program"),Activity("mylabel"))
f = Entry(Program("program"),Activity("flippyfloppy"))
new_now.add_to_entries(e)
new_now.add_to_entries(f)

new_now.store_entries_in_csv(True)
e.delete()
new_now.store_entries_in_csv()
e.restore()
new_now.store_entries_in_csv()
f.delete()
new_now.store_entries_in_csv(True)
e.delete()
new_now.set_csv_name('test_write3.csv')
new_now.store_entries_in_csv(True)
e.restore()
new_now.store_entries_in_csv()


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

