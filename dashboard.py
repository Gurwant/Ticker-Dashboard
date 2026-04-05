import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Ticker Trends", layout="wide")
st.title("📈 Reddit Stock Trends")

# Connect to the DB
conn = sqlite3.connect('trends.db')

# Query for the last 24 hours
query_24h = """
    SELECT ticker, COUNT(*) as mentions, AVG(sentiment) as avg_sentiment
    FROM ticker_mentions 
    WHERE timestamp >= datetime('now', '-1 day')
    GROUP BY ticker 
    ORDER BY mentions DESC 
    LIMIT 10
"""
df_24h = pd.read_sql_query(query_24h, conn)

# Query for the last 7 days
query_7d = """
    SELECT ticker, COUNT(*) as mentions, AVG(sentiment) as avg_sentiment
    FROM ticker_mentions 
    WHERE timestamp >= datetime('now', '-7 days')
    GROUP BY ticker 
    ORDER BY mentions DESC 
    LIMIT 10
"""
df_7d = pd.read_sql_query(query_7d, conn)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Top 10 Tickers (Last 24 Hours)")
    st.dataframe(df_24h, use_container_width=True)
    if not df_24h.empty:
        st.bar_chart(df_24h.set_index('ticker')['mentions'])

with col2:
    st.subheader("📅 Top 10 Tickers (Last 7 Days)")
    st.dataframe(df_7d, use_container_width=True)
    if not df_7d.empty:
        st.bar_chart(df_7d.set_index('ticker')['mentions'])

conn.close()
