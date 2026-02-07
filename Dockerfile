# Use Python 3.13 slim image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install packages from requirements.txt file
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/