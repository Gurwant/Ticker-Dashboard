#!/bin/bash

# 1. Initialize the SQLite database
python init_db.py

# 2. Start the background worker (the '&' runs it in the background)
python worker.py &

# 3. Start the Streamlit Web UI
streamlit run dashboard.py --server.port=8501 --server.address=0.0.0.0
