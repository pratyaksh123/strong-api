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

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose Heroku's default port
EXPOSE $PORT

# Run Streamlit app
CMD sh -c "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"
