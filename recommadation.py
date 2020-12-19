# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 13:36:59 2020

@author: Alex
"""


import pandas as pd 

hotels = pd.read_csv('hotels.csv')
reviews = pd.read_csv('reviews.csv', index_col = 'h_id')

# On supprime tous les doublons 
reviews.drop_duplicates(subset ="title",keep = 'first', inplace=True)
hotels.drop_duplicates(subset ="name",keep = 'first', inplace=True)

# On affiche le nombre de lignes qu'il nous reste
print(hotels.info())
print(reviews.info())

# On créé une liste de tous les id en supprimant les id en doublons
hotels_id_list = reviews.index.drop_duplicates(keep = 'first')

# On créé 2 tableaux qui permettront de créer le dataframe des avis
all_reviews = []
all_h_id = []

# On parcourt notre liste d'ID uniques 
for review in hotels_id_list:
    
    # On séléctionne la/les ligne(s) contenant l'ID et on récupère le titre du commentaire
    # On obtient soit un string s'il y a 1 seul commentaire pour l'hotel en question soit une liste de string
    rev = reviews.loc[review].title
    
    # On teste pour savoir le type de rev
    if type(rev) == str:
        # On garde la variable comme ça si c'est un string
        liste = rev
    else:
        # On convertit la pandas.series en liste facilement lisible
        liste = rev.tolist()
        
    # On ajoute nos variables aux tableaux
    all_reviews.append(liste)
    all_h_id.append(review)

# On créé le df à partir des 2 tableaux
new_df = pd.DataFrame({
        'Hotel id':all_h_id,
        'reviews': all_reviews})

print(new_df)