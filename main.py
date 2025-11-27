import os
import pandas as pd
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv

# Import our modules
from data_manager import DataManager
from issue_analyzer import IssueAnalyzer
from visualizer import IssueVisualizer

# Load environment variables
load_dotenv()

class SentimentEarlyWarningSystem:
    def __init__(self):
        """Initialize the system"""
        # Initialize components
        self.data_manager = DataManager()
        self.analyzer = IssueAnalyzer()
        self.visualizer = IssueVisualizer()
        
        # Initialize session state
        if 'data' not in st.session_state:
            st.session_state.data = None
        if 'summary' not in st.session_state:
            st.session_state.summary = None
        if 'source' not in st.session_state:
            st.session_state.source = None
    
    def collect_data(self, location: str, max_posts: int):
        """Collect and analyze social media data"""
        with st.spinner("Collecting data..."):
            try:
                # Collect tweets/posts using the data manager
                raw_df, source = self.data_manager.collect_data(location, max_posts)
                
                if raw_df.empty or raw_df is None:
                    st.error("Failed to collect data from both Twitter and Reddit. Using emergency simulation data.")
                    # Create minimal emergency data
                    import pandas as pd
                    from datetime import datetime
                    emergency_data = []
                    for i in range(min(max_posts, 3)):
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
                    raw_df = pd.DataFrame(emergency_data)
                    source = "Emergency Simulation"
                
                # Analyze the collected data
                with st.spinner("Analyzing content..."):
                    analyzed_df = self.analyzer.analyze_tweets(raw_df)
                    
                    # Generate summary
                    summary = self.analyzer.generate_summary(analyzed_df)
                    
                    # Store in session state
                    st.session_state.data = analyzed_df
                    st.session_state.summary = summary
                    st.session_state.source = source
                    
            except Exception as e:
                st.error(f"Data collection failed: {str(e)}. Using emergency simulation data.")
                # Create emergency fallback data
                import pandas as pd
                from datetime import datetime
                emergency_data = []
                for i in range(3):
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
                
                raw_df = pd.DataFrame(emergency_data)
                analyzed_df = self.analyzer.analyze_tweets(raw_df)
                summary = self.analyzer.generate_summary(analyzed_df)
                
                st.session_state.data = analyzed_df
                st.session_state.summary = summary
                st.session_state.source = "Emergency Simulation"
    
    def run_dashboard(self):
        """Run the Streamlit dashboard"""
        st.set_page_config(layout="wide")
        st.title("PSEWS")
        st.markdown("Detect community concerns early from public discussions on Twitter and Reddit.")
        
        # Sidebar for controls
        st.sidebar.header("Controls")
        
        # Data collection controls
        st.sidebar.subheader("Data Collection")
        location = st.sidebar.text_input("Location (used for Twitter)", "Nairobi")
        max_posts = st.sidebar.slider("Maximum posts per category", 5, 30, 15)  # Reduced default and max
        
        # Collect data button
        if st.sidebar.button("Collect Data"):
            self.collect_data(location, max_posts)
        
        # Display data source
        if st.session_state.source:
            st.sidebar.info(f"Data Source: **{st.session_state.source}**")

        # Check if data is available
        if st.session_state.data is None or st.session_state.data.empty:
            st.info("No data available. Please collect data first.")
            return
        
        # Display summary
        st.header("Summary")
        summary = st.session_state.summary
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Issues", summary['total_tweets'])
        col2.metric("High Priority Issues", summary['priority_counts'].get('HIGH', 0))
        col3.metric("Urgent Issues", len(summary['urgent_issues']))
        
        # Overview Section - Main Dashboard
        with st.container():
            st.subheader("📊 Overview Dashboard")
            col1, col2 = st.columns(2)
            with col1:
                fig = self.visualizer.create_category_bar_chart(st.session_state.data)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = self.visualizer.create_priority_pie_chart(st.session_state.data)
                st.plotly_chart(fig, use_container_width=True)
            
            # Simple sentiment overview
            st.markdown("**Sentiment Overview**")
            sentiment_counts = st.session_state.data['sentiment'].value_counts()
            st.bar_chart(sentiment_counts)
        
        # Analysis Section - Combined Category and Priority Analysis
        with st.container():
            st.subheader("🔍 Detailed Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Sentiment by Category**")
                fig = self.visualizer.create_sentiment_by_category(st.session_state.data)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.markdown("**Priority Distribution**")
                priority_counts = st.session_state.data['priority'].value_counts()
                st.bar_chart(priority_counts)
        
        # Trends Section
        with st.container():
            st.subheader("📈 Trends & Platform Analysis")
            # Platform and category stats side by side
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Platform Distribution**")
                platform_counts = st.session_state.data['source'].value_counts()
                st.bar_chart(platform_counts)
            with col2:
                st.markdown("**Top Categories**")
                top_categories = st.session_state.data['category'].value_counts().head(5)
                st.bar_chart(top_categories)
        
        # Urgent Issues Section
        with st.container():
            st.subheader("🚨 Urgent Issues")
            urgent_df = pd.DataFrame(summary['urgent_issues'])
            if not urgent_df.empty:
                st.dataframe(urgent_df, use_container_width=True)
            else:
                st.info("No urgent issues detected.")
        
        # Findings Section - More compact
        with st.container():
            st.subheader("🔍 Key Findings & Actions")
            
            # Calculate key insights
            total_issues = len(st.session_state.data)
            high_priority = summary['priority_counts'].get('HIGH', 0)
            urgent_count = len(summary['urgent_issues'])
            negative_sentiment = (st.session_state.data['sentiment'] == 'negative').sum()
            top_category = st.session_state.data['category'].value_counts().index[0]
            
            # Display findings in a more compact format
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("High Priority Issues", high_priority)
                st.metric("Urgent Issues", urgent_count)
            with col2:
                st.metric("Negative Sentiment", f"{negative_sentiment}/{total_issues}")
                st.metric("Top Category", top_category.replace('_', ' ').title())
            with col3:
                st.markdown("**Quick Actions:**")
                if urgent_count > 0:
                    st.error("⚡ Review urgent issues immediately")
                if high_priority > 0:
                    st.warning("🚨 Address high priority issues within 24h")
                if negative_sentiment > total_issues * 0.3:
                    st.info("😞 Investigate negative sentiment causes")
        
        # Download data
        st.sidebar.subheader("Export")
        if st.sidebar.button("Download Data as CSV"):
            csv = st.session_state.data.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"sentiment_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# Run the application
if __name__ == "__main__":
    app = SentimentEarlyWarningSystem()
    app.run_dashboard()