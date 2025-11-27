import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from collections import Counter
from typing import Dict, List, Tuple
from datetime import datetime

# Download necessary NLTK data
nltk.download('vader_lexicon')

class IssueAnalyzer:
    def __init__(self):
        """Initialize the analyzer with sentiment models"""
        # VADER for sentiment analysis (lightweight)
        self.vader = SentimentIntensityAnalyzer()
        
        # Keywords for different issue categories
        self.issue_keywords = {
            "infrastructure": ["water", "electricity", "road", "bridge", "power", "sewage"],
            "healthcare": ["hospital", "clinic", "doctor", "medicine", "healthcare", "medical"],
            "safety": ["crime", "accident", "dangerous", "emergency", "police", "fire"],
            "social_services": ["welfare", "housing", "food security", "unemployment", "social support"],
            "governance": ["complaint", "service delivery", "government", "municipality", "council"]
        }
        
        # Urgency indicators
        self.urgency_keywords = ["emergency", "urgent", "dying", "dangerous", "critical", "immediate"]
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Remove mentions and hashtags symbols but keep the text
        text = re.sub(r'[@#]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text using VADER (lightweight)"""
        # VADER sentiment analysis
        vader_scores = self.vader.polarity_scores(text)
        
        # Use compound score for sentiment classification
        compound_score = vader_scores['compound']
        
        return {
            "vader": compound_score,
            "combined": compound_score,
            "label": "positive" if compound_score > 0.1 else "negative" if compound_score < -0.1 else "neutral"
        }
    
    def categorize_issue(self, text: str) -> Tuple[str, float]:
        """Categorize the issue based on keywords"""
        text_lower = text.lower()
        category_scores = {}
        
        for category, keywords in self.issue_keywords.items():
            score = 0
            for keyword in keywords:
                # Count occurrences of keyword
                count = text_lower.count(keyword.lower())
                score += count
            
            # Normalize by text length
            category_scores[category] = score / len(text.split()) if len(text.split()) > 0 else 0
        
        # Find category with highest score
        if max(category_scores.values()) == 0:
            return "other", 0
        
        best_category = max(category_scores, key=category_scores.get)
        return best_category, category_scores[best_category]
    
    def detect_urgency(self, text: str) -> Tuple[bool, int]:
        """Detect if the text indicates urgency"""
        text_lower = text.lower()
        urgency_count = 0
        
        for keyword in self.urgency_keywords:
            urgency_count += text_lower.count(keyword)
        
        return urgency_count > 0, urgency_count
    
    def analyze_tweets(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze a DataFrame of tweets"""
        results = []
        
        for _, row in df.iterrows():
            text = self.preprocess_text(row['text'])
            
            # Analyze sentiment
            sentiment = self.analyze_sentiment(text)
            
            # Categorize issue
            category, category_score = self.categorize_issue(text)
            
            # Detect urgency
            is_urgent, urgency_count = self.detect_urgency(text)
            
            # Calculate priority score
            priority_score = 0
            if sentiment['label'] == 'negative':
                priority_score += abs(sentiment['combined']) * 10
            
            if is_urgent:
                priority_score += urgency_count * 5
            
            if row['retweet_count'] > 10:
                priority_score += row['retweet_count'] * 0.5
            
            # Determine priority level
            if priority_score > 15:
                priority = "HIGH"
            elif priority_score > 7:
                priority = "MEDIUM"
            else:
                priority = "LOW"
            
            results.append({
                "id": row['id'],
                "text": text,
                "created_at": row['created_at'],
                "user": row['user'],
                "location": row.get('location'),
                "retweet_count": row['retweet_count'],
                "favorite_count": row['favorite_count'],
                "source": row['source'],
                "sentiment": sentiment['label'],
                "sentiment_score": sentiment['combined'],
                "category": category,
                "category_score": category_score,
                "is_urgent": is_urgent,
                "urgency_count": urgency_count,
                "priority_score": priority_score,
                "priority": priority
            })
        
        return pd.DataFrame(results)
    
    def generate_summary(self, df: pd.DataFrame) -> Dict:
        """Generate a summary of the analyzed tweets"""
        # Count by category
        category_counts = df['category'].value_counts().to_dict()
        
        # Count by priority
        priority_counts = df['priority'].value_counts().to_dict()
        
        # Count by sentiment
        sentiment_counts = df['sentiment'].value_counts().to_dict()
        
        # Average sentiment by category
        avg_sentiment_by_category = df.groupby('category')['sentiment_score'].mean().to_dict()
        
        # Urgent issues
        urgent_issues = df[df['is_urgent'] == True].sort_values('priority_score', ascending=False)
        
        # Top trending issues (high volume)
        trending_issues = df.groupby('category').size().sort_values(ascending=False).head(5).index.tolist()
        
        return {
            "total_tweets": len(df),
            "category_counts": category_counts,
            "priority_counts": priority_counts,
            "sentiment_counts": sentiment_counts,
            "avg_sentiment_by_category": avg_sentiment_by_category,
            "urgent_issues": urgent_issues[['text', 'category', 'priority_score']].head(10).to_dict('records'),
            "trending_issues": trending_issues,
            "timestamp": datetime.now().isoformat()
        }