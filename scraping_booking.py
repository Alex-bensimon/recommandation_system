# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 12:32:39 2020

@author: Alex
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

hotels_name = []
hotels_link = []
hotels_rate = []
hotels_location = []
hotels_list = hotels_name,hotels_link

page = 0
nb_page = 2
i = 0

for i in range(nb_page):
    
    homepage = requests.get("https://www.booking.com/searchresults.fr.html?aid=397594&label=gog235jc-1DCAEoggI46AdIDVgDaE2IAQGYAQ24ARfIAQzYAQPoAQH4AQKIAgGoAgO4Aq3znf4FwAIB0gIkZGM2MmJhYWYtNGNlZS00ZjdkLTkzNmMtNTJmOGJlMzJkZDAy2AIE4AIB&sid=0cca7583b65086c7fef150d28e6879d9&tmpl=searchresults&city=-1456928&class_interval=1&dest_id=-1456928&dest_type=city&dr_ps=IDR&from_idr=1&group_adults=2&group_children=0&ilp=1&label_click=undef&no_rooms=1&raw_dest_type=city&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&srpvid=5609432bef8d0142&ssb=empty&top_ufis=1&rows=25&offset="+str(page))
    home_soup = BeautifulSoup(homepage.text, 'lxml')
    
    for a in home_soup.find_all('a',  class_='js-sr-hotel-link hotel_name_link url'):
        
        hotels_name.append(a.find('span', class_="sr-hotel__name").text.replace('\n',""))
        link = a['href'].replace('\n',"")
        full_link = "https://www.booking.com" + link
        hotels_link.append(full_link)
        
        hotel_content = requests.get(full_link)
        hotel_soup = BeautifulSoup(hotel_content.text, 'lxml')
        hotels_rate.append(hotel_soup.find('div', class_="bui-review-score__badge").text)
        hotels_location.append(hotel_soup.find('span', class_="hp_address_subtitle js-hp_address_subtitle jq_tooltip").text.strip())
        
    
    hotels_df = pd.DataFrame({'name':hotels_name,'link':hotels_link,'rate':hotels_rate,'location':hotels_location})
    print(hotels_df)
    page = page + 25

