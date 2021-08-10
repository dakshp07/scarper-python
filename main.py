# Author: Daksh Paleria
# The default path for saving csv is the root folder where you are running this script.
# The default name of csv is result.csv
# If you want to overwrite the default path to scan path to save csv, csv name then run the script in following manner:
# python3 main_csv.py /your_path_to_save filename.csv
# Eg: python3 main_csv.py /home/daksh/Desktop/downloads /home/daksh/Desktop data.csv
# This will prompt the script to scan the folder in the given path, save the csv in next path, name the csv accordingly.
# imports
import requests
import bs4
from bs4 import BeautifulSoup
import os
import sys
import pandas as pd
from colorama import Fore

n=len(sys.argv)
if(n==1):
    directory_csv=os.path.dirname(os.path.abspath(__file__))
    file_csv_name="result.csv"

if (n==2):
    directory_csv=sys.argv[1]
    file_csv_name="result.csv"
if (n==3):
    directory_csv=sys.argv[1]
    file_csv_name=sys.argv[2]

# array declaration
job_apply_links=[]
job_titles=[]
job_position=[]
job_locations=[]

url="https://in.indeed.com/jobs?q=intern&l=India"
page=requests.get(url)
soup=BeautifulSoup(page.text, "html.parser")
job_soup=soup.find(id="resultsCol")
job_card_parent=job_soup.find(id="mosaic-zone-jobcards")
job_cards=job_card_parent.find_all("div", id="mosaic-provider-jobcards")

for job_card in job_cards:
    job_main_card=job_card.find_all('a')
    for links in job_main_card:
        job_apply_link="https://in.indeed.com"+links['href']
        if(job_apply_link[-6:]=="&vjs=3"):
            job_apply_links.append(job_apply_link)
        card_one=links.find_all(class_="jobCard_mainContent")
        for card_ones in card_one:
            card_two=card_ones.find_all('tbody')
            #print(card_two)
            for card_twos in card_two:
                card_three=card_twos.find_all('tr')
                for card_threes in card_three:
                    card_final=card_threes.find('td', class_="resultContent")
                    job_title_card=card_final.find('div',class_='heading6 company_location tapItem-gutter')
                    job_position_card=card_final.find('div',class_="heading4 color-text-primary singleLineTitle tapItem-gutter")
                    job_position_h2=job_position_card.find_all('h2')
                    for job_position_h2s in job_position_h2:
                        job_position.append(job_position_h2s.text.strip('new'))
                    job_title=job_title_card.find('span', class_="companyName")
                    job_titles.append(job_title.text)
                    job_location=job_title_card.find('div', class_="companyLocation")
                    job_locations.append(job_location.text)


dict={"Company Name":job_titles, "Position": job_position, "Location": job_locations, "Link To Apply": job_apply_links}
dataframe=pd.DataFrame(dict)
dataframe.to_csv(directory_csv+"/"+file_csv_name, index=False)
print(Fore.WHITE+"Successfully Dumped at "+Fore.GREEN+directory_csv+"/"+file_csv_name)