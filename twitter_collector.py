import tweepy
import pandas as pd
import time
from datetime import datetime, timedelta
import os
import json
from typing import List, Dict, Tuple

class TwitterDataCollector:
    def __init__(self, api_key: str, api_secret: str, access_token: str, access_token_secret: str):
        """Initialize Twitter API client"""
        self.auth = tweepy.OAuthHandler(api_key, api_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
        
        # Keywords for different issue categories
        self.issue_keywords = {
            "infrastructure": ["water shortage", "no electricity", "road damage", "bridge", "power outage"],
            "healthcare": ["hospital", "clinic", "medical", "medicine", "healthcare"],
            "safety": ["crime", "accident", "dangerous", "emergency", "police"],
            "social_services": ["welfare", "housing", "food security", "unemployment", "social support"],
            "governance": ["complaint", "service delivery", "government", "municipality", "council"]
        }
        
        # Urgency indicators
        self.urgency_keywords = ["emergency", "urgent", "dying", "dangerous", "critical", "immediate"]
    
    def search_tweets(self, query: str, count: int = 100, location: str = None) -> List[Dict]:
        """Search for tweets matching the query"""
        tweets = []
        
        try:
            # Add location filter if provided
            if location:
                query = f"{query} near:\"{location}\""
            
            # Search tweets
            results = self.api.search_tweets(
                q=query,
                count=count,
                tweet_mode="extended",
                lang="en",
                include_entities=False
            )
            
            for tweet in results:
                tweets.append({
                    "id": tweet.id_str,
                    "text": tweet.full_text,
                    "created_at": tweet.created_at.isoformat(),
                    "user": tweet.user.screen_name,
                    "retweet_count": tweet.retweet_count,
                    "favorite_count": tweet.favorite_count,
                    "location": tweet.user.location if hasattr(tweet.user, "location") else None
                })
                
        except Exception as e:
            print(f"Error searching tweets: {e}")
            
        return tweets
    
    def collect_issue_tweets(self, location: str = None, max_tweets_per_category: int = 50) -> pd.DataFrame:
        """Collect tweets related to all issue categories"""
        all_tweets = []
        
        for category, keywords in self.issue_keywords.items():
            for keyword in keywords:
                tweets = self.search_tweets(keyword, max_tweets_per_category, location)
                
                for tweet in tweets:
                    tweet["category"] = category
                    tweet["keyword"] = keyword
                    all_tweets.append(tweet)
                
                # Rate limiting
                time.sleep(1)
        
        return pd.DataFrame(all_tweets)
    
    def save_tweets(self, df: pd.DataFrame, filename: str = None) -> str:
        """Save tweets to a JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tweets_{timestamp}.json"
        
        df.to_json(filename, orient="records", date_format="iso")
        return filename