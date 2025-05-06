import streamlit as st
import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page config
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("C:/Users/kumar/OneDrive/Desktop/Movie/tmdb_5000_movies.csv")
    # Process genres from JSON string to list of names
    df['genres'] = df['genres'].apply(lambda x: [i['name'] for i in eval(x)] if pd.notna(x) else [])
    # Create a string of all text data for TF-IDF
    df['combined_features'] = df['overview'].fillna('') + ' ' + \
                             df['genres'].apply(lambda x: ' '.join(x))
    return df

movies = load_data()

# TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['combined_features'])

# Cosine Similarity Matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Index mapping
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# Recommendation Function
def recommend(title):
    if title not in indices:
        return pd.DataFrame()
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    movie_indices = [i[0] for i in sim_scores]
    
    result = movies.iloc[movie_indices].copy()
    result['similarity_score'] = [i[1] for i in sim_scores]
    return result

# Sidebar
st.sidebar.title("🎬 Navigation")
page = st.sidebar.radio("Go to", ["Movie Recommender", "About"])

if page == "Movie Recommender":
    # Main content
    st.title("🎬 Movie Recommendation System")
    st.write("""Discover movies similar to your favorites! Enter a movie title below 
             and get personalized recommendations based on plot, genres, and themes.""")
    
    # Search box with autocomplete
    movie_input = st.selectbox(
        "Enter a movie title:",
        options=movies['title'].sort_values().tolist(),
        index=None,
        placeholder="Type to search..."
    )

    if st.button("Get Recommendations", type="primary"):
        if movie_input:
            with st.spinner('Finding similar movies...'):
                recommendations = recommend(movie_input)
                
                if not recommendations.empty:
                    st.subheader("Top 5 Movie Recommendations")
                    
                    # Display recommendations in a grid
                    cols = st.columns(5)
                    for idx, (_, movie) in enumerate(recommendations.iterrows()):
                        with cols[idx]:
                            st.markdown(f"**{movie['title']}**")
                            st.write(f"⭐ {movie['vote_average']:.1f}/10")
                            st.write(f"*{', '.join(movie['genres'][:2])}*")
                            st.write(f"📅 {pd.to_datetime(movie['release_date']).year}")
                            st.write(f"Similarity: {movie['similarity_score']:.2%}")
                else:
                    st.error("Movie not found in database.")
        else:
            st.warning("Please enter a movie title to continue.")

        # Show selected movie details
        if movie_input and movie_input in indices:
            st.divider()
            st.subheader("Selected Movie Details")
            movie_idx = indices[movie_input]
            movie_details = movies.iloc[movie_idx]
            
            col1, col2 = st.columns([2, 3])
            with col1:
                st.markdown(f"**Title:** {movie_details['title']}")
                st.write(f"**Release Date:** {pd.to_datetime(movie_details['release_date']).strftime('%B %d, %Y')}")
                st.write(f"**Rating:** ⭐ {movie_details['vote_average']}/10 ({movie_details['vote_count']} votes)")
                st.write(f"**Genres:** {', '.join(movie_details['genres'])}")
                if movie_details['tagline']:
                    st.write(f"**Tagline:** *{movie_details['tagline']}*")
            with col2:
                st.write("**Overview:**")
                st.write(movie_details['overview'])
                if movie_details['homepage']:
                    st.write(f"**Website:** [{movie_details['homepage']}]({movie_details['homepage']})")

else:
    # About page
    st.title("About the Movie Recommender")
    st.write("""
    This movie recommendation system uses Natural Language Processing (NLP) to find similar movies.
    It analyzes movie descriptions, genres, and other features using TF-IDF vectorization with 
    cosine similarity to match movies with similar themes, plots, and characteristics.
    
    ### Features:
    - Content-based movie recommendations
    - Detailed movie information
    - Similarity scores
    - User-friendly interface
    
    ### Data Source:
    The system uses the TMDB (The Movie Database) dataset, which includes:
    - Movie descriptions and genres
    - Release dates and ratings
    - Production information
    - And more!
    
    ### How it works:
    1. Enter a movie title you enjoy
    2. The system analyzes the movie's features
    3. It finds movies with similar characteristics
    4. You get personalized movie recommendations!
    """)
