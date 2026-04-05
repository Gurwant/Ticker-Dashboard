import praw
import sqlite3
import time
import json
from ollama import Client

# 1. Connect to your remote Ollama server
ollama_client = Client(host='http://192.168.1.29:11434')

# 2. Setup Reddit API (You need to get these keys from reddit.com/prefs/apps)
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="TrendTracker script by /u/yourusername"
)

def process_posts():
    conn = sqlite3.connect('trends.db')
    cursor = conn.cursor()
    
    # Grab new posts from wallstreetbets
    for submission in reddit.subreddit('wallstreetbets').new(limit=10):
        text_to_analyze = f"Title: {submission.title}\nBody: {submission.selftext}"
        
        prompt = f"""
        Extract any stock tickers mentioned in the text. 
        Format your response EXACTLY as a JSON array of objects with keys "ticker" and "sentiment" (-1.0 to 1.0).
        If none, return [].
        Text: {text_to_analyze}
        """
        
        try:
            # 3. Ask your remote server to process it
            response = ollama_client.generate(model='llama3:8b', prompt=prompt)
            data = json.loads(response['response'])
            
            # 4. Save to database
            for item in data:
                cursor.execute('''
                    INSERT INTO ticker_mentions (ticker, sentiment, source_url)
                    VALUES (?, ?, ?)
                ''', (item['ticker'].upper(), item['sentiment'], submission.url))
            
            conn.commit()
        except Exception as e:
            print(f"Error processing {submission.id}: {e}")

    conn.close()

# Run it every 15 minutes
while True:
    print("Fetching new data...")
    process_posts()
    time.sleep(900)
