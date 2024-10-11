import streamlit as st
import pandas as pd
import subprocess
import threading
import os
from streamlit_autorefresh import st_autorefresh

st.title("Real-Time Keyword Trend and Sentiment Analysis")

def start_runpy():
    subprocess.Popen(['python', 'run.py'])

if 'runpy_started' not in st.session_state:
    threading.Thread(target=start_runpy, daemon=True).start()
    st.session_state['runpy_started'] = True

st_autorefresh(interval=60000, key="keyword_analysis_refresh")

def load_data():
    if os.path.exists('data.csv'):
        df = pd.read_csv('data.csv')
        return df
    else:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    top_keywords = df

    st.subheader("Top Trending Keywords")
    st.table(top_keywords)

    st.subheader("Popularity Score Chart")
    st.bar_chart(top_keywords.set_index('Keyword'))
else:
    st.write("Waiting for data...")
