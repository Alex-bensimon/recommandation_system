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
from random import randint
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
    
    if home_soup.find_all('a',  class_='property_title prominent')!=None:
        for a in home_soup.find_all('a',  class_='property_title prominent'):
            # On parcourt chaque hotel et on récupère le lien
            hotels_name.append(a.text.replace('\n',"").strip())
            #print(hotels_name)
            link = a['href'].replace('\n',"")
            full_link = "https://www.tripadvisor.fr" + link
            #print(full_link)
            hotels_link.append(full_link)
            
            hotel_content = requests.get(full_link)
            hotel_soup = BeautifulSoup(hotel_content.text, 'lxml')
            
            # On prend ses caractéristiques
            if hotel_soup.find('span', class_="_3cjYfwwQ") != None:
                hotels_rate.append(hotel_soup.find('span', class_="_3cjYfwwQ").text)
            else:
                hotels_rate.append(None)
                
            if hotel_soup.find('span', class_="_3ErVArsu jke2_wbp") != None:
                hotels_location.append(hotel_soup.find('span', class_="_3cjYfwwQ").text)
            else:
                hotels_location.append(None)
                
            hotels_location.append(hotel_soup.find('span', class_="_3ErVArsu jke2_wbp").text)
            
            hotels_id.append(h_id)
           
            
            # Partie où on s'occupe des avis
            
            # Là, c'est les 5 div des commentaires
            if hotel_soup.find_all('div', class_='_2wrUUKlw _3hFEdNs8') != None:
                reviews = hotel_soup.find_all('div', class_='_2wrUUKlw _3hFEdNs8')
            else:
                print("Comments fail")
                
            for review in reviews:
                # On prend les caractéristiques de l'avis
                if review.find('a', class_="ui_header_link _1r_My98y") != None:
                    reviews_name.append(review.find('a', class_="ui_header_link _1r_My98y").text)
                else: 
                    reviews_name.append(None)
                
                if review.find('span', class_="ui_bubble_rating") != None:
                    rating = review.find('span', class_="ui_bubble_rating")
                else: 
                    print("No rating")
                    
                char_to_delete = 'abcdefghijklmnopqrstuvwxyz<>/="_'
                
                for char in char_to_delete:
                    rating = str(rating).replace(char,"").strip()
                    
                new_rate = create_rating(rating)                
                reviews_rate.append(new_rate)
                
                if review.find('a', class_="ocfR3SKN") != None:
                    reviews_title.append(review.find('a', class_="ocfR3SKN").text)
                else:
                    reviews_title.append(None)
                    
                reviews_id.append(c_id)
                id_hotel.append(id_h)
                    
                c_id = c_id + 1
                print("comment nb : "+str(c_id))
                
                # On teste pour savoir si l'user a mis + d'un commentaire
                if review.find('span', class_='_1fk70GUn') != None:
                    nb_comment = review.find('span', class_='_1fk70GUn').text.strip()
                else:
                    nb_comment = "10000000"
                if len(nb_comment) <= 4:
                    if int(nb_comment) > 1:
                        
                        # Si oui, on récupère le lien de son profil
                        if review.find('a', class_='ui_header_link _1r_My98y') != None:
                            user = review.find('a', class_='ui_header_link _1r_My98y')                    
                            user_link = user['href']
                            full_user_link = "https://www.tripadvisor.fr" + user_link
                            user_content = requests.get(full_user_link)
                            user_soup = BeautifulSoup(user_content.text, 'lxml')
    
                        
                            # On parcourt tous les commentaires laissés par l'user
                            if user_soup.find_all('div', class_='nMewIgXP ui_card section') != None:
                                user_reviews = user_soup.find_all('div', class_='nMewIgXP ui_card section')      
                                for user_review in user_reviews:
                                    if user_review.find('div', class_='_2X5tM2jP _2RdXRsdL _1gafur1D') != None:
                                        div = user_review.find('div', class_='_2X5tM2jP _2RdXRsdL _1gafur1D')
                                        if div.find('a') != None:
                                            href_user = div.find('a')
                                            href = href_user['href']
                                                                        
                                            # On chercher à savoir si le commentaire est sur un hôtel ou restau
                                            test = href[1:6]
                                            
                                            if test == "Hotel":
                                                
                                                # On récupère les caractéristiques du commentaire
                                                reviews_name.append(user_review.find('a', class_="ui_link _1r_My98y").text)
                                                rating = user_review.find('span', class_="ui_bubble_rating")
                                                char_to_delete = 'abcdefghijklmnopqrstuvwxyz<>/="_'
                                                
                                                for char in char_to_delete:
                                                    rating = str(rating).replace(char,"").strip()
                                                    
                                                new_rate = create_rating(rating)
                                                reviews_rate.append(new_rate)
                                                if user_review.find('div', class_="_3IEJ3tAK _2K4zZcBv") != None:
                                                    reviews_title.append(user_review.find('div', class_="_3IEJ3tAK _2K4zZcBv").text)
                                                else:
                                                    reviews_title.append(None)
                                                reviews_id.append(c_id)
                                                
                                                new_hotel_link = "https://www.tripadvisor.fr" + href
                                                new_hotel = requests.get(new_hotel_link)
                                                new_hotel_soup = BeautifulSoup(new_hotel.text, 'lxml')
                                                
                                                hotels_name.append(new_hotel_soup.find('h1', class_="_1mTlpMC3").text.replace('\n',"").strip())
                                                hotels_link.append(new_hotel_link)
                                                hotels_rate.append(new_hotel_soup.find('span', class_="_3cjYfwwQ").text)
                                                hotels_location.append(new_hotel_soup.find('span', class_="_3ErVArsu jke2_wbp").text)
                                                new_hotel_id = randint(10000, 100000)
                                                hotels_id.append(new_hotel_id)
                                                id_hotel.append(new_hotel_id)
                                                
                                                print("comment nb : "+str(c_id))
                                                c_id = c_id + 1
                                        else:
                                            print("Div None")
                                    else:
                                        print("Comment")
                            else: 
                                print("No user comments")
                        else:
                            print("No profile")
                        
            h_id = h_id + 1
            id_h = h_id
            print("Hotel nb : "+str(h_id))
        
    else:
        print("Fail")
            
    hotels_df = pd.DataFrame({'id':hotels_id,'name':hotels_name,'link':hotels_link,'rate':hotels_rate,'location':hotels_location})
    reviews_df = pd.DataFrame({'id':reviews_id,'user_name':reviews_name,'rate':reviews_rate,'title':reviews_title,'hotel_id':id_hotel})

    print(hotels_df)
    print(reviews_df)
    page = page + 30


