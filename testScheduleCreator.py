from BCScheduleCreator import ConvertMilitaryToStd, PrintClass
import json

#print(type(data))
def doesClassMeet(day, meeting, type):
	if meeting[type] is not None:
		if day in meeting[type]['Days']:
			return True
	return False


with open('testJSON.json') as file:
    data = json.loads(file.read())

daysOfWeek = ['M','T','W','Th','F']
monday = []
tuesday = []
wednesday = []
thursday = []
friday = []
week = {'M': monday, 'T': tuesday, 'W': wednesday, 'Th': thursday,'F':friday}
for meeting in data:
	PrintClass(meeting)
	for day in daysOfWeek:
		if doesClassMeet(day, meeting, 'LEC'):
				week[day].append(meeting)
		if doesClassMeet(day, meeting, 'LAB'):
				week[day].append(meeting)

for day in daysOfWeek:
	print(r'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
	week[day] = sorted(week[day], key=lambda k: k['LEC']['Start']) 
	for time in week[day]:
		#print('------------------------------------------------------')
		if doesClassMeet(day, time, 'LEC'):
			print('DAY ',day,'  LEC: ',ConvertMilitaryToStd(time['LEC']['Start']), end='')
			if doesClassMeet(day, time, 'LAB'):
				print('  LAB: ',ConvertMilitaryToStd(time['LAB']['Start']), end='')
			print()