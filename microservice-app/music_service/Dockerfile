# Use lightweight Python image
FROM python:3.11-slim

# Set environment variables to avoid issues with pygame audio in container
ENV SDL_AUDIODRIVER=dummy
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install OS dependencies for pygame
RUN apt-get update && apt-get install -y \
    libsdl2-mixer-2.0-0 \
    libsdl2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create upload folder inside container
RUN mkdir -p music_files

# Expose port
EXPOSE 5004

# Start the app
CMD ["python", "app.py"]
