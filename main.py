# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 18:16:57 2020

@author: Victor HENRIO
"""

import main_scraping_function as scrap
import recommadation as contenu_reco
import recommandation_filtrage_collab as filt_collab_reco


def main(nb_page=20):
    
    #hotel,review = scrap.main_scraping_function()
    
    df_recommandations,df_users,df,df_tfidfvect,cosine_sim = contenu_reco.content_based_recommandation()   
    #Recommandation user = 1940342934814397417
    reco = df_recommandations.loc[df_recommandations['u_id'] == 1940342934814397417].recommandations
        
    df = filt_collab_reco.get_clean_data()
    predictions = filt_collab_reco.define_format_and_train_model(df)
    recommended_hotels = filt_collab_reco.get_recommandations_for_a_user(predictions)
    
    return df_recommandations, reco, recommended_hotels
    
    
    
if __name__ == "__main__":
    
    df_recommandations, reco, recommended_hotels = main()