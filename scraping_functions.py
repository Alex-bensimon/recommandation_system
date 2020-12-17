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
import re

def hotels_tab_creation():
    hotels_name = []            #0         
    hotels_link = []            #1
    hotels_rate = []            #2
    hotels_location = []        #3
    hotels_id = []              #4
#    hotels_description = []     #5
    
    hotels_attributs = hotels_name,hotels_link,hotels_rate,hotels_location,hotels_id#,hotels_description   
    return hotels_attributs

def reviews_tab_creation(): 
    reviews_name = []           #0
    reviews_rate = []           #1
    reviews_title = []          #2
    user_id = []                #3
    id_hotel = []               #4
    
    reviews_attributs = reviews_name,reviews_rate,reviews_title,user_id,id_hotel
    return reviews_attributs


def creation_hotel_dataframe(hotels_attributs):

    hotels = pd.DataFrame({
        'name': hotels_attributs[0],
        'link': hotels_attributs[1],
        'rate': hotels_attributs[2],
        'location': hotels_attributs[3],
        'h_id': hotels_attributs[4],
#        'description': hotels_attributs[5],
    })    
    return hotels


def creation_review_dataframe(reviews_attributs):

    hotels = pd.DataFrame({
        'name': reviews_attributs[0],
        'rate': reviews_attributs[1],
        'title': reviews_attributs[2],
        'u_id': reviews_attributs[3],
        'h_id': reviews_attributs[4],
    })
    return hotels


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


def get_hotelid_from_URL(url):
    cut_url = url[40:]
    regex = r"(?<=[g,d])([0-9]*)(?=-)"
    matchs = re.findall(regex, cut_url)
    h_id = "".join(matchs)
    
    return int(h_id)


def get_cid_from_username_in_URL(review):
    url = review.find('a',href = True)
    cut_url = url['href'][9:]
    u_id = hash(cut_url)
    
    return u_id


def hotel_scraping(hotels_attributs,a):
    
    # On parcourt chaque hotel et on récupère le lien
    link = a['href'].replace('\n',"")
    full_link = "https://www.tripadvisor.fr" + link
    hotels_attributs[1].append(full_link)
      
    hotel_content = requests.get(full_link)
    hotel_soup = BeautifulSoup(hotel_content.text, 'lxml')
    
    if hotel_soup.find('h1', class_="_1mTlpMC3") != None:
        hotels_attributs[0].append(hotel_soup.find('h1', class_="_1mTlpMC3").text.replace('\n',"").strip())
    else:
        hotels_attributs[0].append(None)
    # On prend ses caractéristiques
    if hotel_soup.find('span', class_="_3cjYfwwQ") != None:
        hotels_attributs[2].append(hotel_soup.find('span', class_="_3cjYfwwQ").text)
    else:
        hotels_attributs[2].append(None)
        
    if hotel_soup.find('span', class_="_3ErVArsu jke2_wbp") != None:
        hotels_attributs[3].append(hotel_soup.find('span', class_="_3ErVArsu jke2_wbp").text)
    else:
        hotels_attributs[3].append(None)
    
    h_id = get_hotelid_from_URL(full_link)                
    hotels_attributs[4].append(h_id)
    
     # Là, c'est les 5 div des commentaires
    if hotel_soup.find_all('div', class_='_2wrUUKlw _3hFEdNs8') != None:
        reviews = hotel_soup.find_all('div', class_='_2wrUUKlw _3hFEdNs8')
    else:
        print("Comments fail")
    
    return hotels_attributs,reviews,h_id


def new_hotel_scraping(hotels_attributs,new_hotel_soup,href):
    
    link = href
    full_link = "https://www.tripadvisor.fr" + link
    hotels_attributs[1].append(full_link)
      
    hotel_content = requests.get(full_link)
    hotel_soup = BeautifulSoup(hotel_content.text, 'lxml')
    
    if hotel_soup.find('h1', class_="_1mTlpMC3") != None:
        hotels_attributs[0].append(hotel_soup.find('h1', class_="_1mTlpMC3").text.replace('\n',"").strip())
    else:
        hotels_attributs[0].append(None)
    # On prend ses caractéristiques
    if hotel_soup.find('span', class_="_3cjYfwwQ") != None:
        hotels_attributs[2].append(hotel_soup.find('span', class_="_3cjYfwwQ").text)
    else:
        hotels_attributs[2].append(None)
        
    if hotel_soup.find('span', class_="_3ErVArsu jke2_wbp") != None:
        hotels_attributs[3].append(hotel_soup.find('span', class_="_3ErVArsu jke2_wbp").text)
    else:
        hotels_attributs[3].append(None)
    
    h_id = get_hotelid_from_URL(full_link)                
    hotels_attributs[4].append(h_id)
    
     # Là, c'est les 5 div des commentaires
    if hotel_soup.find_all('div', class_='_2wrUUKlw _3hFEdNs8') != None:
        reviews = hotel_soup.find_all('div', class_='_2wrUUKlw _3hFEdNs8')
    else:
        print("Comments fail")
    
    return hotels_attributs,reviews
            

def reviews_scraping(reviews_attributs,review,href,h_id):
    
    # On prend les caractéristiques de l'avis
    #print("#"*20,"REVIEW : ","#"*20,"\n\n")
    if review.find('a', class_="ui_header_link _1r_My98y") != None:
        reviews_attributs[0].append(review.find('a', class_="ui_header_link _1r_My98y").text)
    else: 
        reviews_attributs[0].append(None)
        
    
    if review.find('span', class_="ui_bubble_rating") != None:
        rating = review.find('span', class_="ui_bubble_rating")
        rating = delete_chars(rating)
        new_rate = create_rating(rating)                
        reviews_attributs[1].append(new_rate)
    else: 
        reviews_attributs[1].append(None)
        print("No rating")
        
    
    if review.find('a', class_="ocfR3SKN") != None:
        reviews_attributs[2].append(review.find('a', class_="ocfR3SKN").text)
    else:
        reviews_attributs[2].append(None)
    
    u_id = get_cid_from_username_in_URL(review)
    reviews_attributs[3].append(u_id)
    reviews_attributs[4].append(h_id)
    
    new_hotel_link = "https://www.tripadvisor.fr" + href
    new_hotel = requests.get(new_hotel_link)
    new_hotel_soup = BeautifulSoup(new_hotel.text, 'lxml')

    return reviews_attributs,new_hotel_soup

def user_reviews_scraping(reviews_attributs,review,href,h_id):
    
    # On prend les caractéristiques de l'avis
    #print("#"*20,"REVIEW : ","#"*20,"\n\n")
    if review.find('a', class_="ui_link _1r_My98y") != None:
        reviews_attributs[0].append(review.find('a', class_="ui_link _1r_My98y").text)
    else: 
        reviews_attributs[0].append(None)
        
    
    if review.find('span', class_="ui_bubble_rating") != None:
        rating = review.find('span', class_="ui_bubble_rating")
        rating = delete_chars(rating)
        new_rate = create_rating(rating)                
        reviews_attributs[1].append(new_rate)
    else: 
        reviews_attributs[1].append(None)
        print("No rating")
        
        
    if review.find('div', class_="_3IEJ3tAK _2K4zZcBv") != None:
        reviews_attributs[2].append(review.find('div', class_="_3IEJ3tAK _2K4zZcBv").text)
    else:
        reviews_attributs[2].append(None)
    
    u_id = get_cid_from_username_in_URL(review)
    reviews_attributs[3].append(u_id)
    reviews_attributs[4].append(h_id)
    
    new_hotel_link = "https://www.tripadvisor.fr" + href
    new_hotel = requests.get(new_hotel_link)
    new_hotel_soup = BeautifulSoup(new_hotel.text, 'lxml')

    return reviews_attributs,new_hotel_soup
        

def test_nb_user_reviews(review):
    if review.find('span', class_='_1fk70GUn') != None:
        nb_comment = review.find('span', class_='_1fk70GUn').text.strip()
    else:
        nb_comment = "10000000"
    if len(nb_comment) <= 4 and int(nb_comment) > 1:
        result = True
    else:
        result = False
        
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
            
    return test,href



if __name__ == "__main__":
    
    
    for i in range(2):
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
                            test,href = test_hotel_or_restau(user_review)
                            if test == "Hotel":
                                reviews_attributs,new_hotel_soup = reviews_scraping(user_review,href)
                                hotel_scraping(new_hotel_soup)
    


