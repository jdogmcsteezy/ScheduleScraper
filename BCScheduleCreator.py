from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

def GrabClassData(Term, Location, Subject):
	driver = webdriver.Firefox()
	driver.get('http://searchclasses.butte.edu/')
	selection = Select(driver.find_element_by_id('InputTermId'))
	selection.select_by_visible_text(Term)
	selection = Select(driver.find_element_by_id('InputLocationId'))
	selection.select_by_visible_text(Location)
	if Subject is not None:
		selection = Select(driver.find_element_by_id('InputSubjectId'))
		selection.select_by_visible_text(Subject)
	driver.find_element_by_id('searchButton').click()
	tableData = driver.page_source
	#driver.quit()
	soup = BeautifulSoup(tableData, 'lxml')
	# Create file for texting
	with open('sampleLargeHTML.html', 'w') as file:
		file.write(tableData)
	#print for testing
	print(soup.prettify())

GrabClassData('Spring 2018', 'Main Campus', None)