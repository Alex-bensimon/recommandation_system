# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 12:51:18 2020

@author: Alex
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from random import randint
import time
from time import sleep

def hotels_tab_creation():
    hotels_name = []
    hotels_link = []
    hotels_rate = []
    hotels_location = []
    hotels_id = []
    hotels_description = []
    
    return hotels_name,hotels_link,hotels_rate,hotels_location,hotels_id,hotels_description

def reviews_tab_creation(): 
    reviews_name = []
    reviews_rate = []
    reviews_title = []
    user_id = []
    id_hotel = []
    
    return reviews_name,reviews_rate,reviews_title,user_id,id_hotel


def create_rating(rating):
    new_rating = rating[0]+","+rating[1]
    return new_rating

def delete_chars(rating):
    char_to_delete = 'abcdefghijklmnopqrstuvwxyz<>/="_'
    for char in char_to_delete:
        rating = str(rating).replace(char,"").strip()
        
    return rating
        

def homepage_request(page,i=0):
    homepage = requests.get("https://www.tripadvisor.fr/Hotels-g187147-oa"+str(page)+"-Paris_Ile_de_France-Hotels.html")
    home_soup = BeautifulSoup(homepage.text, 'lxml')
    
    return home_soup


def totor_function():
    h_id = 100
    return h_id

def totor_function2():
    c_id = 100
    return c_id


def hotel_scraping(a):
    
    hotels_name,hotels_link,hotels_rate,hotels_location,hotels_id,hotels_description = hotels_tab_creation()
    h_id = totor_function()
    
    # On parcourt chaque hotel et on récupère le lien
    hotels_name.append(a.text.replace('\n',"").strip())
    link = a['href'].replace('\n',"")
    full_link = "https://www.tripadvisor.fr" + link
    hotels_link.append(full_link)
    
    hotel_content = requests.get(full_link)
    hotel_soup = BeautifulSoup(hotel_content.text, 'lxml')
    
    # On prend ses caractéristiques
    if hotel_soup.find('span', class_="_3cjYfwwQ") != None:
        hotels_rate.append(hotel_soup.find('span', class_="_3cjYfwwQ").text)
    else:
        hotels_rate.append(None)
        
    if hotel_soup.find('span', class_="_3ErVArsu jke2_wbp") != None:
        hotels_location.append(hotel_soup.find('span', class_="_3ErVArsu jke2_wbp").text)
    else:
        hotels_location.append(None)
                    
    hotels_id.append(h_id)
    
     # Là, c'est les 5 div des commentaires
    if hotel_soup.find_all('div', class_='_2wrUUKlw _3hFEdNs8') != None:
        reviews = hotel_soup.find_all('div', class_='_2wrUUKlw _3hFEdNs8')
    else:
        print("Comments fail")
    
    return reviews
            

def reviews_scraping(review):
    
    reviews_name,reviews_rate,reviews_title,user_id,id_hotel = reviews_tab_creation()
    c_id = totor_function2()
    
    # On prend les caractéristiques de l'avis
    if review.find('a', class_="ui_header_link _1r_My98y") != None:
        reviews_name.append(review.find('a', class_="ui_header_link _1r_My98y").text)
    else: 
        reviews_name.append(None)
    
    if review.find('span', class_="ui_bubble_rating") != None:
        rating = review.find('span', class_="ui_bubble_rating")
    else: 
        print("No rating")
        
    rating = delete_chars(rating)
        
    new_rate = create_rating(rating)                
    reviews_rate.append(new_rate)
    
    if review.find('a', class_="ocfR3SKN") != None:
        reviews_title.append(review.find('a', class_="ocfR3SKN").text)
    else:
        reviews_title.append(None)
        
    user_id.append(c_id)
    id_hotel.append("A CHANGER")
        

def test_nb_user_reviews(review):
    if review.find('span', class_='_1fk70GUn') != None:
        nb_comment = review.find('span', class_='_1fk70GUn').text.strip()
    else:
        nb_comment = "10000000"
    if len(nb_comment) <= 4:
        if int(nb_comment) > 1:
            result = True
            print("True")
        else:
            result = False
            print("False")
            
    return result


def get_user_link(review):
    if review.find('a', class_='ui_header_link _1r_My98y') != None:
        user = review.find('a', class_='ui_header_link _1r_My98y')                    
        user_link = user['href']
        full_user_link = "https://www.tripadvisor.fr" + user_link
        user_content = requests.get(full_user_link)
        user_soup = BeautifulSoup(user_content.text, 'lxml')
        
        # On parcourt tous les commentaires laissés par l'user
        if user_soup.find_all('div', class_='nMewIgXP ui_card section') != None:
            user_reviews = user_soup.find_all('div', class_='nMewIgXP ui_card section') 
            
    return user_reviews


def test_hotel_or_restau(user_review):
    if user_review.find('div', class_='_2X5tM2jP _2RdXRsdL _1gafur1D') != None:
        div = user_review.find('div', class_='_2X5tM2jP _2RdXRsdL _1gafur1D')
        if div.find('a') != None:
            href_user = div.find('a')
            href = href_user['href']
                                        
            # On chercher à savoir si le commentaire est sur un hôtel ou restau
            test = href[1:6]
            
    return test

def main(nb_page):
    for i in range(nb_page):
        home_soup = homepage_request(1,i=0)
                
        if home_soup.find_all('a',  class_='property_title prominent') != None:
            for a in home_soup.find_all('a',  class_='property_title prominent'):
                reviews = hotel_scraping(a)
                for review in reviews:
                    reviews_scraping(review)
                    result = test_nb_user_reviews(review)
                    
                    if result == True: 
                        user_reviews = get_user_link(review)
                        for user_review in user_reviews:
                            test = test_hotel_or_restau(user_review)
                            if test == "Hotel":
                                reviews_scraping(user_review)
