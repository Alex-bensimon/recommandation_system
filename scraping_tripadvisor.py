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

def get_driver():
    print("create driver chrome")
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    return webdriver.Chrome(ChromeDriverManager().install())


hotels_name = []
hotels_link = []
hotels_rate = []
hotels_location = []
hotels_id = []
hotels_description = []
hotels_list = hotels_name,hotels_link

page = 0
nb_page = 2
i = 0
h_id = 0

for i in range(nb_page):
    
    homepage = requests.get("https://www.tripadvisor.fr/Hotels-g187147-oa"+str(page)+"-Paris_Ile_de_France-Hotels.html")
    home_soup = BeautifulSoup(homepage.text, 'lxml')
    
    for a in home_soup.find_all('a',  class_='property_title prominent'):
        
        hotels_name.append(a.text.replace('\n',"").strip())
        print(hotels_name)
        link = a['href'].replace('\n',"")
        full_link = "https://www.tripadvisor.fr" + link
        print(full_link)
        hotels_link.append(full_link)
        
        hotel_content = requests.get(full_link)
        hotel_soup = BeautifulSoup(hotel_content.text, 'lxml')
        hotels_rate.append(hotel_soup.find('span', class_="_3cjYfwwQ").text)
        hotels_location.append(hotel_soup.find('span', class_="_3ErVArsu jke2_wbp").text)
        hotels_id.append(h_id)
        
        driver = get_driver()
        driver.get(full_link)
        sleep(5)
        
        description_plus = driver.find_element_by_css_selector("span[class='ui_icon caret-down ']")
        description_plus.click()
        

        
    
    hotels_df = pd.DataFrame({'id':h_id,'name':hotels_name,'link':hotels_link,'rate':hotels_rate,'location':hotels_location})
    print(hotels_df)
    page = page + 30

