# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 18:16:57 2020

@author: Victor HENRIO
"""

import scraping_functions as scrap


def main(nb_page=1):
    
    hotels_attributs = scrap.hotels_tab_creation()
    reviews_attributs = scrap.reviews_tab_creation()
    
    for i in range(nb_page):
        home_soup = scrap.homepage_request(1,i=0)
                
        if home_soup.find_all('a',  class_='property_title prominent') != None:
            for hotel_url in home_soup.find_all('a',  class_='property_title prominent'):
                hotels_attributs,reviews = scrap.hotel_scraping(hotels_attributs,hotel_url)
                print("#"*20,"\n\n")
                print(hotels_attributs)
                for review in reviews:
                    scrap.reviews_scraping(reviews_attributs,review,"")
                    result = scrap.test_nb_user_reviews(review)
                    if result == True: 
                        user_reviews = scrap.get_user_link(review)
                        for user_review in user_reviews:
                            test,href = scrap.test_hotel_or_restau(user_review)
                            if test == "Hotel":
                                reviews_attributs,new_hotel_soup = scrap.reviews_scraping(reviews_attributs,user_review,href)
                                hotels_attributs,reviews = scrap.new_hotel_scraping(hotels_attributs,new_hotel_soup,href)
    
    hotels = scrap.creation_hotel_dataframe(hotels_attributs)
    reviews = scrap.creation_review_dataframe(reviews_attributs)
    hotels.to_csv("data/hotels.csv", encoding="utf-8")
    reviews.to_csv("data/reviews.csv", encoding="utf-8")

    
    return hotels_attributs,reviews_attributs



if __name__ == "__main__":
    hotel,review = main()