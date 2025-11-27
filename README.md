# Public Sentiment Early Warning System (PSEWS)

A comprehensive dashboard for monitoring public sentiment and community concerns from social media platforms (Twitter and Reddit) with advanced analytics and early warning capabilities.

## Features

- **Real-time Data Collection**: Gather posts from Twitter and Reddit APIs
- **Advanced Sentiment Analysis**: Using VADER and Hugging Face transformers
- **Issue Categorization**: Automatic classification of community concerns
- **Priority Assessment**: High/Medium/Low priority scoring with urgency detection
- **Interactive Visualizations**: Comprehensive charts and analytics dashboard
- **Simulation Fallback**: Realistic synthetic data when APIs are unavailable
- **Export Capabilities**: CSV export functionality

## Local Development

### Prerequisites

- Python 3.11+
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd publicsystem
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download NLTK data:
```python
import nltk
nltk.download('vader_lexicon')
```

### Configuration

Create a `.env` file in the root directory with your API credentials:

```env
# Twitter API (v2)
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here

# Reddit API
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=your_app_name/1.0
```

### Running Locally

```bash
streamlit run main.py
```

The dashboard will be available at `http://localhost:8501`

## Deployment to Render

### Method 1: Using render.yaml (Recommended)

1. **Connect Repository**: Link your GitHub/GitLab repository to Render

2. **Deploy Service**:
   - Go to Render Dashboard → New → Web Service
   - Connect your repository
   - Service will auto-detect `render.yaml` configuration

3. **Environment Variables**: Add your API credentials in Render's environment settings:
   - `TWITTER_BEARER_TOKEN`
   - `REDDIT_CLIENT_ID`
   - `REDDIT_CLIENT_SECRET`
   - `REDDIT_USER_AGENT`

4. **Deploy**: Click "Create Web Service" - Render will handle the rest!

### Method 2: Manual Configuration

If `render.yaml` doesn't work:

1. **Create Web Service** on Render
2. **Runtime**: Python 3.11
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `streamlit run main.py --server.port $PORT --server.headless true --server.runOnSave false`

## Project Structure

```
publicsystem/
├── main.py                 # Main Streamlit application
├── data_manager.py         # Data collection from APIs
├── issue_analyzer.py       # Sentiment analysis and categorization
├── visualizer.py           # Chart generation and visualization
├── social_simulator.py     # Synthetic data generation
├── requirements.txt        # Python dependencies
├── render.yaml            # Render deployment configuration
├── .env                   # Environment variables (local only)
└── README.md              # This file
```

## API Configuration

### Twitter API (v2)
1. Apply for Twitter Developer Account
2. Create a Project/App
3. Get Bearer Token from API Keys section

### Reddit API
1. Go to https://www.reddit.com/prefs/apps
2. Create a "script" application
3. Note down Client ID and Secret

## Usage

1. **Data Collection**: Enter location and select number of posts
2. **Analysis**: System automatically analyzes sentiment and categorizes issues
3. **Visualization**: Explore interactive charts and insights
4. **Export**: Download analyzed data as CSV

## Features Overview

- **Multi-platform Support**: Twitter and Reddit integration
- **Advanced NLP**: Transformer-based sentiment analysis
- **Real-time Monitoring**: Live data collection and analysis
- **Priority Scoring**: Automated urgency and priority assessment
- **Interactive Dashboard**: Comprehensive visualization suite
- **Simulation Mode**: Realistic fallback data generation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues or questions:
- Check the troubleshooting section below
- Open an issue on GitHub
- Review the code documentation

## Troubleshooting

### Common Issues

1. **API Rate Limits**: Twitter/Reddit may limit requests
2. **Missing Dependencies**: Ensure all packages are installed
3. **Environment Variables**: Check `.env` file configuration
4. **Port Issues**: Render uses dynamic ports

### Performance Tips

- Use simulation mode for testing without API calls
- Adjust post limits based on API quotas
- Monitor memory usage with large datasets

---

**Built with ❤️ for community monitoring and early warning systems**