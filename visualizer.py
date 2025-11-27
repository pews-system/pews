import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class IssueVisualizer:
    def __init__(self):
        """Initialize the visualizer with style settings"""
        plt.style.use('ggplot')
        sns.set_palette("viridis")
    
    def create_category_bar_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create a bar chart showing the distribution of issues by category"""
        category_counts = df['category'].value_counts().reset_index()
        category_counts.columns = ['category', 'count']
        
        fig = px.bar(
            category_counts, 
            x='category', 
            y='count',
            title='Issues by Category',
            color='count',
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            xaxis_title="Category",
            yaxis_title="Number of Issues",
            height=500
        )
        
        return fig
    
    def create_sentiment_scatter(self, df: pd.DataFrame) -> go.Figure:
        """Create a scatter plot showing sentiment vs. urgency by category"""
        # Filter to only include negative sentiment for clearer visualization
        df_filtered = df[df['sentiment'] == 'negative'].copy()
        
        # Create size based on retweet count
        df_filtered['size'] = np.log1p(df_filtered['retweet_count']) * 5
        
        fig = px.scatter(
            df_filtered,
            x='urgency_count',
            y='sentiment_score',
            color='category',
            size='size',
            hover_data=['text'],
            title='Sentiment vs. Urgency by Category',
            labels={
                'sentiment_score': 'Sentiment Score (More Negative = Lower)',
                'urgency_count': 'Urgency Indicators Count',
                'size': 'Retweet Count (log scale)'
            }
        )
        
        fig.update_layout(
            height=600
        )
        
        return fig
    
    def create_priority_pie_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create a pie chart showing the distribution of priorities"""
        priority_counts = df['priority'].value_counts().reset_index()
        priority_counts.columns = ['priority', 'count']
        
        # Define colors for priorities
        colors = {
            'HIGH': 'red',
            'MEDIUM': 'orange',
            'LOW': 'green'
        }
        
        fig = px.pie(
            priority_counts,
            values='count',
            names='priority',
            title='Distribution of Issue Priorities',
            color='priority',
            color_discrete_map=colors
        )
        
        fig.update_layout(height=500)
        
        return fig
    
    def create_trend_line_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create a line chart showing trends over time"""
        # Convert created_at to datetime if it's not already
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Group by date and category
        df['date'] = df['created_at'].dt.date
        trend_data = df.groupby(['date', 'category']).size().reset_index(name='count')
        
        fig = px.line(
            trend_data,
            x='date',
            y='count',
            color='category',
            title='Issue Trends Over Time',
            labels={
                'date': 'Date',
                'count': 'Number of Issues'
            }
        )
        
        fig.update_layout(
            height=500,
            xaxis_title="Date",
            yaxis_title="Number of Issues"
        )
        
        return fig
    
    def create_sentiment_by_category(self, df: pd.DataFrame) -> go.Figure:
        """Create a grouped bar chart showing sentiment distribution by category"""
        sentiment_by_category = df.groupby(['category', 'sentiment']).size().reset_index(name='count')
        
        fig = px.bar(
            sentiment_by_category,
            x='category',
            y='count',
            color='sentiment',
            barmode='group',
            title='Sentiment Distribution by Category',
            labels={
                'category': 'Category',
                'count': 'Number of Issues',
                'sentiment': 'Sentiment'
            }
        )
        
        fig.update_layout(
            height=500,
            xaxis_title="Category",
            yaxis_title="Number of Issues"
        )
        
        return fig
    
    def create_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """Create a heatmap showing issues by category and priority"""
        heatmap_data = df.groupby(['category', 'priority']).size().reset_index(name='count')
        
        # Pivot the data for heatmap
        heatmap_pivot = heatmap_data.pivot(index='category', columns='priority', values='count').fillna(0)
        
        fig = px.imshow(
            heatmap_pivot,
            labels=dict(x="Priority", y="Category", color="Count"),
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            title="Issue Distribution by Category and Priority",
            color_continuous_scale="Viridis"
        )
        
        fig.update_layout(height=500)
        
        return fig
    
    def create_dashboard(self, df: pd.DataFrame, save_path: str = None) -> go.Figure:
        """Create a comprehensive dashboard with multiple visualizations"""
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('Issues by Category', 'Sentiment vs. Urgency', 
                          'Priority Distribution', 'Trends Over Time',
                          'Sentiment by Category', 'Issue Heatmap'),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "pie"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "heatmap"}]]
        )
        
        # Get individual figures
        category_fig = self.create_category_bar_chart(df)
        sentiment_fig = self.create_sentiment_scatter(df)
        priority_fig = self.create_priority_pie_chart(df)
        trend_fig = self.create_trend_line_chart(df)
        sentiment_cat_fig = self.create_sentiment_by_category(df)
        heatmap_fig = self.create_heatmap(df)
        
        # Add traces to subplot
        for trace in category_fig.data:
            fig.add_trace(trace, row=1, col=1)
        
        for trace in sentiment_fig.data:
            fig.add_trace(trace, row=1, col=2)
        
        for trace in priority_fig.data:
            fig.add_trace(trace, row=2, col=1)
        
        for trace in trend_fig.data:
            fig.add_trace(trace, row=2, col=2)
        
        for trace in sentiment_cat_fig.data:
            fig.add_trace(trace, row=3, col=1)
        
        for trace in heatmap_fig.data:
            fig.add_trace(trace, row=3, col=2)
        
        # Update layout
        fig.update_layout(
            height=1200,
            width=1200,
            title_text="Public Sentiment Early Warning System Dashboard",
            showlegend=False
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig