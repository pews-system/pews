import os
import pandas as pd
import time
import tweepy
import praw
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st

# Import simulation module
from social_simulator import SocialMediaSimulator

# Load environment variables
load_dotenv()

class DataManager:
    """
    Manages data collection from multiple sources (Twitter, Reddit).
    Tries Twitter first, falls back to Reddit, then to simulation data.
    """
    def __init__(self):
        # Initialize simulation fallback
        self.simulator = SocialMediaSimulator()
        
        # Initialize Twitter client (v2)
        self.twitter_client = None
        try:
            bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
            if bearer_token:
                self.twitter_client = tweepy.Client(bearer_token=bearer_token)
                print("Twitter client initialized successfully.")
            else:
                print("TWITTER_BEARER_TOKEN not found in .env file. Twitter will be skipped.")
        except Exception as e:
            print(f"Could not initialize Twitter client: {e}")
        # Initialize Reddit client
        self.reddit_client = None
        try:
            client_id = os.getenv("REDDIT_CLIENT_ID")
            client_secret = os.getenv("REDDIT_CLIENT_SECRET")
            user_agent = os.getenv("REDDIT_USER_AGENT")

            if client_id and client_secret and user_agent:
                self.reddit_client = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent
                )
                # Test connection by accessing a read-only attribute
                if self.reddit_client.read_only:
                    print("Reddit client initialized successfully.")
            else:
                print("One or more Reddit credentials not found. Reddit will be skipped.")
        except Exception as e:
            print(f"Could not initialize Reddit client: {e}")
        # Keywords for different issue categories (common for both platforms)
        self.issue_keywords = {
            "infrastructure": ["water shortage", "power outage", "road damage", "bridge collapse"],
            "healthcare": ["hospital", "clinic", "medical", "medicine", "healthcare"],
            "safety": ["crime", "accident", "dangerous", "emergency", "police"],
            "social_services": ["welfare", "housing", "food security", "unemployment"],
            "governance": ["complaint", "service delivery", "government", "municipality"]
        }
        
        # Mapping from data_manager categories to simulator categories
        self.category_mapping = {
            "infrastructure": "roads_infrastructure",
            "healthcare": "healthcare_facilities", 
            "safety": "security_crime",
            "social_services": "housing",
            "governance": "corruption"
        }

    def _normalize_twitter_data(self, tweets_data):
        """Converts raw Twitter data to a unified DataFrame format."""
        normalized = []
        for tweet in tweets_data:
            normalized.append({
                "id": tweet["id"],
                "text": tweet["text"],
                "created_at": tweet["created_at"],
                "user": tweet["user"],
                "retweet_count": tweet["retweet_count"],
                "favorite_count": tweet["favorite_count"],
                "location": tweet.get("location"),
                "source": "Twitter"
            })
        return pd.DataFrame(normalized)

    def _normalize_reddit_data(self, posts_data):
        """Converts raw Reddit data to a unified DataFrame format."""
        normalized = []
        for post in posts_data:
            # Use score as a proxy for retweets, comments for favorites
            normalized.append({
                "id": post["id"],
                "text": post["text"],
                "created_at": post["created_at"],
                "user": post["user"],
                "retweet_count": post["score"],
                "favorite_count": post["num_comments"],
                "location": None,
                "source": "Reddit"
            })
        return pd.DataFrame(normalized)

    def _collect_from_twitter(self, location: str, max_posts: int):
        """Collects data from Twitter API v2."""
        if not self.twitter_client:
            raise ConnectionError("Twitter client not initialized.")
        
        all_posts = []
        for category, keywords in self.issue_keywords.items():
            for keyword in keywords:
                try:
                    response = self.twitter_client.search_recent_tweets(
                        query=keyword,
                        max_results=min(100, max_posts // len(self.issue_keywords)),
                        tweet_fields=["created_at", "public_metrics", "author_id", "geo"],
                        user_fields=["username", "location"],
                        expansions=["author_id", "geo.place_id"]
                    )
                    
                    if response.data:
                        users = {user["id"]: user for user in response.includes.get("users", [])}
                        for tweet in response.data:
                            user = users.get(tweet.author_id, {})
                            all_posts.append({
                                "id": tweet.id,
                                "text": tweet.text,
                                "created_at": tweet.created_at.isoformat(),
                                "user": user.get("username", ""),
                                "retweet_count": tweet.public_metrics.get("retweet_count", 0),
                                "favorite_count": tweet.public_metrics.get("like_count", 0),
                                "location": user.get("location"),
                                "category": category
                            })
                except Exception as e:
                    print(f"Error collecting from Twitter for keyword '{keyword}': {e}")
                time.sleep(1)
        return self._normalize_twitter_data(all_posts)

    def _collect_from_reddit(self, location: str, max_posts: int):
        """Collects data from Reddit API."""
        if not self.reddit_client:
            raise ConnectionError("Reddit client not initialized.")
            
        all_posts = []
        for category, keywords in self.issue_keywords.items():
            for keyword in keywords:
                try:
                    search_results = self.reddit_client.subreddit("all").search(
                        keyword, 
                        limit=max_posts // len(self.issue_keywords)
                    )
                    for post in search_results:
                        all_posts.append({
                            "id": post.id,
                            "text": f"{post.title}. {post.selftext}",
                            "created_at": datetime.fromtimestamp(post.created_utc).isoformat(),
                            "user": post.author.name if post.author else "[deleted]",
                            "score": post.score,
                            "num_comments": post.num_comments,
                            "category": category
                        })
                except Exception as e:
                    print(f"Error collecting from Reddit for keyword '{keyword}': {e}")
                time.sleep(2)
        return self._normalize_reddit_data(all_posts)

    def _generate_simulation_data(self, location: str, max_posts: int):
        """Generate simulation data as fallback."""
        print("\n🎭 Using simulation data (API sources unavailable)")
        print(f"Generating {max_posts} realistic posts for {location}...")
        
        try:
            # Generate base simulation
            df = self.simulator.generate_simulation_data(
                num_posts=max_posts,
                location=location,
                days_back=7
            )
            
            # Add trending issue for realism (30% of the time)
            import random
            if random.random() < 0.3:
                trending_category = random.choice(list(self.issue_keywords.keys()))
                simulator_category = self.category_mapping.get(trending_category, trending_category)
                print(f"Adding trending {trending_category} issue (mapped to {simulator_category})...")
                
                try:
                    df = self.simulator.add_trending_issue(
                        df, 
                        category=simulator_category, 
                        num_related_posts=int(max_posts * 0.15)
                    )
                    print("Trending issue added successfully.")
                except Exception as trend_error:
                    print(f"Could not add trending issue ({trend_error}), continuing with base simulation...")
            
            return df
            
        except Exception as e:
            print(f"Simulation generation failed: {e}")
            # Create minimal fallback data
            print("Creating minimal fallback simulation data...")
            fallback_data = []
            for i in range(min(max_posts, 10)):  # At least 10 posts minimum
                fallback_data.append({
                    "id": f"fallback_{i}",
                    "text": f"Community issue reported in {location}. Service delivery concerns.",
                    "created_at": datetime.now().isoformat(),
                    "user": "CommunityMember",
                    "retweet_count": random.randint(1, 20),
                    "favorite_count": random.randint(5, 50),
                    "location": location,
                    "source": "Simulation",
                    "category": "governance"
                })
            return pd.DataFrame(fallback_data)

    def collect_data(self, location: str, max_posts: int):
        """
        Attempts to collect data from Twitter, falls back to Reddit, 
        then to simulation data if both fail.
        Returns a tuple of (dataframe, source_name).
        """
        # Try Twitter first
        if self.twitter_client:
            print("\nAttempting to collect data from Twitter...")
            try:
                df = self._collect_from_twitter(location, max_posts)
                if not df.empty:
                    print(f"Successfully collected {len(df)} posts from Twitter.")
                    return df, "Twitter"
            except Exception as e:
                print(f"Twitter collection failed: {e}")
        else:
            print("\nSkipping Twitter (client not initialized).")
        
        # Try Reddit second
        if self.reddit_client:
            print("\nAttempting to collect data from Reddit...")
            try:
                df = self._collect_from_reddit(location, max_posts)
                if not df.empty:
                    print(f"Successfully collected {len(df)} posts from Reddit.")
                    return df, "Reddit"
            except Exception as e:
                print(f"Reddit collection also failed: {e}")
        else:
            print("\nSkipping Reddit (client not initialized).")

        # Fall back to simulation
        print("\nBoth API sources failed or unavailable.")
        print("Generating simulation data as fallback...")
        
        try:
            df = self._generate_simulation_data(location, max_posts)
            if not df.empty:
                print(f"Generated {len(df)} simulated posts.")
                
                # Show warning in Streamlit if available
                try:
                    st.warning(
                        "**Using Simulated Data**: API sources are unavailable. "
                        "Displaying realistic simulation data for demonstration purposes. "
                        "To use real data, please configure API credentials."
                    )
                except:
                    pass
                
                return df, "Simulation"
            else:
                raise Exception("Generated DataFrame is empty")
                
        except Exception as e:
            print(f"Simulation generation failed: {e}")
            print("Creating emergency fallback data...")
            
            # Emergency fallback - create minimal working data
            emergency_data = []
            for i in range(min(max_posts, 5)):  # At least 5 posts
                emergency_data.append({
                    "id": f"emergency_{i}",
                    "text": f"Community concern in {location}. Local service delivery issue reported.",
                    "created_at": datetime.now().isoformat(),
                    "user": "LocalResident",
                    "retweet_count": 1,
                    "favorite_count": 5,
                    "location": location,
                    "source": "Emergency Simulation",
                    "category": "governance"
                })
            
            df = pd.DataFrame(emergency_data)
            print(f"Created {len(df)} emergency fallback posts.")
            
            try:
                st.warning(
                    "**Emergency Fallback Data**: All data sources failed. "
                    "Using minimal simulation data. Please check API credentials."
                )
            except:
                pass
            
            return df, "Emergency Simulation"