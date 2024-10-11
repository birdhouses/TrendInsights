# run.py

import pandas as pd
import numpy as np
import feedparser
from pytrends.request import TrendReq
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.preprocessing import MinMaxScaler
import string
import time

nltk.download('vader_lexicon', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger')

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter

stop_words = set(stopwords.words('english'))
custom_stop_words = set([
    'font', 'http', 'https', 'www', 'com', 'nbsp', 'li', 'ol', 'ul', 'br', 'amp', 'gt', 'lt',
    'style', 'class', 'id', 'div', 'span', 'src', 'href', 'img', 'alt', 'px', 'em', 'strong',
    'blockquote', 'code', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'script', 'rel', 'type',
    'meta', 'link', 'stylesheet', 'css', 'js', 'data', 'function', 'var', 'let', 'const',
    'new', 'time', 'one', 'would', 'could', 'us', 'said', 'also', 'first', 'last', 'say',
    'may', 'like', 'get', 'go', 'know', 'year', 'make', 'see', 'back', 'people', 'cnn', 'york', 'time'
    'post', 'washington', 'time', 'video', 'today', 'news', 'reuters'
])

stop_words.update(custom_stop_words)

exclude_punct = set(string.punctuation)
lemmatizer = WordNetLemmatizer()

pytrends = TrendReq(hl='en-US', tz=360, retries=5, timeout=(10,25), backoff_factor=0.1, requests_args={'verify':False})

rss_urls = [
    'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en',
    'http://feeds.bbci.co.uk/news/rss.xml',
    'https://rss.cnn.com/rss/edition.rss',
    'https://feeds.npr.org/1001/rss.xml'
]

def collect_data():
    while True:
        text_data = ''
        for url in rss_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                text_data += ' ' + entry.title + ' ' + entry.description

        tokens = word_tokenize(text_data)
        pos_tags = nltk.pos_tag(tokens)
        cleaned_tokens = [
            lemmatizer.lemmatize(token.lower()) for token, pos in pos_tags
            if token.lower() not in stop_words and
            token.lower() not in exclude_punct and
            token.isalpha() and
            len(token) > 2 and
            pos.startswith('NN')
        ]

        word_freq = Counter(cleaned_tokens)
        most_common_words = [word for word, freq in word_freq.most_common(20)]

        timeframe = 'now 1-d'
        keyword_data = []

        for i in range(0, len(most_common_words), 5):
            time.sleep(10)
            keywords_batch = most_common_words[i:i+5]
            pytrends.build_payload(keywords_batch, timeframe=timeframe)
            trends_data = pytrends.interest_over_time()
            if trends_data.empty:
                continue
            for keyword in keywords_batch:
                if keyword not in trends_data.columns:
                    continue
                trend = trends_data[keyword]
                if trend.empty or trend.sum() == 0:
                    continue
                current_interest = trend.iloc[-1]
                average_interest = trend.mean()
                if trend.iloc[0] == 0:
                    trend_velocity = 0
                else:
                    trend_velocity = (current_interest - trend.iloc[0]) / trend.iloc[0]
                sia = SentimentIntensityAnalyzer()
                relevant_texts = [entry.title + ' ' + entry.description for url in rss_urls for entry in feedparser.parse(url).entries if keyword in (entry.title.lower() + ' ' + entry.description.lower())]
                sentiments = [sia.polarity_scores(text)['compound'] for text in relevant_texts]
                if sentiments:
                    average_sentiment = sum(sentiments) / len(sentiments)
                else:
                    average_sentiment = 0
                keyword_info = {
                    'Keyword': keyword,
                    'Frequency': word_freq[keyword],
                    'Current Interest': current_interest,
                    'Average Interest': average_interest,
                    'Trend Velocity': trend_velocity,
                    'Average Sentiment': average_sentiment,
                }
                keyword_data.append(keyword_info)

        df = pd.DataFrame(keyword_data)

        if not df.empty:
            scaler = MinMaxScaler()
            df[['Frequency', 'Current Interest', 'Average Interest', 'Trend Velocity', 'Average Sentiment']] = scaler.fit_transform(
                df[['Frequency', 'Current Interest', 'Average Interest', 'Trend Velocity', 'Average Sentiment']]
            )

            df['Popularity Score'] = (
                df['Frequency'] * 0.2 +
                df['Current Interest'] * 0.2 +
                df['Average Interest'] * 0.2 +
                df['Trend Velocity'] * 0.2 +
                df['Average Sentiment'] * 0.2
            )

            df = df.sort_values(by='Popularity Score', ascending=False)
            df.to_csv('data.csv', index=False)

        time.sleep(300)  # Wait for 5 minutes before next update

if __name__ == '__main__':
    collect_data()
