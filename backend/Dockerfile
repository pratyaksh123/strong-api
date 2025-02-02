# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y python3-pip python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy project files (but not .env due to .dockerignore)
COPY . .

# Set Flask environment variables
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose Heroku's default port
EXPOSE $PORT

# Start Flask server
CMD ["gunicorn", "-w", "4", "-c", "gunicorn_conf.py", "wsgi:app"]