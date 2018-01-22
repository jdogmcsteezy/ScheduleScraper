from BCScheduleCreator import ConvertMilitaryToStd, PrintClass, DoesClassMeet
import json

#print(type(data))



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
		if DoesClassMeet(day, meeting, 'LEC'):
				week[day].append(meeting)

for day in daysOfWeek:
	print(r'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
	week[day] = sorted(week[day], key=lambda k: k['LEC']['Start']) 
	for time in week[day]:
		#print('------------------------------------------------------')
		if DoesClassMeet(day, time, 'LEC'):
			print('DAY ',day,'  LEC: ',(time['LEC']['Start']), end='')
			if DoesClassMeet(day, time, 'LAB'):
				print('  LAB: ',(time['LAB']['Start']), end='')
			print()