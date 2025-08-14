FROM python:3.11-slim-bullseye
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir python-multipart

# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y awscli curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . /app

# Ensure final_model directory exists and has proper permissions
RUN mkdir -p /app/final_model /app/prediction_output /app/logs

EXPOSE 8000

# Add health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["python3", "app.py"]