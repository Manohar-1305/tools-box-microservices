# Use a lightweight Python base image
FROM python:3.10-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Install OS-level dependencies (ffmpeg required by yt-dlp)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Create app directory
WORKDIR /app
# Copy requirement file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy app code
COPY . .
# Create downloads directory
RUN mkdir -p downloads
# Expose Flask port
EXPOSE 5002
# Run the Flask app
CMD ["python", "app.py"]
