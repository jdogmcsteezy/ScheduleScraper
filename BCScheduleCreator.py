from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

Subjects = ['AB - Agriculture Business, ACCT - Accounting, AET - Agricultural Engineering Tech, AGR - Agriculture, AGS - Agricultural Science, AJ - Administration of Justice, AJLE - AJ Law Enforcement, ALH - Allied Health, ANTH - Anthropology, ART - Art, ASL - American Sign Language, AUT - Automotive Technology, BCIS - Business Computer Information , BIOL - Biological Sciences, BUS - Business, CDF - Child Development &amp; Family Rel, CHEM - Chemistry, CHIN - Chinese, CLP - Career Life Planning, CMST - Communication Studies, COS - Cosmetology, CSCI - Computer Science, CSL - Counseling, DFT - Drafting, DRAM - Drama, DSPS - Disabled Student Programs/Serv, ECON - Economics, EDUC - Education, EH - Environmental Horticulture, EMS - Emergency Medical Services, ENGL - English, ENGR - Engineering, ESL - English as a Second Language, FASH - Fashion, FN - Foods &amp; Nutrition, FREN - French, FSC - Fire Science, GEOG - Geography, GEOL - Geology, GERM - German, HIM - Health Information Management, HIST - History, HLTH - Health, HON - Honors, HUM - Humanities, IDST - Interdisciplinary Studies, ITAL - Italian, JOUR - Journalism, JPN - Japanese, KIN - Kinesiology, LATN - Latin, LEAD - Language Education/Development, LIS - Library &amp; Information Science, LM - Life Management, MATH - Mathematics, MCS - Multicultural Studies, MSP - MultiMedia Studies Program, MUS - Music, NR - Natural Resources, NSG - Nursing, OLS - Occupational &amp; Life Skills, PE - Physical Education, PHIL - Philosophy, PHO - Photography, PHYS - Physics, POS - Political Science, PSC - Physical Science, PSY - Psychology, READ - Reading, RLS - Real Estate, RT - Respiratory Care, RTVF - Radio/TV/Film, SOC - Sociology, 'SPAN - Spanish, SPE - Special Education', 'WKE - Work Experience, WLD - Welding']

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

GrabClassData('Spring 2018', 'Main Campus', '')