# import Libararies 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
import pickle

# data cleaning and normalization 

def preprocess(dataset):
    # Retrieve the columns 
    
    condition_columns = ['condition_type1', 'condition_type2', 'condition_type3', 'condition_type4', 'condition_type5', 'condition_type6', 'condition_type7', 'condition_type8', 'condition_type9']
    
    # The selected columns are to have their missing values replaced with an empty string. 
   
    df_conditions = dataset[condition_columns].fillna('')

    return df_conditions.apply(lambda x: ' '.join(x), axis=1)

#This is the model

class Model:

    def __init__(self, dataset_path):
        # Load the dataset
        self.dataset = pd.read_csv(dataset_path)

        # Preprocess the conditions column
        self.dataset.loc[:, 'conditions'] =preprocess(self.dataset)

        # Initialize the TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer()

        # Calculate the TF-IDF matrix for the conditions in the dataset
        self.tfidf_matrix = self.vectorizer.fit_transform(self.dataset['conditions'])

    def recommend_remedies(self, remedy_type, conditions):
        # Find remedies for the exact conditions selected by the user
        filtered_dataset = self.dataset.loc[(self.dataset['remedy_type'] == remedy_type)]

        exact_conditions_array = []
        for condition in conditions:
            matchers = filtered_dataset.loc[filtered_dataset['conditions'].str.contains(condition)]
            if not matchers.empty:
                filtered_dataset = matchers
                exact_conditions_array.append(condition)
            else:
                similar_conditions_Array = []
                for joined_condition in self.dataset['conditions']:
                    if fuzz.token_set_ratio(condition, joined_condition) > 90:
                        similar_conditions_Array.append(joined_condition)
                exact_conditions_array.append(' or '.join(similar_conditions_Array))
        filtered_dataset.loc[:, 'conditions'] =preprocess(filtered_dataset)

        # Calculate the TF-IDF matrix for the conditions 
        tfidf_matrix = self.vectorizer.transform(filtered_dataset['conditions'])

        # Concatenate the input conditions and similar conditions
        user_conditions = ' and '.join(exact_conditions_array)

        # Transform the user conditions into a TF-IDF matrix
        user_tfidf = self.vectorizer.transform([user_conditions])

        # Calculate the cosine similarity between the user conditions and the conditions in the filtered dataset
        cosine_similarity_score = cosine_similarity(user_tfidf, tfidf_matrix)

        # Sort the filtered dataset based on the cosine similarity scores
        sorted_indexes = cosine_similarity_score.argsort()[0][::-1]
        sorted_dataset = filtered_dataset.iloc[sorted_indexes]

        list_of_remedy_names = sorted_dataset['remedy_name'].tolist()
        list_of_remedy_indexes = sorted_dataset['index'].tolist()

        return list_of_remedy_indexes, list_of_remedy_names
    
    
    # Gives the remedy name and index function 

    def recommend(self, remedy_type, conditions):
        list_of_remedy_names, list_of_remedy_indexes = self.recommend_remedies(remedy_type, conditions)
        print(f"Recommended {remedy_type} remedies for {conditions}:")
        for name in list_of_remedy_names:
            print(name)

        return list_of_remedy_names, list_of_remedy_indexes
           
   # Export the model function

    def model_export(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

model = Model('E:\FYP\DATASET\Remedy Dataset -( the final remedy recomendation dataset ) - final sheet .csv')
model.model_export('model.pkl')
