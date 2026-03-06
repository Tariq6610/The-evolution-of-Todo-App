FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Hugging Face ONLY exposes 7860
EXPOSE 7860

CMD ["sh", "-c", "python chatbot_scripts/start_server.py"]
