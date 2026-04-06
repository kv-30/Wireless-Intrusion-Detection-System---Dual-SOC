# Base image
FROM python:3.11-slim

# Install build tools
RUN apt-get update && apt-get install -y build-essential


# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY rf_api.py .
COPY artifacts/ artifacts/

# Expose port
EXPOSE 5000

# Run the Flask API
CMD ["python", "rf_api.py"]