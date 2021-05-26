import csv
from datetime import datetime

now = datetime.now()
timestamp = datetime.timestamp(now)
dt_object: datetime = datetime.fromtimestamp(timestamp)
timestr = dt_object.strftime('%Y-%m-%d %H:%M:%S')
print(timestr)

keys = ['Timestamp', 'Patient name', 'Therapist name', 'ID number']
with open('treatments.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()  # add column names in the CSV file
    writer.writerow({'Timestamp': timestr, 'Patient name': 'Aaa Bbb', 'Therapist name': 'Abc Def', 'ID number': '123456789'})
    writer.writerow({'Timestamp': timestr, 'Patient name': 'Aaa Bbb', 'Therapist name': 'Abc Def', 'ID number': '012345678'})


############# ID search ##########
# myid='012345678'
#
# file = csv.DictReader(open("treatments.csv"))
# for row in file:
#     id = (row['ID number'])
#     if myid ==id:
#         print('good')
#     else:
#         print('bad')

################################




