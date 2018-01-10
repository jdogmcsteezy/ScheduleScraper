from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import string

def CleanText(string):
	string = string.replace(r'\n', '')
	string = string.replace('\'', '')
	string = string.replace(',', '')
	string = string.replace('*', '')
	string = string.replace('  ', '')
	return string.strip()

def ParseSchedule(string):
	schedule = {}
	for type in string:
		

file = open('sampleHTML.html')

htmlStr = [line for line in file]
soup = BeautifulSoup(str(htmlStr), 'lxml')
rows = soup.find('tbody').findAll('tr')
classInfo = {}
classes = {}
# for row in rows:
# 	print('----------------------------------------')
# 	for content in row.contents:
# 		print(content)


# --------This Finds Building, room, LEC/Lab, Day, Time
# for row in rows:
# 	for td in row.findAll('td', 'col-md-4'):
# 		for div in td.findAll('div'):
# 		# s = CleanText(td.find('div').text)

# 			print(div.text)
# 			print('\n')

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
	classInfo['LocationTime'] = LocationTime
	for td in row.findAll('td', 'col-md-2'):
		classInfo['Title'] = CleanText(td.text)
	for td in row.findAll('a',href=True):
		if 'http://www.butte.edu/district_info/directory' in td['href']:
			classInfo['Instructor'] = CleanText(td.text)

	print(classInfo)
	print('\n')



# for row in rows:
# 	for td in row.findAll('a',href=True):
# 		if 'http://www.butte.edu/district_info/directory' in td['href']:
# 			s = CleanText(td.text)
# 			print(s)
# 			print('\n')
		
