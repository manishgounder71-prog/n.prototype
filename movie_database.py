import json
import os

class MovieDatabase:
    def __init__(self, json_file='movies.json'):
        self.json_file = json_file
        self.movies = self.load_movies()
    
    def load_movies(self):
        """Load movies from JSON file"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('movies', [])
        except FileNotFoundError:
            print(f"Error: {self.json_file} not found")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.json_file}")
            return []
    
    def get_all_movies(self):
        """Return all movies"""
        return self.movies
    
    def get_movie_by_id(self, movie_id):
        """Get a specific movie by ID"""
        for movie in self.movies:
            if movie['id'] == movie_id:
                return movie
        return None
    
    def get_movies_by_genre(self, genre):
        """Get all movies that contain the specified genre"""
        return [movie for movie in self.movies if genre in movie['genres']]
    
    def get_movies_by_genres(self, genres):
        """Get all movies that contain any of the specified genres"""
        matching_movies = []
        for movie in self.movies:
            if any(genre in movie['genres'] for genre in genres):
                matching_movies.append(movie)
        return matching_movies
    
    def filter_by_rating(self, movies, min_rating=0):
        """Filter movies by minimum rating"""
        return [movie for movie in movies if movie['rating'] >= min_rating]
    
    def search_movies(self, query):
        """Search movies by title or description"""
        query = query.lower()
        results = []
        for movie in self.movies:
            if (query in movie['title'].lower() or 
                query in movie['description'].lower()):
                results.append(movie)
        return results
    
    def get_top_rated(self, limit=10):
        """Get top rated movies"""
        sorted_movies = sorted(self.movies, key=lambda x: x['rating'], reverse=True)
        return sorted_movies[:limit]
