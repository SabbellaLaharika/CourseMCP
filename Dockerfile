# Use a slim Python 3.12 base image for minimal footprint
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install curl for the Docker healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies first (leverages Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application source code
COPY . .

# Create the data directory in case it doesn't exist
RUN mkdir -p /app/data

# Expose port 8080
EXPOSE 8080

# Start the server using uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
