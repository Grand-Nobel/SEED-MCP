# Use a minimal Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy app files
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port for Fly.io
EXPOSE 8080

# Start the app using uvicorn (assuming FastAPI or similar)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
