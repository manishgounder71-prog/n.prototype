import random

class RecommendationEngine:
    def __init__(self, movie_database):
        self.db = movie_database
        
        # Mood to genre mapping
        self.mood_mappings = {
            'happy': {
                'genres': ['Comedy', 'Romance', 'Musical', 'Family', 'Animation'],
                'min_rating': 7.0,
                'description': 'Feel-good movies to boost your happiness'
            },
            'sad': {
                'genres': ['Drama', 'Romance'],
                'min_rating': 7.5,
                'description': 'Emotional films that understand your feelings'
            },
            'excited': {
                'genres': ['Action', 'Adventure', 'Thriller', 'Sci-Fi'],
                'min_rating': 7.0,
                'description': 'High-energy movies to match your excitement'
            },
            'relaxed': {
                'genres': ['Documentary', 'Animation', 'Fantasy'],
                'min_rating': 7.5,
                'description': 'Calming content for peaceful viewing'
            },
            'scared': {
                'genres': ['Horror', 'Mystery', 'Thriller'],
                'min_rating': 7.0,
                'description': 'Thrilling films to embrace the fear'
            },
            'inspired': {
                'genres': ['Biography', 'Documentary', 'Sports', 'Drama'],
                'min_rating': 7.5,
                'description': 'Motivational stories to fuel your ambition'
            }
        }
    
    def get_recommendations_by_mood(self, mood, limit=6):
        """
        Get movie recommendations based on user's mood
        
        Args:
            mood: User's current mood (happy, sad, excited, relaxed, scared, inspired)
            limit: Maximum number of recommendations to return
        
        Returns:
            Dictionary with recommendations and mood info
        """
        mood = mood.lower()
        
        if mood not in self.mood_mappings:
            return {
                'error': f'Unknown mood: {mood}',
                'available_moods': list(self.mood_mappings.keys())
            }
        
        mood_config = self.mood_mappings[mood]
        genres = mood_config['genres']
        min_rating = mood_config['min_rating']
        
        # Get movies matching the genres
        matching_movies = self.db.get_movies_by_genres(genres)
        
        # Filter by minimum rating
        filtered_movies = self.db.filter_by_rating(matching_movies, min_rating)
        
        # Score and rank movies
        scored_movies = self._score_movies(filtered_movies, genres)
        
        # Sort by score (descending) and get top recommendations
        scored_movies.sort(key=lambda x: x['recommendation_score'], reverse=True)
        recommendations = scored_movies[:limit]
        
        return {
            'mood': mood,
            'description': mood_config['description'],
            'genres': genres,
            'count': len(recommendations),
            'recommendations': recommendations
        }
    
    def _score_movies(self, movies, preferred_genres):
        """
        Score movies based on genre matching and rating
        
        Scoring algorithm:
        - Base score from rating (0-10)
        - Bonus points for each matching genre (+2 per genre)
        - Slight randomization for variety (±0.5)
        """
        scored_movies = []
        
        for movie in movies:
            score = movie['rating']  # Base score from rating
            
            # Count matching genres
            matching_genres = sum(1 for genre in movie['genres'] if genre in preferred_genres)
            score += matching_genres * 2  # Bonus for genre matches
            
            # Add slight randomization for variety
            score += random.uniform(-0.5, 0.5)
            
            movie_copy = movie.copy()
            movie_copy['recommendation_score'] = round(score, 2)
            movie_copy['matching_genres'] = matching_genres
            scored_movies.append(movie_copy)
        
        return scored_movies
    
    def get_similar_movies(self, movie_id, limit=5):
        """
        Get movies similar to a given movie based on genres
        """
        movie = self.db.get_movie_by_id(movie_id)
        
        if not movie:
            return {'error': 'Movie not found'}
        
        # Get movies with similar genres
        similar_movies = self.db.get_movies_by_genres(movie['genres'])
        
        # Remove the original movie
        similar_movies = [m for m in similar_movies if m['id'] != movie_id]
        
        # Score based on genre overlap
        scored_movies = self._score_movies(similar_movies, movie['genres'])
        scored_movies.sort(key=lambda x: x['recommendation_score'], reverse=True)
        
        return {
            'original_movie': movie,
            'similar_movies': scored_movies[:limit]
        }
    
    def get_all_moods(self):
        """Return all available moods with descriptions"""
        return {
            mood: {
                'description': config['description'],
                'genres': config['genres']
            }
            for mood, config in self.mood_mappings.items()
        }
