from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import os


WINDOW_SIZE = "1280,720"

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.whoscored.com/Statistics")
driver.execute_script("window.scrollTo(0, 410)")



def edit(x):
	x = ''.join([i for i in x if not i.isdigit()])
	return x[1:]








def summery():
	global driver
	l2 = []
	summary_colums = ["Team","Tournament","Goals","Shots pg","Discipline","Possession%","Pass%","AerialsWon","Rating_S"]
	for i in range(5):
		time.sleep(2)
		summary_page = driver.page_source
		soup = BeautifulSoup(summary_page,'lxml')
		table = soup.find_all('tbody',id="top-team-stats-summary-content")
		teams = table[0].find_all('tr')
		
		for team in teams:
			l1 = []
			items = team.find_all('td')
			for item in items:
				l1.append(item.text)
			l2.append(l1)

		button = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div[3]/div[2]/div[4]/div/dl[2]/dd[3]/a")
		driver.execute_script("arguments[0].click();", button)

	df  = pd.DataFrame(l2,columns = summary_colums )
	df['Team'] = df['Team'].apply(edit)
	df.sort_values('Team',ascending=True, inplace=True)
	df.drop('Discipline',axis='columns',inplace=True)
	return df


def defensive():
	global driver
	l2 = []
	defense_colums = ["Team","Tournament","Shots pg","Tackles pg","Interceptions pg","Fouls pg","Offsides pg","Rating_d"]
	d_button = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div[3]/div[1]/ul/li[2]/a")
	driver.execute_script("arguments[0].click();", d_button)
	for i in range(5 ):
		time.sleep(1)
		defense_page = driver.page_source
		soup = BeautifulSoup(defense_page,'lxml')
		table = soup.find("div", {"id": "statistics-team-table-defensive"})
		teams = table.find_all('tr')
		for team in teams[1:]:
			l1 = []
			items = team.find_all('td')
			for item in items:
				l1.append(item.text)
			l2.append(l1)

		button = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div[3]/div[4]/div[4]/div/dl[2]/dd[3]/a")
		driver.execute_script("arguments[0].click();", button)
	df  = pd.DataFrame(l2,columns = defense_colums )
	df['Team'] = df['Team'].apply(edit)
	df.sort_values('Team',ascending=True, inplace=True)
	df.drop('Rating_d',axis='columns',inplace=True)
	df.drop('Shots pg',axis='columns',inplace=True)
	# df.drop('Team',axis='columns',inplace=True)
	df.drop('Tournament',axis='columns',inplace=True)
	return df

def offensive():
	global driver
	l2 = []
	defense_colums = ["Team","Tournament","Shots pg","Shots OT pg","Dribbles pg","Fouled pg","Rating_O"]
	d_button = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div[3]/div[1]/ul/li[3]/a")
	driver.execute_script("arguments[0].click();", d_button)
	for i in range(5):
		time.sleep(1)
		defense_page = driver.page_source
		soup = BeautifulSoup(defense_page,'lxml')
		table = soup.find("div", {"id": "statistics-team-table-offensive"})
		teams = table.find_all('tr')
		for team in teams[1:]:
			l1 = []
			items = team.find_all('td')
			for item in items:
				l1.append(item.text)
			l2.append(l1)

		button = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div[3]/div[3]/div[4]/div/dl[2]/dd[3]/a")
		driver.execute_script("arguments[0].click();", button)
	df  = pd.DataFrame(l2,columns = defense_colums )
	df['Team'] = df['Team'].apply(edit)
	df.sort_values('Team',ascending=True, inplace=True)
	df.drop('Rating_O',axis='columns',inplace=True)
	df.drop('Shots pg',axis='columns',inplace=True)
	df.drop('Tournament',axis='columns',inplace=True)
	return df

def matches():
	url = 'https://www.whoscored.com/LiveScores'
	driver.get(url)
	Tournaments = ["Spain - LaLiga","Italy - Serie A","Germany - 1. Bundesliga","England - Premier League","France - Ligue 1"]



	d_button = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div[1]/div[3]/dl[1]/dd[1]/div/a[1]/span")
	driver.execute_script("arguments[0].click();", d_button)

	time.sleep(1)

	legues = driver.find_elements_by_xpath('//*[@class="divtable-row group ls-1 stream-is-available"]')

	def res_split(res):
		for i in range(len(res)):

			if res[i] == ':':
				home = int(res[0:i-1])
				away = int(res[i+1:])
				break
		return home, away




	data_columns = ['Home','Away','home goals','away goals']
	data = []
	for item in legues:

		ID = item.get_attribute("id")
		team = item.find_element_by_class_name('tournament-link').text
		if team in Tournaments:
			# print('////',team,'////')
			matches = driver.find_elements_by_xpath('//*[@data-group-id="{}"]'.format(int(ID[1:])))
			for matche in matches:
				home = matche.find_element_by_class_name('home')
				away = matche.find_element_by_class_name('away')
				result = matche.find_element_by_class_name('result')
				home_r, away_r = res_split(result.text)
				data.append([home.text,away.text,home_r,away_r])
				# print(home.text , '/////' , away.text)
				# print(result.text)

	df = pd.DataFrame(data,columns = data_columns)
	return df







df1 = summery()
time.sleep(2)
df2 = defensive()
time.sleep(1)
df3 = offensive()

dfs = [df1, df2, df3]
dfs = [df.set_index('Team') for df in dfs]
df = dfs[0].join(dfs[1:])
stop = False

dfm = matches()

date = datetime.date(datetime.now())
yesterday = date - timedelta(1)
yesterday = str(yesterday)
date = str(date)
#os.mkdir(yesterday)
try:
	os.mkdir("AI_data")
except :
	FileExistsError


try:
	os.mkdir('AI_data/{}'.format(yesterday))
except:
	FileExistsError

dfm.to_csv('AI_data/{}/matches.csv'.format(yesterday),index = False)


try:
	os.mkdir('AI_data/{}'.format(date))
except:
	FileExistsError
	stop = True

if not stop:
	df.to_csv('AI_data/{}/stats.csv'.format(date),index = True)
