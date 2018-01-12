import os
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from contextlib import contextmanager
from bs4 import BeautifulSoup
import re
import sys

Subjects_dir = 'Subjects_Schedules'
Subjects = ['AB - Agriculture Business', 'ACCT - Accounting', 'AET - Agricultural Engineering Tech', 'AGR - Agriculture', 'AGS - Agricultural Science', 'AJ - Administration of Justice', 'AJLE - AJ Law Enforcement', 'ALH - Allied Health', 'ANTH - Anthropology', 'ART - Art', 'ASL - American Sign Language', 'AUT - Automotive Technology', 'BCIS - Business Computer Information', 'BIOL - Biological Sciences', 'BUS - Business', 'CDF - Child Development & Family Rel', 'CHEM - Chemistry', 'CHIN - Chinese', 'CLP - Career Life Planning', 'CMST - Communication Studies', 'COS - Cosmetology', 'CSCI - Computer Science', 'CSL - Counseling', 'DFT - Drafting', 'DRAM - Drama', 'DSPS - Disabled Student Programs/Serv', 'ECON - Economics', 'EDUC - Education', 'EH - Environmental Horticulture', 'EMS - Emergency Medical Services', 'ENGL - English', 'ENGR - Engineering', 'ESL - English as a Second Language', 'FASH - Fashion', 'FN - Foods & Nutrition', 'FREN - French', 'FSC - Fire Science', 'GEOG - Geography', 'GEOL - Geology', 'GERM - German', 'HIM - Health Information Management', 'HIST - History', 'HLTH - Health', 'HON - Honors', 'HUM - Humanities', 'IDST - Interdisciplinary Studies', 'ITAL - Italian', 'JOUR - Journalism', 'JPN - Japanese', 'KIN - Kinesiology', 'LATN - Latin', 'LEAD - Language Education/Development', 'LIS - Library & Information Science', 'LM - Life Management', 'MATH - Mathematics', 'MCS - Multicultural Studies', 'MSP - MultiMedia Studies Program', 'MUS - Music', 'NR - Natural Resources', 'NSG - Nursing', 'OLS - Occupational & Life Skills', 'PE - Physical Education', 'PHIL - Philosophy', 'PHO - Photography', 'PHYS - Physics', 'POS - Political Science', 'PSC - Physical Science', 'PSY - Psychology', 'READ - Reading', 'RLS - Real Estate', 'RT - Respiratory Care', 'RTVF - Radio/TV/Film', 'SOC - Sociology', 'SPAN - Spanish', 'SPE - Special Education', 'WKE - Work Experience', 'WLD - Welding']

@contextmanager
def Web_Driver():
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)
    yield driver
    driver.quit()

def GrabClassData(Driver, Term, Location, Subject):
    Driver.get('http://searchclasses.butte.edu/')
    selection = Select(Driver.find_element_by_id('InputTermId'))
    selection.select_by_visible_text(Term)
    selection = Select(Driver.find_element_by_id('InputLocationId'))
    selection.select_by_visible_text(Location)
    if Subject is not None:
        selection = Select(Driver.find_element_by_id('InputSubjectId'))
        selection.select_by_visible_text(Subject)
    Driver.find_element_by_id('searchButton').click()
    WebDriverWait(Driver, 20).until(EC.presence_of_element_located((By.ID, 'resultsBoiler')))
    tableData = Driver.page_source
    return tableData

def SaveDataToHTML(Subject, Data):
    # Grab the acronymn for the subject
    pattern = re.compile(r'[A-Z]+\b')
    fileName = pattern.search(Subject).group()
    # Create file name
    filePath = os.path.join(Subjects_dir, fileName + '_Schedule.html')
    # Create directory if it does not exist
    if not os.path.exists(Subjects_dir):
        os.makedirs(Subjects_dir)
    with open(filePath, 'w') as file:
        file.write(Data)

def SaveDataToJSON():
    pass

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
def ParseHTMLtoJSON(data, classes, building):
    soup = BeautifulSoup(data, 'lxml')
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
        #print(classInfo)
        #print('\n')
    return classes

# Just checks to see if the depatment can be found.
# Data should be an HTML string.
# Buillding should be a string of department. ex: 'MC'
def IsDepartmentInBuilding(data, building):
    inBuilding = False
    soup = BeautifulSoup(data, 'lxml')
    tbody = soup.find('tbody')
    if not tbody:
        return False
    rows = tbody.findAll('tr')
    for row in rows:
        for td in row.findAll('td', 'col-md-4'):
            for div in td.findAll('div', limit=2):
                text = div.text
                if building in text:
                    inBuilding = True
    return inBuilding

# Goes to webpage and fills out forms for all subjects
# then checks whether the subject has any classes in the 'building' paramater.
# Saves every relevant subject to a txt file named subjectsIn_building.txt.
def CompileClassesInBuilding(building):
    fileName = 'subjectsIn_' + building + '.txt'
    with open(fileName, 'w') as file:
        with Web_Driver() as driver:
            for subject in Subjects:
                data = GrabClassData(driver,'Spring 2018', 'Main Campus', subject)
                if IsDepartmentInBuilding(data, building):
                    file.write(subject + '\n')


# classes1 = []
# ParseHTMLtoJSON('Subjects_Schedules/ENGL_Schedule.html', classes1)
# print(classes1)

with Web_Driver() as driver:
       data = GrabClassData(driver,'Spring 2018', 'Main Campus', 'CSCI - Computer Science')
       classes = []
       ParseHTMLtoJSON(data, classes, 'MC')
       print(classes)