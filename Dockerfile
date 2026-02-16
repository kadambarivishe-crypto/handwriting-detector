FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY main.py .
COPY models/ ./models/

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main.py:app", "--host", "0.0.0.0", "--port", "8000"]