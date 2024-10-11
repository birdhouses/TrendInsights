# TrendInsights

TrendInsights is a Python application that analyzes current news trends and sentiments to identify popular keywords and topics. It fetches data from multiple RSS news feeds, processes the text to extract significant keywords, and evaluates their popularity and sentiment using Google Trends and NLTK.

![Screenshot](/assets/image.png)

## Features

- Extracts and processes text data from major news RSS feeds.
- Identifies the most frequent and meaningful keywords.
- Analyzes keyword trends using Google Trends.
- Performs sentiment analysis on keywords using NLTK's VADER.
- Ranks keywords based on frequency, trend velocity, average interest, and sentiment score.

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

Run the script:

```bash
python app.py
```

The script will output a list of keywords with their popularity scores.
