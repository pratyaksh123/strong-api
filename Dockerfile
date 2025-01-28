# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for cron and pipenv
RUN apt-get update && apt-get install -y cron python3-pip python3-dev && \
    pip install --no-cache-dir pipenv && \
    apt-get clean

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

# Copy custom entrypoint script
COPY custom_entrypoint.sh /usr/local/bin/custom_entrypoint.sh
RUN chmod +x /usr/local/bin/custom_entrypoint.sh

# Ensure cron logs exist
RUN touch /var/log/cron.log

# Create cron job file (sources exported env file before execution)
RUN echo "0 0 * * * root . /etc/environment && cd /app && pipenv run python api.py >> /var/log/cron.log 2>&1" > /etc/cron.d/fetch_data

# Apply cron job
RUN chmod 0644 /etc/cron.d/fetch_data && crontab /etc/cron.d/fetch_data

# Set entrypoint to export environment variables before running CMD
ENTRYPOINT ["/usr/local/bin/custom_entrypoint.sh"]

# Start cron service & Flask server
CMD cron && pipenv run gunicorn -w 4 -b 0.0.0.0:5000 server:app