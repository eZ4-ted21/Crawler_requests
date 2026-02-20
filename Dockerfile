# Use official Python image
FROM python:3.13-slim-bookworm

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set new working directory
WORKDIR /crawler_requests

# Copy requirements first (better caching)
COPY requirements.txt .
COPY gs_creds.json .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Default command
CMD ["python", "test.py"]
