from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options


WINDOW_SIZE = "1280,720"

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
# driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
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
		# nextbutton = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[3]/div[2]/div[4]/div/dl[2]/dd[3]/a')
		# nextbutton.click()
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

df1 = summery()
time.sleep(2)
df2 = defensive()
time.sleep(1)
df3 = offensive()

dfs = [df1, df2, df3]
dfs = [df.set_index('Team') for df in dfs]
df = dfs[0].join(dfs[1:])


df.to_csv(r'total_data.csv',index = True)
driver.close()