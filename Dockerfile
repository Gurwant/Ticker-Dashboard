# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your requirements first (for better Docker caching)
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Make the startup script executable
RUN chmod +x start.sh

# Expose the port Streamlit uses for the Web UI
EXPOSE 8501

# Command to run when the container starts
CMD ["./start.sh"]
