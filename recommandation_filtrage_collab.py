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

reviews = pd.read_csv('reviews.csv')

reviews["rate"] = reviews["rate"].astype(str).apply(lambda x: x.replace(',','.'))
reviews["rate"] = reviews["rate"].astype(float)

df = reviews.drop('title', 1)
df = df.drop('name', 1)
df = df.drop('Unnamed: 0', 1)

# Define the format
reader = Reader()
data = Dataset.load_from_df(df[['u_id', 'h_id', 'rate']], reader)
algo = SVD() # ou NMF()

#algo1=NMF()
#results = cross_validate(algo, data, measures=['RMSE'], cv=3, verbose=True)

trainset = data.build_full_trainset()   #Build on entire data set
algo.fit(trainset)

testset = trainset.build_anti_testset()

#Predicting the ratings for testset
predictions = algo.test(testset)
#predictions1=algo1.test(testset)
erreur = accuracy.rmse(predictions)
#erreur1=accuracy.rmse(predictions1)

#%%
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
n=4
pred_user = get_all_predictions(predictions,n)

#pred_user1= get_all_predictions(predictions1,n)

tmp = pd.DataFrame.from_dict(pred_user)
tmp_transpose = tmp.transpose()

#recommandation pour user x
user_id= 3227041573719229893
results_pred = tmp_transpose.loc[user_id]

#format de results_pred (moviedid, rating), mais on va extraire movieID
recommended_movie_ids=[]
for x in range(0, n):
    recommended_movie_ids.append(results_pred[x][0])
  
movies = pd.read_csv('reviews.csv')
movies.head()
recommended_movies = movies[movies['h_id'].isin(recommended_movie_ids)]


 

