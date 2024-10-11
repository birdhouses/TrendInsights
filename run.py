import pandas as pd
import numpy as np
import feedparser
from pytrends.request import TrendReq
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.preprocessing import MinMaxScaler
import string

nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english'))
exclude_punct = set(string.punctuation)
lemmatizer = WordNetLemmatizer()

pytrends = TrendReq(hl='en-US', tz=360, retries=5)

rss_urls = [
    'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en',
    'http://feeds.bbci.co.uk/news/rss.xml',
    'https://rss.cnn.com/rss/edition.rss',
    'https://feeds.npr.org/1001/rss.xml'
]

text_data = ''
for url in rss_urls:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        text_data += ' ' + entry.title + ' ' + entry.description

tokens = word_tokenize(text_data)
cleaned_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens
                  if token.lower() not in stop_words and
                  token.lower() not in exclude_punct and
                  token.isalpha()]

from collections import Counter
word_freq = Counter(cleaned_tokens)
most_common_words = [word for word, freq in word_freq.most_common(50)]

timeframe = 'today 12-m'
keyword_data = []

for i in range(0, len(most_common_words), 5):
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

print(df[['Keyword', 'Popularity Score']])
