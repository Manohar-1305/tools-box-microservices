# Use a lightweight Python base image
FROM python:3.11-slim
# Set working directory
WORKDIR /app
# Install system dependencies (for requests, Flask, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# Copy app source code
COPY . .
# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Expose port
EXPOSE 5000
# Start the Flask app
CMD ["python", "app.py"]
