from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from sentiment_analyzer import SentimentAnalyzer
from movie_database import MovieDatabase
from recommendation_engine import RecommendationEngine
from ai_assistant import MovieAIAssistant

app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize components
sentiment_analyzer = SentimentAnalyzer()
movie_db = MovieDatabase('movies.json')
recommendation_engine = RecommendationEngine(movie_db)
ai_assistant = MovieAIAssistant(movie_db)

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', path)

@app.route('/api/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    """
    Analyze sentiment of movie review text
    
    Expected JSON body:
    {
        "text": "This movie was absolutely amazing! I loved every moment."
    }
    
    Returns:
    {
        "sentiment": "positive",
        "confidence": 95.5,
        "scores": {...},
        ...
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing "text" field in request body'
            }), 400
        
        text = data['text']
        
        # Analyze sentiment
        result = sentiment_analyzer.analyze(text)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/get_recommendations', methods=['POST'])
def get_recommendations():
    """
    Get movie recommendations based on mood
    
    Expected JSON body:
    {
        "mood": "happy",
        "limit": 6
    }
    
    Returns:
    {
        "mood": "happy",
        "description": "...",
        "recommendations": [...]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'mood' not in data:
            return jsonify({
                'error': 'Missing "mood" field in request body',
                'available_moods': list(recommendation_engine.mood_mappings.keys())
            }), 400
        
        mood = data['mood']
        limit = data.get('limit', 6)  # Default to 6 recommendations
        
        # Get recommendations
        result = recommendation_engine.get_recommendations_by_mood(mood, limit)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/movies', methods=['GET'])
def get_movies():
    """
    Get all movies or search movies
    
    Query parameters:
    - search: Search query (optional)
    - genre: Filter by genre (optional)
    - limit: Maximum number of results (optional)
    """
    try:
        search_query = request.args.get('search')
        genre_filter = request.args.get('genre')
        limit = request.args.get('limit', type=int)
        
        movies = movie_db.get_all_movies()
        
        # Apply search filter
        if search_query:
            movies = movie_db.search_movies(search_query)
        
        # Apply genre filter
        if genre_filter:
            movies = movie_db.get_movies_by_genre(genre_filter)
        
        # Apply limit
        if limit:
            movies = movies[:limit]
        
        return jsonify({
            'count': len(movies),
            'movies': movies
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/moods', methods=['GET'])
def get_moods():
    """Get all available moods with their descriptions"""
    try:
        moods = recommendation_engine.get_all_moods()
        return jsonify({
            'moods': moods
        })
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/movie/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Get a specific movie by ID"""
    try:
        movie = movie_db.get_movie_by_id(movie_id)
        
        if not movie:
            return jsonify({
                'error': f'Movie with ID {movie_id} not found'
            }), 404
        
        return jsonify(movie)
    
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/similar/<int:movie_id>', methods=['GET'])
def get_similar(movie_id):
    """Get similar movies to a given movie"""
    try:
        limit = request.args.get('limit', default=5, type=int)
        result = recommendation_engine.get_similar_movies(movie_id, limit)
        
        if 'error' in result:
            return jsonify(result), 404
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/ask_ai', methods=['POST'])
def ask_ai():
    """
    Ask the AI assistant about movies
    
    Expected JSON body:
    {
        "message": "What movie should I watch tonight?",
        "conversation_history": []  # optional
    }
    
    Returns:
    {
        "response": "AI response text",
        "success": true
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing "message" field in request body'
            }), 400
        
        message = data['message']
        conversation_history = data.get('conversation_history', [])
        
        # Get AI response
        result = ai_assistant.chat(message, conversation_history)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'response': 'Sorry, I encountered an error. Please try again.'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'movie_count': len(movie_db.get_all_movies()),
        'available_moods': list(recommendation_engine.mood_mappings.keys())
    })

if __name__ == '__main__':
    print("Movie Review Sentiment Analysis System")
    print("=" * 50)
    print(f"Loaded {len(movie_db.get_all_movies())} movies")
    print(f"Available moods: {', '.join(recommendation_engine.mood_mappings.keys())}")
    print("=" * 50)
    print("Starting server at http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
