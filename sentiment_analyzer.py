from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon', quiet=True)
        
        self.sia = SentimentIntensityAnalyzer()
    
    def analyze_with_vader(self, text):
        """
        Analyze sentiment using VADER (Valence Aware Dictionary and sEntiment Reasoner)
        VADER is specifically attuned to sentiments expressed in social media and works
        well for movie reviews.
        
        Returns a dictionary with:
        - compound: normalized compound score (-1 to 1)
        - pos: positive score
        - neu: neutral score
        - neg: negative score
        """
        scores = self.sia.polarity_scores(text)
        return scores
    
    def analyze_with_textblob(self, text):
        """
        Analyze sentiment using TextBlob
        
        Returns:
        - polarity: -1 (negative) to 1 (positive)
        - subjectivity: 0 (objective) to 1 (subjective)
        """
        blob = TextBlob(text)
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
    
    def analyze(self, text):
        """
        Main analysis method that combines both VADER and TextBlob
        
        Returns comprehensive sentiment analysis results
        """
        if not text or not text.strip():
            return {
                'error': 'Empty text provided'
            }
        
        # Get VADER scores
        vader_scores = self.analyze_with_vader(text)
        
        # Get TextBlob scores
        textblob_scores = self.analyze_with_textblob(text)
        
        # Determine overall sentiment based on compound score
        compound = vader_scores['compound']
        if compound >= 0.05:
            sentiment = 'positive'
            emoji = '😊'
        elif compound <= -0.05:
            sentiment = 'negative'
            emoji = '😞'
        else:
            sentiment = 'neutral'
            emoji = '😐'
        
        # Calculate confidence (absolute value of compound score)
        confidence = abs(compound)
        
        return {
            'sentiment': sentiment,
            'emoji': emoji,
            'confidence': round(confidence * 100, 2),
            'scores': {
                'compound': round(compound, 4),
                'positive': round(vader_scores['pos'], 4),
                'neutral': round(vader_scores['neu'], 4),
                'negative': round(vader_scores['neg'], 4),
                'polarity': round(textblob_scores['polarity'], 4),
                'subjectivity': round(textblob_scores['subjectivity'], 4)
            },
            'text_length': len(text),
            'word_count': len(text.split())
        }
    
    def get_sentiment_label(self, compound_score):
        """Convert compound score to sentiment label"""
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
