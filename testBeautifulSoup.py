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
            #print(match,time)
            meeting[time] = match.group().strip()
        # Add the dic to a schedule
        schedule[type_] = meeting
    #return schedule dict.
    return schedule
    
    
with open('sampleHTML.html') as file:
    soup = BeautifulSoup(file, 'lxml')
rows = soup.find('tbody').findAll('tr')
classes = []
for row in rows:
    classInfo = {}
    LocationTime = []
    for td in row.findAll('td', 'col-md-4'):
        for div in td.findAll('div', limit=2):
            text = div.text
            if 'MC' in text:
                LocationTime.append(CleanText(text))
    if not LocationTime:
        continue 
    schedule = ParseSchedule(LocationTime)
    if not schedule:
        continue
    classInfo['Schedule'] = schedule
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
    classes.append(classInfo)
    print(classInfo)
    print('\n')

with open('subjectsHTML.txt') as f:
    text = f.read()
    pattern = re.compile(r'>.+<')
    matches = pattern.finditer(text)
    
    with open ('subjects.txt','w') as w:
        for match in matches:
            w.write(match.group()[1:-1])
            w.write('\', \'')