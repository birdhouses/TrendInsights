# Keyword Trend and Sentiment Analysis

This repository contains a Python script that analyzes keyword trends and sentiment from RSS feeds and Google Trends. It collects data from multiple RSS news sources, processes the text to extract the most frequent keywords, and checks the popularity and sentiment trends using Google Trends. The script ranks the keywords based on their frequency, trend velocity, sentiment, and popularity score.

## Features

- Extracts keywords from multiple RSS feeds.
- Performs sentiment analysis using the VADER sentiment analyzer.
- Fetches trend data for keywords from Google Trends.
- Ranks keywords based on frequency, sentiment, and trend data.
- Outputs the most popular and trending keywords.

## Requirements

- Python 3.6+
- Internet connection to fetch data from RSS feeds and Google Trends.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/birdhouses/TrendInsights.git
   cd TrendInsights
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, install the packages manually:

   ```bash
   pip install pandas numpy feedparser pytrends nltk scikit-learn
   ```

3. Download NLTK data:

   ```python
   import nltk
   nltk.download('vader_lexicon')
   nltk.download('stopwords')
   nltk.download('punkt')
   nltk.download('wordnet')
   ```

## Usage

1. Run the script to analyze and rank keywords:

   ```bash
   python3 script.py
   ```

2. The script will output the most popular keywords along with their popularity scores.

## Data Sources

- **RSS Feeds**: The script collects data from the following RSS sources:
  - Google News
  - BBC News
  - CNN
  - NPR

- **Google Trends**: It uses the `pytrends` library to retrieve trend data from Google.

## How It Works

1. The script fetches RSS feed data from multiple sources.
2. It processes the text, removes stop words, punctuation, and lemmatizes the tokens.
3. It calculates keyword frequency and identifies the top 50 most common keywords.
4. For each keyword, the script fetches trend data from Google Trends and performs sentiment analysis on the associated text.
5. Keywords are ranked based on their frequency, trend velocity, average interest, and sentiment score.