# Use a lightweight Python base image
FROM python:3.11-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# Create and set app directory
WORKDIR /app
# Copy application files
COPY . /app
# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Expose the app port
EXPOSE 5003
# Run the application
CMD ["python", "app.py"]
