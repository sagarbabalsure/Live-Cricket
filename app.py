from terminaltables import SingleTable
from bs4 import BeautifulSoup
from termcolor import colored
import requests
import html5lib

r = requests.get("https://www.cricbuzz.com/cricket-match/live-scores")

soup = BeautifulSoup(r.content,'html5lib')

matches = soup.find_all('div',class_='cb-col cb-col-100 cb-lv-main')

def line():
	print("_______________________________________________________________________________________________________________________________")


for match in matches:
	link = match.find('h3',class_='cb-lv-scr-mtch-hdr inline-block').a['href']
	try:
		r2 = requests.get(f'https://www.cricbuzz.com'+link)
		if r2.status_code == 200:
			soup2 = BeautifulSoup(r2.content,'html5lib')

			title = soup2.find('div',class_='cb-nav-main cb-col-100 cb-col cb-bg-white').h1

			venue_and_date = soup2.find('div',class_='cb-nav-main cb-col-100 cb-col cb-bg-white').find('div',class_='cb-nav-subhdr cb-font-12')
			splitted_list1 = venue_and_date.text.split('Venue:')
			splitted_list2 = splitted_list1[0].split(':')
			splitted_list3 = splitted_list1[1].split('Date & Time:')

			try:
				team_score = soup2.find('div',class_='cb-col-100 cb-col cb-col-scores')

				bats_and_bow_names = list()
				batsman1 = soup2.find('div',class_='cb-col-67 cb-col').find_all('a')
				for batsman in batsman1:
					bats_and_bow_names.append(batsman.text)

				bats_score = list()
				batsman_score = soup2.find('div',class_='cb-col-67 cb-col').find_all('div',class_=['cb-col cb-col-10 ab text-right','cb-col cb-col-8 ab text-right'])
				for score in batsman_score:
					bats_score.append(score.text)
				# print(list1)

				bow_score = list()
				for bowler in soup2.find('div',class_='cb-col-67 cb-col').find_all('div',class_='cb-col cb-col-100 cb-min-itm-rw'):
					B = bowler.find_all('div',class_=['cb-col cb-col-10 text-right','cb-col cb-col-8 text-right'])
					for b in B:
						bow_score.append(b.text)


				print("				",colored(title.text,'green',attrs=['bold']))
				print("				      	   ",colored("Series: ",'cyan',attrs=['bold']),splitted_list2[1])
				print("					   ",colored("Venue: ",'cyan',attrs=['bold']),splitted_list3[0])
				print("					   ",colored("Date & Time: ",'cyan',attrs=['bold']),splitted_list3[1])
				print("				",team_score.text)

				final_list_batsman = ['Batsman','R','B','4s','6s'],[bats_and_bow_names[0],bats_score[0],bats_score[1],bats_score[2],bats_score[3]],[bats_and_bow_names[1],bats_score[4],bats_score[5],bats_score[6],bats_score[7]]
				final_list_bowler = ['Bowler','O','M','R','W'],[bats_and_bow_names[2],bow_score[0],bow_score[1],bow_score[2],bow_score[3]],[bats_and_bow_names[3],bow_score[4],bow_score[5],bow_score[6],bow_score[7]]
			
				table = SingleTable(final_list_batsman)
				print(table.table)
				table = SingleTable(final_list_bowler)
				print(table.table)
				line()

			except Exception as e:
				try:
					print("				",colored(title.text,'green',attrs=['bold']))
					print("				      	   ",colored("Series: ",'cyan',attrs=['bold']),splitted_list2[1])
					print("					   ",colored("Venue: ",'cyan',attrs=['bold']),splitted_list3[0])
					print("					   ",colored("Date & Time: ",'cyan',attrs=['bold']),splitted_list3[1])
					match_result = soup2.find('div',class_='cb-col cb-col-100 cb-min-comp')
					print(match_result.text)
					line()

				except Exception as e:
					line()

		else:
			print('Error')
	except Exception as e:
		print(e)
		line()