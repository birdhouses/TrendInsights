# TrendInsights

TrendInsights is a Python application that analyzes current news trends and sentiments to identify popular keywords and topics. It features a Streamlit web interface that updates automatically and displays trending keywords in real-time.

## Features

- **Real-Time Updates**: Streamlit interface that refreshes to show the latest trending keywords.
- **Data Sources**: Extracts and processes text data from major news RSS feeds.
- **Trend Analysis**: Uses Google Trends to analyze keyword popularity.
- **Sentiment Analysis**: Performs sentiment analysis using NLTK's VADER.
- **Keyword Ranking**: Ranks keywords based on frequency, trend velocity, average interest, and sentiment score.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/birdhouses/TrendInsights.git
   cd TrendInsights
   ```

2. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data:**

   ```python
   import nltk
   nltk.download('vader_lexicon')
   nltk.download('stopwords')
   nltk.download('punkt')
   nltk.download('wordnet')
   nltk.download('averaged_perceptron_tagger')
   ```

## Usage

1. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

2. **View the app:**

   Open the URL provided by Streamlit (usually `http://localhost:8501`) in your web browser to view the live dashboard.
