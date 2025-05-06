class MovieRecommender:
    def __init__(self, user_name):
        self.user_name = user_name
        self.preferences = {
            'genres': [],
            'actors': [],
            'directors': [],
            'watched_movies': set()
        }
        self.mood_recommendations = {
            'happy': ['comedy', 'adventure', 'family'],
            'thoughtful': ['drama', 'documentary', 'indie'],
            'excited': ['action', 'thriller', 'sci-fi'],
            'relaxed': ['romance', 'animation', 'comedy']
        }

    def update_preferences(self, category, items):
        if category in self.preferences:
            if isinstance(self.preferences[category], list):
                self.preferences[category].extend(items)
            else:
                self.preferences[category].update(items)

    def get_mood_based_recommendations(self, current_mood):
        if current_mood.lower() in self.mood_recommendations:
            return self.mood_recommendations[current_mood.lower()]
        return []

    def recommend_movies(self, current_mood=None, limit=5):
        print(f"\nMovie Recommendations for {self.user_name}:")
        
        if current_mood:
            mood_genres = self.get_mood_based_recommendations(current_mood)
            print(f"\nBased on your {current_mood} mood, you might enjoy:")
            # Here you would implement actual movie recommendations based on mood
            # This is a placeholder for demonstration
            print(f"Suggested genres: {', '.join(mood_genres)}")

        print("\nPersonalized Recommendations:")
        # This is where you would implement the actual recommendation algorithm
        # For now, we'll just show a placeholder message
        print("Based on your preferences in:")
        for category, items in self.preferences.items():
            if items and category != 'watched_movies':
                print(f"- {category.capitalize()}: {', '.join(items[:3])}")

    def add_watched_movie(self, movie):
        self.preferences['watched_movies'].add(movie)

# Example usage
def main():
    recommender = MovieRecommender("Trae")
    
    # Update user preferences
    recommender.update_preferences('genres', ['sci-fi', 'thriller', 'drama'])
    recommender.update_preferences('actors', ['Tom Hanks', 'Leonardo DiCaprio'])
    recommender.update_preferences('directors', ['Christopher Nolan', 'Martin Scorsese'])
    
    # Add some watched movies
    recommender.add_watched_movie("Inception")
    recommender.add_watched_movie("The Departed")
    
    # Get recommendations
    recommender.recommend_movies(current_mood="thoughtful")

if __name__ == "__main__":
    main()