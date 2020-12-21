# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 13:36:59 2020

@author: Alex

i=df[df[‘Name’]==’Will’]
print(i)
print(new_df['h_id']==187147198174])
"""
import pandas as pd 
import nltk 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel


def create_clean_df():
    hotels = pd.read_csv('hotels.csv')
    reviews = pd.read_csv('reviews.csv', index_col = 'h_id')
    
    # On supprime tous les doublons 
    reviews.drop_duplicates(subset ="title",keep = 'first', inplace=True)
    hotels.drop_duplicates(subset ="name",keep = 'first', inplace=True)
    
    # On affiche le nombre de lignes qu'il nous reste
    print(hotels.info())
    print(reviews.info())
    return hotels,reviews


def nlp_processing(hotels_id_list,hotels,reviews):
    
    # On créé 2 tableaux qui permettront de créer le dataframe des avis
    all_reviews = []
    all_h_id = []
    
    # On parcourt notre liste d'ID uniques 
    for h_id in hotels_id_list:
        
        # On séléctionne la/les ligne(s) contenant l'ID et on récupère le titre du commentaire
        # On obtient soit un string s'il y a 1 seul commentaire pour l'hotel en question soit une liste de string
        rev = reviews.loc[h_id].title
        # On teste pour savoir le type de rev
        if type(rev) == str:
            # On garde la variable comme ça si c'est un string
            liste_str = rev
        else:
            # On convertit la pandas.series en liste facilement lisible
            liste = rev.tolist()
            # On convertit la liste en string car on veut juste tous les mots
            liste_str = ' '.join([str(elem) for elem in liste]) 
        
        liste_str = liste_str.lower()
        word_list = word_tokenize(liste_str)
    
        liste_ponct = [",", ".", "!", "?", ";"]
        word_to_del = liste_ponct + stopwords.words('french')
        
        word_list = [word for word in word_list if word not in word_to_del]
        
        stem_word_list = stemming_word(word_list)      
        new_list =  ' '.join([str(elem) for elem in stem_word_list]) 
        
        # On ajoute nos variables aux tableaux
        all_reviews.append(new_list)
        all_h_id.append(h_id)
            
        # On créé le df à partir des 2 tableaux
        df = pd.DataFrame({'h_id':all_h_id,'reviews': all_reviews})     
    
    return df
  
    
def stemming_word(word_list):

    port_stemmer = PorterStemmer()
    stem_word_list = []
    
    for word in word_list:
        stem_word = port_stemmer.stem(word)
        stem_word_list.append(stem_word)
    
    return stem_word_list
    

def tfidf_on_reviews(df):
    
    reviews = df['reviews']
    
    tfidfs = TfidfVectorizer()
    tf_matrice = tfidfs.fit_transform(reviews)

    tfidf_tokens = tfidfs.get_feature_names()
    
    df_tfidfvect = pd.DataFrame(data = tf_matrice.toarray(),index = df["h_id"], columns = tfidf_tokens)

    print("\nTD-IDF Vectorizer\n")
    print(df_tfidfvect)
    return(df_tfidfvect)



def get_df_with_best_reviews(reviews):
    h_id_list = []
    users = []
    users_id_list = reviews['u_id']
        
    for u_id in users_id_list:

        all_h_id = reviews.loc[(reviews['u_id'] == u_id) & (reviews['rate'] >= 4)].h_id.values
        print(type(all_h_id))
        h_id_list.append(all_h_id)
        users.append(u_id)
            
    df_users = pd.DataFrame({'u_id':users,'all_h_id': h_id_list})  
    return(df_users)
    


def get_recommandation(df, cosine_sim, h_id):
    
   # list_hotel_id = df['h_id']
    number_hotel = df.index[df['h_id'] == h_id].tolist()
    print("number_hotel :",number_hotel)
    list_hotel_sim = cosine_sim[:,number_hotel[0]]
    scores_series = pd.Series(list_hotel_sim).sort_values(ascending=False)
    scores_series_fi=scores_series.head(10).keys()  
    final= hotels['name'].iloc[scores_series_fi]
    
    return final

if __name__ == "__main__":
    
    
    hotels, reviews = create_clean_df()
    hotels_id_list = reviews.index.drop_duplicates(keep = 'first')
    df = nlp_processing(hotels_id_list, hotels, reviews)
    df_tfidfvect = tfidf_on_reviews(df)
    cosine_sim = linear_kernel(df_tfidfvect, df_tfidfvect)
    
    reviews = pd.read_csv('reviews.csv')
    reviews["rate"] = reviews["rate"].astype(str).apply(lambda x: x.replace(',','.'))
    reviews["rate"] = reviews["rate"].astype(float)
    df_users = get_df_with_best_reviews(reviews)


    # On fait la recommandation pour chacun des users :
    # Bug : Un des users à un hotels qui n'existe pas dans df
    for hotel_user in df_users["all_h_id"]:   
        print(type(hotel_user))
        if hotel_user.size == 0 :
            liste_reco = None
        else :
            print(hotel_user)
            liste_reco = get_recommandation(df, cosine_sim, hotel_user[0])
            print(liste_reco)
    #h_id = 187147228694
    #regarder avec df
            
    n_input = 187147498038
    df[(df == n_input).any(1)].stack()[lambda x: x != n_input].unique()
    
    

    

    
    
    
    
    
    
    
   
       
    
    