# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 18:16:57 2020

@author: Victor HENRIO
"""

import scraping_functions as scrap


def main(nb_page=2):
    
    for i in range(nb_page):
        home_soup = scrap.homepage_request(1,i=0)
                
        if home_soup.find_all('a',  class_='property_title prominent') != None:
            for hotel_url in home_soup.find_all('a',  class_='property_title prominent'):
                reviews = scrap.hotel_scraping(hotel_url)
                print(reviews)


"""
    for i in range(nb_page=2):
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
"""


if __name__ == "__main__":
    main()