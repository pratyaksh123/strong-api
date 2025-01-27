# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Pipenv
RUN apt-get update && apt-get install -y python3-pip python3-dev && \
    pip install --no-cache-dir pipenv

# Copy project files (but not .env due to .dockerignore)
COPY . .

# Set Flask environment variables
ENV FLASK_APP=server.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Install dependencies in a virtual environment
RUN pipenv install --deploy --ignore-pipfile

# Expose Flask port
EXPOSE 5000

# Run Flask with Gunicorn
CMD ["pipenv", "run", "gunicorn", "-b", "0.0.0.0:5000", "server:app"]
