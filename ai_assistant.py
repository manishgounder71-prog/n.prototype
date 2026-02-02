import os
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class MovieAIAssistant:
    def __init__(self, movie_database):
        self.db = movie_database
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key or self.api_key == 'your_openai_api_key_here':
            print("⚠️ Warning: OpenAI API key not configured. AI assistant will not work.")
            print("Please set OPENAI_API_KEY in your .env file")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
        
        # System prompt with movie database context
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self):
        """Build a system prompt with movie database context"""
        movies_list = self.db.get_all_movies()
        
        # Create a compact movie list for the AI
        movies_info = []
        for movie in movies_list[:20]:  # Limit to top 20 to save tokens
            movies_info.append(
                f"- {movie['title']} ({movie['year']}): {', '.join(movie['genres'])}, "
                f"Rating: {movie['rating']}/10"
            )
        
        movies_context = "\n".join(movies_info)
        
        return f"""You are a friendly and knowledgeable movie recommendation assistant for CineScope, 
a movie sentiment analysis and recommendation platform.

You help users discover movies based on their preferences, mood, and interests. You can:
- Recommend movies from our database
- Answer questions about movies, genres, directors, and actors
- Help users decide what to watch based on their mood
- Provide brief insights about films without spoilers
- Explain why certain movies might match their preferences

Here are some popular movies in our database:
{movies_context}

Guidelines:
- Be conversational and friendly
- Keep responses concise (2-3 sentences usually)
- Focus on recommendations from our database when possible
- Ask clarifying questions if needed
- Don't give away spoilers unless explicitly asked
- If a movie isn't in our database, you can still discuss it but mention we have similar options

Remember: You're helping people find their next favorite movie!"""
    
    def chat(self, user_message, conversation_history=None):
        """
        Send a message to OpenAI and get a response
        
        Args:
            user_message: The user's question
            conversation_history: List of previous messages (optional)
        
        Returns:
            Dictionary with AI response or error
        """
        if not self.client:
            return {
                'error': 'OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file.',
                'response': 'Sorry, the AI assistant is not currently available. Please configure your OpenAI API key.'
            }
        
        try:
            # Build messages array
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                'response': ai_response,
                'success': True
            }
        
        except Exception as e:
            error_msg = str(e)
            print(f"OpenAI API Error: {error_msg}")
            
            # Handle specific errors
            if 'api_key' in error_msg.lower():
                return {
                    'error': 'Invalid API key',
                    'response': 'There was an issue with the API key. Please check your configuration.'
                }
            elif 'rate_limit' in error_msg.lower():
                return {
                    'error': 'Rate limit exceeded',
                    'response': 'Too many requests. Please try again in a moment.'
                }
            else:
                return {
                    'error': f'API error: {error_msg}',
                    'response': 'Sorry, I encountered an error. Please try again.'
                }
    
    def get_movie_recommendation_prompt(self, mood, genres=None):
        """Generate a prompt to ask AI for recommendations based on mood"""
        prompt = f"I'm feeling {mood}. "
        if genres:
            prompt += f"I'm interested in {', '.join(genres)} movies. "
        prompt += "What movie would you recommend from the database and why?"
        return prompt
    
    def search_movies_in_db(self, query):
        """Search for movies in the database that match a query"""
        return self.db.search_movies(query)
