# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 12:32:39 2020

@author: Alex
"""


"""
Filtrage collaboratif : matrice avec users et remplie avec les ratings --> KNN, SVD, NME
Base contenu : utiliser TF-IDF, Vectorizer --> utiliser commentaire et/ou description de l'hôtel
Déduire positivité d'un commentaire selon la note 
Possibilité de créer un profil user : ce qu'il aime, critères qui l'intéressent

On prend 1 ville, on scrape tous les commentaires (ou on se limite un peu) mais seulement le
titre. Puis on clique sur le profil de chacun et on récupère ses avis et description des 
hôtels. 
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

import time
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver    
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    print("create driver chrome")
    return webdriver.Chrome(ChromeDriverManager().install())

def create_rating(rating):
    new_rating = rating[0]+","+rating[1]
    return new_rating

hotels_name = []
hotels_link = []
hotels_rate = []
hotels_location = []
hotels_id = []
hotels_description = []
hotels_list = hotels_name,hotels_link

reviews_name = []
reviews_rate = []
reviews_title = []
reviews_id = []
id_hotel = []
reviews_list = reviews_name,reviews_rate,reviews_title

page = 0
nb_page = 1
i = 0
h_id = 0
id_h = 0
c_id = 0

for i in range(nb_page):
    
    homepage = requests.get("https://www.tripadvisor.fr/Hotels-g187147-oa"+str(page)+"-Paris_Ile_de_France-Hotels.html")
    home_soup = BeautifulSoup(homepage.text, 'lxml')
    
    for a in home_soup.find_all('a',  class_='property_title prominent'):
        
        hotels_name.append(a.text.replace('\n',"").strip())
        #print(hotels_name)
        link = a['href'].replace('\n',"")
        full_link = "https://www.tripadvisor.fr" + link
        #print(full_link)
        hotels_link.append(full_link)
        
        hotel_content = requests.get(full_link)
        hotel_soup = BeautifulSoup(hotel_content.text, 'lxml')
        hotels_rate.append(hotel_soup.find('span', class_="_3cjYfwwQ").text)
        hotels_location.append(hotel_soup.find('span', class_="_3ErVArsu jke2_wbp").text)
        hotels_id.append(h_id)
        
        # Cette partie est inutile, finalement on ne prend pas la description
        #driver = get_driver()
        #driver.get(full_link)
        #sleep(5)
        
        #description_plus = driver.find_element_by_css_selector("div[class='_36B4Vw6t']")
        #description_plus.click()
        
        
        # Partie où on s'occupe des avis
        
        # Là, c'est les 5 div des commentaires
        reviews = hotel_soup.find_all('div', class_='_2wrUUKlw _3hFEdNs8')
        for review in reviews:
            # PROBLEME : ça prend toujours le 1er commentaire 5 fois 
            reviews_name.append(hotel_soup.find('a', class_="ui_header_link _1r_My98y").text)
            
            rating = hotel_soup.find('span', class_="ui_bubble_rating")
            char_to_delete = 'abcdefghijklmnopqrstuvwxyz<>/="_'
            
            for char in char_to_delete:
                rating = str(rating).replace(char,"").strip()
                
            new_rate = create_rating(rating)
                
            reviews_rate.append(new_rate)
            reviews_title.append(hotel_soup.find('a', class_="ocfR3SKN").text)
            reviews_id.append(c_id)
            id_hotel.append(id_h)
                
            c_id = c_id + 1
            print("comment nb : "+str(c_id))
        
        h_id = h_id + 1
        id_h = h_id
        print("Hotel nb : "+str(h_id))
            
    hotels_df = pd.DataFrame({'id':hotels_id,'name':hotels_name,'link':hotels_link,'rate':hotels_rate,'location':hotels_location})
    reviews_df = pd.DataFrame({'id':reviews_id,'user_name':reviews_name,'rate':reviews_rate,'title':reviews_title,'hotel_id':id_hotel})

    print(hotels_df)
    print(reviews_df)
    page = page + 30


