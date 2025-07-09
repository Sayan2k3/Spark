"""
Review Analysis Service for extracting insights from product reviews
"""
from typing import Dict, List, Any
import re
from collections import defaultdict


class ReviewAnalyzer:
    """Analyzes product reviews to extract feature-specific insights"""
    
    def __init__(self):
        self.feature_keywords = {
            'battery': ['battery', 'battery life', 'charge', 'charging', 'power', 'lasts', 'drain', 'mah'],
            'camera': ['camera', 'photo', 'picture', 'image', 'selfie', 'video', 'lens', 'megapixel', 'mp'],
            'performance': ['fast', 'speed', 'lag', 'smooth', 'performance', 'processor', 'ram', 'gaming'],
            'display': ['screen', 'display', 'brightness', 'colors', 'oled', 'refresh rate', 'resolution'],
            'storage': ['storage', 'memory', 'gb', 'space', 'capacity'],
            'build': ['build', 'quality', 'premium', 'durable', 'design', 'material', 'glass', 'aluminum']
        }
        
        self.sentiment_words = {
            'positive': ['excellent', 'amazing', 'great', 'good', 'love', 'best', 'awesome', 'fantastic', 
                        'perfect', 'impressive', 'outstanding', 'superb', 'wonderful'],
            'negative': ['poor', 'bad', 'terrible', 'worst', 'hate', 'disappointing', 'awful', 'horrible',
                        'mediocre', 'slow', 'issue', 'problem', 'fails']
        }
    
    def analyze_reviews_for_features(self, reviews: List[Dict[str, Any]], features: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Analyze reviews for specific features
        
        Args:
            reviews: List of review dictionaries with 'text' and 'rating' fields
            features: List of features to analyze (e.g., ['battery', 'camera'])
            
        Returns:
            Dictionary with feature analysis results
        """
        results = {}
        
        for feature in features:
            if feature not in self.feature_keywords:
                continue
                
            feature_mentions = []
            feature_ratings = []
            positive_count = 0
            negative_count = 0
            
            keywords = self.feature_keywords[feature]
            
            for review in reviews:
                review_text = review.get('text', '').lower()
                review_rating = review.get('rating', 3)
                
                # Check if review mentions this feature
                if any(keyword in review_text for keyword in keywords):
                    feature_mentions.append(review_text)
                    feature_ratings.append(review_rating)
                    
                    # Analyze sentiment
                    sentiment = self._analyze_sentiment(review_text)
                    if sentiment > 0:
                        positive_count += 1
                    elif sentiment < 0:
                        negative_count += 1
            
            if feature_mentions:
                avg_rating = sum(feature_ratings) / len(feature_ratings)
                sentiment_score = (positive_count - negative_count) / len(feature_mentions)
                
                results[feature] = {
                    'average_rating': round(avg_rating, 2),
                    'mention_count': len(feature_mentions),
                    'positive_mentions': positive_count,
                    'negative_mentions': negative_count,
                    'sentiment_score': round(sentiment_score, 2),
                    'sample_reviews': self._extract_sample_reviews(feature_mentions[:3], feature)
                }
            else:
                results[feature] = {
                    'average_rating': 0,
                    'mention_count': 0,
                    'positive_mentions': 0,
                    'negative_mentions': 0,
                    'sentiment_score': 0,
                    'sample_reviews': []
                }
        
        return results
    
    def _analyze_sentiment(self, text: str) -> int:
        """
        Simple sentiment analysis
        Returns: 1 for positive, -1 for negative, 0 for neutral
        """
        text_lower = text.lower()
        positive_score = sum(1 for word in self.sentiment_words['positive'] if word in text_lower)
        negative_score = sum(1 for word in self.sentiment_words['negative'] if word in text_lower)
        
        if positive_score > negative_score:
            return 1
        elif negative_score > positive_score:
            return -1
        return 0
    
    def _extract_sample_reviews(self, reviews: List[str], feature: str) -> List[str]:
        """Extract relevant snippets from reviews mentioning the feature"""
        samples = []
        keywords = self.feature_keywords.get(feature, [])
        
        for review in reviews:
            # Find sentences containing feature keywords
            sentences = re.split(r'[.!?]+', review)
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in keywords):
                    samples.append(sentence.strip())
                    break
        
        return samples[:3]  # Return up to 3 samples
    
    def generate_feature_summary(self, feature_analysis: Dict[str, Any], feature: str) -> str:
        """Generate a human-readable summary for a feature based on analysis"""
        if feature_analysis['mention_count'] == 0:
            return f"No reviews mention {feature}."
        
        rating = feature_analysis['average_rating']
        sentiment = feature_analysis['sentiment_score']
        
        if rating >= 4.5 and sentiment > 0.5:
            summary = f"Excellent {feature} performance with overwhelmingly positive reviews."
        elif rating >= 4.0 and sentiment > 0:
            summary = f"Very good {feature} with mostly positive feedback."
        elif rating >= 3.5:
            summary = f"Good {feature} with mixed reviews."
        elif rating >= 3.0:
            summary = f"Average {feature} performance with some concerns."
        else:
            summary = f"Below average {feature} with significant user complaints."
        
        return summary