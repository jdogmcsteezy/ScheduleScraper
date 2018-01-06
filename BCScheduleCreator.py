from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()
driver.get('http://searchclasses.butte.edu/')
selection = Select(driver.find_element_by_id('InputTermId'))
selection.select_by_visible_text('Spring 2018')
selection = Select(driver.find_element_by_id('InputSubjectId'))
selection.select_by_visible_text('CSCI - Computer Science')
selection = Select(driver.find_element_by_id('InputLocationId'))
selection.select_by_visible_text('Main Campus')
driver.find_element_by_id('searchButton').click()
print(driver.page_source)
driver.quit()
