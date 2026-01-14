# Use the Python 3 official image
FROM python:3.11-slim

# Run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Create and change to the app directory
WORKDIR /app

# Copy local code to the container image
COPY . ./

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app runs on
EXPOSE $PORT

# Run the web service on container startup
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port $PORT"]