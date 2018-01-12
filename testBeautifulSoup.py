from bs4 import BeautifulSoup
import re

def CleanText(string):
    string = string.replace(r'\n', '')
    string = string.replace('\'', '')
    string = string.replace(',', '')
    string = string.replace('*', '')
    string = string.replace('  ', '')
    return string.strip()

def ParseSchedule(classes):
    schedule = {}
    schedule['LEC'] = None
    schedule['LAB'] = None
    # Iterate through each type of class LEC or LAB
    for classType in classes:
        # To store Building, Days, Room, and start/stop time.
        meeting = {}
        # Find if it is LEC or LAB
        pattern = re.compile(r'(LEC|LAB)')
        match = pattern.search(classType)
        # If LEC or LAB is not found then skip over class because it does not concern project.
        if match is None:
            continue
        type_ = match.group()
        # Find which building
        pattern = re.compile(r'^\w{2,5}')
        match = pattern.search(classType)
        meeting['Building'] = match.group()
        # Find which room
        pattern = re.compile(r'\s\d{3}\s')
        match = pattern.search(classType)
        meeting['Room'] = match.group().strip()
        # Find which days
        pattern = re.compile(r'\s[MTWHhF]{1,6}\s')
        match = pattern.search(classType)
        # Check if the class even has official meeting times
        if match is not None:
            meeting['Days'] = match.group().strip()
        else:
            meeting['Days'] = None
        # Find start and stop times
        pattern = re.compile(r'\s\d{1,2}:\d{2}\s(AM|PM)')
        # Save those time to a list
        matches = [match for match in pattern.finditer(classType)]
        times = ['Start','End']
        for match,time in zip(matches, times):
            meeting[time] = match.group().strip()
        # Add the dic to a schedule
        schedule[type_] = meeting
    # Return schedule dict.
    return schedule

# Takes the files saved by GrabClassData and parses them into a dict.
# At this point this function needs a building specified based on how it parses
# the <div> that contains class info. A later improvment will be using regex to be 
# able to compile classes from any building into one dict.
def ParseHTMLtoJSON(file, classes, building):
    with open(file) as file:
        soup = BeautifulSoup(file, 'lxml')
    rows = soup.find('tbody').findAll('tr')
    for row in rows:
        classInfo = {}
        LocationTime = []
        for td in row.findAll('td', 'col-md-4'):
            for div in td.findAll('div', limit=2):
                text = div.text
                if building in text:
                    LocationTime.append(CleanText(text))
        if not LocationTime:
            continue 
        # Parse the div that holds LEC, LAB, Start, End, Days, Building, Room.
        schedule = ParseSchedule(LocationTime)
        # Merge the returned scheule
        classInfo = {**classInfo, **schedule}
        td = row.find('td', 'col-md-2')
        pattern = re.compile(r'[A-Z]\w{1,3}-\d+')
        department_num = pattern.search(td.text).group()
        pattern = re.compile(r'[A-Z]\d{4}\s.+')
        name = pattern.search(td.text).group()
        name = CleanText(name)[6:]
        classInfo['Title'] = department_num + ' ' + name
        for td in row.findAll('a',href=True):
            if 'http://www.butte.edu/district_info/directory' in td['href']:
                classInfo['Instructor'] = CleanText(td.text)
            else:
                classInfo['Instructor'] = None
        classes.append(classInfo)
        print(classInfo)
        print('\n')
    return classes

def IsDepartmentInBuilding(file, building):
    inBuilding = False
    with open(file) as file:
        soup = BeautifulSoup(file, 'lxml')
    tbody = soup.find('tbody')
    if not tbody:
        return False
    rows =tbody.findAll('tr')
    for row in rows:
        for td in row.findAll('td', 'col-md-4'):
            for div in td.findAll('div', limit=2):
                text = div.text
                if building in text:
                    inBuilding = True
    return inBuilding

def CompileClassesInBuilding(building):


# classes1 = []
# ParseHTMLtoJSON('Subjects_Schedules/ENGL_Schedule.html', classes1)
# print(classes1)

print(isDepartmentInBuilding('Subjects_Schedules/WLD_Schedule.html', 'MC'))
