# Use an official lightweight Python image.
FROM python:3.11-slim

# Install system dependencies (FFmpeg is crucial for yt-dlp)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirement file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8000

# Command to run the application
# We use host 0.0.0.0 to allow external access
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
