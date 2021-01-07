# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 20:32:54 2020

@author: Alex
"""


from collections import defaultdict

from surprise import SVD, NMF
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import cross_validate
import pandas as pd
from surprise import Reader
from surprise.model_selection import train_test_split
from surprise.model_selection import GridSearchCV


def get_clean_data():
    
    reviews = pd.read_csv('reviews.csv')
    
    reviews["rate"] = reviews["rate"].astype(str).apply(lambda x: x.replace(',','.'))
    reviews["rate"] = reviews["rate"].astype(float)
    
    df = reviews.drop('title', 1)
    df = df.drop('name', 1)
    df = df.drop('Unnamed: 0', 1)
    
    df = df.fillna(0)
    
    return df

def define_format_and_train_model(df,model= "SVD"):
    
    # Define the format
    reader = Reader()
    data = Dataset.load_from_df(df[['u_id', 'h_id', 'rate']], reader)
    
    if model == "SVD":
        algo = SVD() # ou NMF()
        trainset = data.build_full_trainset()   #Build on entire data set
        algo.fit(trainset)
        
        testset = trainset.build_anti_testset()
        
        #Predicting the ratings for testset
        predictions = algo.test(testset)
        erreur = accuracy.rmse(predictions)
    
    elif model == "MNF":
        algo=NMF()
        trainset = data.build_full_trainset()   #Build on entire data set
        algo.fit(trainset)
        
        testset = trainset.build_anti_testset()      
        #Predicting the ratings for testset
        predictions=algo.test(testset)
        erreur=accuracy.rmse(predictions)
   
    #results = cross_validate(algo, data, measures=['RMSE'], cv=3, verbose=True)
    
    return predictions


def get_all_predictions(prediction,n):
 
    # First map the predictions to each user.
    similar_n = defaultdict(list)    
    for uid, iid, true_r, est, _ in prediction:
        similar_n[uid].append((iid, est))

    # sort the predictions for each user
    for uid, user_ratings in similar_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        similar_n[uid]=user_ratings[:n]
    return similar_n


def get_recommandations_for_a_user(predictions,nb_predictions=4,user_id= 3227041573719229893):
    
    pred_user = get_all_predictions(predictions,nb_predictions)
    
    #pred_user1= get_all_predictions(predictions1,n)
    
    tmp = pd.DataFrame.from_dict(pred_user)
    tmp_transpose = tmp.transpose()
    
    results_pred = tmp_transpose.loc[user_id]
    
    #format de results_pred (moviedid, rating), mais on va extraire movieID
    recommended_hotel_ids=[]
    for x in range(0, nb_predictions):
        recommended_hotel_ids.append(results_pred[x][0])
      
    hotels = pd.read_csv('hotels.csv')
    hotels = hotels.drop('Unnamed: 0', 1)
    
    hotels.head()
    recommended_hotels = hotels[hotels['h_id'].isin(recommended_hotel_ids)]
    recommended_hotels.drop_duplicates(subset ="h_id",keep = 'first', inplace=True)
    
    return recommended_hotels


if __name__ == "__main__":
    
    df = get_clean_data()
    predictions = define_format_and_train_model(df)
    recommended_hotels = get_recommandations_for_a_user(predictions)
    print(recommended_hotels)
    
    

 

