
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
df = pd.read_csv(r"C:\Users\amnsh\OneDrive\Desktop\ML\My flask codes\books.csv")

# Select the columns of interest
columns_of_interest = ['title', 'authors', 'average_rating', 'num_pages']
df = df[columns_of_interest]

# Convert the 'authors' column to a list of strings
df['authors'] = df['authors'].apply(lambda x: x.split(','))

# Convert the 'title' and 'authors' columns to lowercase
df['title'] = df['title'].str.lower()
df['authors'] = df['authors'].apply(lambda x: [s.lower().strip() for s in x])

# Create a TfidfVectorizer object to convert the 'title' and 'authors' columns to numerical vectors
tfidf = TfidfVectorizer(stop_words='english')

# Create a matrix of TF-IDF features for the 'title' and 'authors' columns
tfidf_matrix = tfidf.fit_transform(df['title'] + ' ' + df['authors'].apply(lambda x: ' '.join(x)))

# Calculate the cosine similarity between each pair of books
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Define a function to recommend books based on a given book title
def get_recommendations(title):
    # Get the index of the book with the given title
    idx = df[df['title'] == title].index[0]

    # Get the pairwise similarity scores between the book and all other books
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the books based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 10 most similar books (excluding itself)
    sim_scores = sim_scores[1:11]

    # Get the indices of the top 10 most similar books
    book_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar books
    return df.iloc[book_indices]

# Ask the user to input a book title
title = input("Enter a book title: ").lower()

# Get the top 10 most similar books based on the input title
recommendations = get_recommendations(title)
print(recommendations)


pickle.dump(get_recommendations,open('rsmodel.pkl','wb'))