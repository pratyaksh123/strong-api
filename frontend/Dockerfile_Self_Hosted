# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for pipenv
RUN apt-get update && apt-get install -y python3-pip python3-dev && \
    pip install --no-cache-dir pipenv && \
    apt-get clean

# Copy frontend files into the container
COPY . .

# Install dependencies in a virtual environment
RUN pipenv install --deploy --ignore-pipfile

# Expose Streamlit's default port
EXPOSE 8501

# Run Streamlit app
CMD ["pipenv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
