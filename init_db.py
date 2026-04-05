import sqlite3

conn = sqlite3.connect('trends.db')
cursor = conn.cursor()

# Create a table to store the ticker, sentiment, and exact time it was mentioned
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ticker_mentions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT,
        sentiment REAL,
        source_url TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()
