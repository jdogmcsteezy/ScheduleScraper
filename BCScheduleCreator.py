from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

def GrabClassData(Term, Subject, Location):
	driver = webdriver.Firefox()
	driver.get('http://searchclasses.butte.edu/')
	selection = Select(driver.find_element_by_id('InputTermId'))
	selection.select_by_visible_text(Term)
	selection = Select(driver.find_element_by_id('InputSubjectId'))
	selection.select_by_visible_text(Subject)
	selection = Select(driver.find_element_by_id('InputLocationId'))
	selection.select_by_visible_text(Location)
	driver.find_element_by_id('searchButton').click()
	tableData = driver.page_source
	driver.quit()
	soup = BeautifulSoup(tableData)
	
	print(soup.prettify())

GrabClassData('Spring 2018', 'CSCI - Computer Science', 'Main Campus')